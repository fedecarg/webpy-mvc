import web

from app.controllers.application import ApplicationController
from app.models.user import User


class IndexController(ApplicationController):

    def index(self):
        user = User.find(3)
        web.debug(self.params)
