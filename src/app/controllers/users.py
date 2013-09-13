import hashlib, time
import web
from app.controllers.application import ApplicationController
from app.models.user import UserDao, UserForm

class UsersController(ApplicationController):

    def index(self, page=1):
        users = UserDao.all()
        return self.render(users=users)

    def new(self):
        form = UserForm.get('new')
        title = 'Add User (%s) ' % self.method
        token = hashlib.md5(str(time.time())).hexdigest()
        if self.method == 'GET' or not form.validates():
            return self.render(title=title, form=form, token=token)
        else:
            data = form.d
            #UserDao.save(data)
            return self.redirect_to('/users/%s' % id)
    
    def show(self, id):
        user = UserDao.find(id)
        return self.render(user=user)
    
    def delete(self, id):
        return self.notfound()
    