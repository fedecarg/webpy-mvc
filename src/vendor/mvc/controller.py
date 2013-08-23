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

import os
import web


class ActionController(object):
    """Rendering a template and sending a response back to the browser:
        
        >>> class UsersTestController(ActionController):
        ...     def index(self):
        ...         return self.render(title='home')
        ...
        >>> app = application({}, globals())
        >>> app.dispatch(controller='users_test', action='index')
        {'layout': 'layouts/main', 'render': {'title': 'home'}, 'view': 'users_test/index'}
        
    Accessing URL parameters in your controller action:

        >>> class UsersTestController(ActionController):
        ...     def edit(self):
        ...         self.id = self.params['id']
        ...
        >>> app.dispatch(controller='users_test', action='edit', id=1)
        {'layout': 'layouts/main', 'render': {'id': 1}, 'view': 'users_test/edit'}
            
    Rendering a view that corresponds to a different action within the same controller:
    
        >>> class UsersTestController(ActionController):
        ...     def index(self):
        ...         return self.render('foo')
        ... 
        >>> app.dispatch(controller='users_test', action='index')
        {'layout': 'layouts/main', 'render': {}, 'view': 'users_test/foo'}
            
    Rendering an action's template from another controller:

        >>> class UsersTestController(ActionController):
        ...     def index(self):
        ...         return self.render('books/index')
        ... 
        >>> app.dispatch(controller='users_test', action='index')
        {'layout': 'layouts/main', 'render': {}, 'view': 'books/index'}
                        
    Specifying a layout for a current controller:
    
        >>> class UsersTestController(ActionController):
        ...     layout = 'mobile'
        ...
        ...     def index(self):
        ...         return self.render()
        ... 
        >>> app.dispatch(controller='users_test', action='index')
        {'layout': 'layouts/mobile', 'render': {}, 'view': 'users_test/index'}
        
    Specifying a layout for a current action:
    
        >>> class UsersTestController(ActionController):
        ...     def index(self):
        ...         return self.render(layout='mobile')
        ... 
        >>> app.dispatch(controller='users_test', action='index')
        {'layout': 'layouts/mobile', 'render': {}, 'view': 'users_test/index'}
    
    Using the initialize method to put default values into instance variables:
    
        >>> class UsersTestController(ActionController):
        ...     def initialize(self):
        ...         self.title = 'home page'
        ...     def index(self):
        ...         return self.render(title=self.title)
        ... 
        >>> app.dispatch(controller='users_test', action='index')
        {'layout': 'layouts/main', 'render': {'title': 'home page'}, 'view': 'users_test/index'}
    """
    layout = 'main'
    
    
    def __init__(self, params):
        """web.ctx: data found in contextual variables http://webpy.org/cookbook/ctx"""
        self.env = web.ctx.get('env')
        self.method = web.ctx.get('method')
        self.params = params
        self.view = {}
        if hasattr(self, 'initialize'):
            self.initialize()
    
    
    def __dir__(self):
        return ['env', 'method', 'params', 'view']
    
    
    def __getattr__(self, attr):
        if attr in dir(self):
            return self.__dict__[attr]
        else:
            return self.__dict__['view'].get(attr)
    
    
    def __setattr__(self, attr, value):
        if attr in dir(self):
            self.__dict__[attr] = value
        else:
            self.__dict__['view'][attr] = value

    
    def render(self, view=None, layout=None, **kwargs):
        controller = self.params.get('controller')
        action = self.params.get('action')
        view = view or os.sep.join([controller, action]) 
        if not os.sep in view:
            view = os.sep.join([controller, view])
        layout = os.sep.join(['layouts', layout or self.layout])
        if controller.endswith('test'):
            return dict(view=view, layout=layout, render=kwargs)
        render = web.template.render(os.sep.join(['app', 'views']), base=layout)
        t = render._template(view)
        def template(**kw):
            return render._base(t(**kw))
        return template(**self.view)
    
    
    def respond_to(self, method):
        """
        Returns true if self responds to the given method. If the method is not 
        defined, false is returned.
        
            >>> class UsersController(ActionController):
            ...     def edit(self):
            ...         pass
            ... 
            >>> c = UsersController()
            >>> c.respond_to('edit')
            True
            >>> c.respond_to('create')
            False
        """
        return hasattr(getattr(self, method, None), '__call__')
        
    
    def redirect_to(self, controller=None, action=None):
        action = action or 'index'
        if controller:
            return self.redirect(os.sep.join([controller, action]))
        else:
            return getattr(self, action)() 
    
    
    def redirect(self, url, status=303):
        if status == 302:
            return web.found(url)
        elif status == 303:
            return web.seeother(url)
        elif status == 304:
            return web.notmodified(url)
        elif status == 306:
            return web.tempredirect(url)
        else:
            return web.seeother(url)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
