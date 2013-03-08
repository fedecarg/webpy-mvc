import hashlib, time
import web

from app.controllers.application import ApplicationController
from app.models.user import User


class UsersController(ApplicationController):


    def index(self, page=1):
        self.users = {}
        #self.users = User.all({'page': page, 'limit': 5})
        user = User.find(1)
        web.debug(user.posts())
        


    def new(self):
        form = User.form('new')
        title = 'Add User (%s) ' % self.request.get('method')
        if self.request.method == 'GET' or not form.validates():
            return self.render(title=title, form=form)
        
        data = form.d
        #data.api_key = hashlib.md5(data.name + str(time.time())).hexdigest()
        id = User(data).save()
        return self.redirect_to('/users/%s' % id)
    
    
    def show(self, id):
        user = User.find(id)
        return self.render(user=user)
    
    
    def delete(self, id):
        return self.notfound()
    