import web

from web import form
from vendor.orm import ActiveRecord
from app.models.post import Post


class User(ActiveRecord):
    
    def posts(self, options=None):
        return Post.find_all(options, where={'user_id':self.id})
    

class UserForm(object):
    
    @classmethod
    def get(cls, name):
        if name == 'new':
            return form.Form(
                form.Textbox('name', form.notnull, description='Name:')
            )
