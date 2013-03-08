import web
from app.controllers.application import ApplicationController

class ErrorsController(ApplicationController):

    def error_404(self, msg=None):
        return self.render('404')

    def error_500(self, msg=None):
        return self.render('500')
