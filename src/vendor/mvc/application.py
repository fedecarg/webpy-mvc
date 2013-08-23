# The mvc module provides MVC support to the existing web.py framework
#
# Copyright (c) 2012 Federico Cargnelutti
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software to deal in this software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of this software, and to permit
# persons to whom this software is furnished to do so, subject to the following
# condition:
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THIS SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THIS SOFTWARE.

import os, re
import web

from vendor.mvc.utils import import_class
from vendor.mvc.inflector import camelize, underscore


class Application(web.application):
    """Application class to delegate requests based on controllers and actions:
    
        >>> class ErrorsController(ActionController):
        ...     def error_404(self):
        ...         return '404 Not Found'
        ...     def error_500(self):
        ...         return '500 Internal Server Error'
        ...
        >>> class UsersTestController(ActionController):
        ...     def index(self):
        ...         return 'list users'
        ...     def show(self):
        ...         return 'show id %s' % self.params['id']
        ...     def update(self):
        ...         return 'update id %s' % self.params['id']
        ...     def delete(self):
        ...         return 'delete id %s' % self.params['id']
        ...
        >>> urls = ('/users/(\d+)',               {'controller':'users_test', 'action':'show', 'id':'{1}'},
        ...         '/users/(\d+)/delete',        {'controller':'users_test', 'action':'delete', 'id':'{0}'},
        ...         '/users/(\d+)/(edit|update)', {'controller':'users_test', 'action':'{1}', 'id':'{0}'},
        ...         '/users',                     {'controller':'users_test', 'action':'index'})
        ...
        >>> app = application(urls, globals())
        >>> app.request('/users').data
        'list users'
        >>> app.request('/users/7').data
        'show id 7'
        >>> app.request('/users/4/update').data
        'update id 4'
        >>> app.request('/users/5/delete').data
        'delete id 5'
        >>> response = app.request('/invalid')
        >>> response.status
        '404 Not Found'
    """
    def _delegate(self, f, fvars, args=None):
        args = args or []
        if not isinstance(f, dict):
            return web.application._delegate(self, f, fvars, args)
        
        route = dict(f)
        for key, val in route.items():
            if not val.startswith('{'):
                continue
            i = int(re.sub('\D', '', val))
            if not args or len(args) <= i:
                raise ValueError("invalid value for '%s' with '%s'" % (key, val))
            route[key] = args[i]
        
        return self.dispatch(**route)
    
    
    def dispatch(self, controller=None, action=None, **params):
        """Dispatch a request to a controller/action:
        
            >>> class UsersTestController(ActionController):
            ...     def test(self):
            ...         self.id = self.params['id']
            ...         self.name = self.params['name']
            ...
            >>> app = application({}, globals())
            >>> app.dispatch(controller='users_test', action='test', id=23, name='Test')
            {'layout': 'layouts/main', 'render': {'id': 23, 'name': 'Test'}, 'view': 'users_test/test'}
        """
        if not controller:
            raise self.notfound('controller missing or invalid')
        elif not action:
            raise self.notfound('action missing or invalid')
        cls = import_class('%sController' % camelize(controller), 'app.controllers.%s' % controller)
        if not hasattr(cls, action):
            raise self.notfound()
        params.update(dict(controller=controller, action=action))
        obj = cls(params)
        view = getattr(obj, action)()
        if not view:
            view = obj.render(action, **dict(obj.view))
        return view
    
    
    def notfound(self):
        html = self.dispatch('errors', 'error_404')
        return web.notfound(html)
        
    
    def internalerror(self):
        if web.config.get('debug'):
            return web.debugerror()
        html = self.dispatch('errors', 'error_500')
        return web.internalerror(html)


application = Application


if __name__ == "__main__":
    import doctest
    doctest.testmod()
