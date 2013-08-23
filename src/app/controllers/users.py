import hashlib, time
import web

from app.controllers.application import ApplicationController
from app.models.user import User, UserForm


class UsersController(ApplicationController):

    def index(self, page=1):
        self.users = User.all(page=page, limit=10)

    def new(self):
        form = UserForm.get('new')
        title = 'Add User (%s) ' % self.method
        if self.method == 'GET' or not form.validates():
            return self.render(title=title, form=form)
        else:
            data = form.d
            #data.api_key = hashlib.md5(data.name + str(time.time())).hexdigest()
            id = User(data).save()
            return self.redirect_to('/users/%s' % id)
    
    def show(self, id):
        user = User.find(id)
        return self.render(user=user)
    
    def delete(self, id):
        return self.notfound()
    