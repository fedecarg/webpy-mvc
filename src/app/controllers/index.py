import web
from app.controllers.application import ApplicationController
from app.models.user import User

class IndexController(ApplicationController):

    def index(self):
        return self.redirect('/users')
