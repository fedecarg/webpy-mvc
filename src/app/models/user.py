import web
from web import form

class User(object):

    class Meta:
        table = 'user'
        fields = ['id', 'name']

    def __init__(self, data=None, **kwargs):
        data = data or kwargs
        for field in self.Meta.fields:
            self.__dict__[field] = data.get(field, None)

class UserDao(object):
    @classmethod
    def find(cls, id):
        return User({'id': id, 'name': 'User %s' % id})

    @classmethod
    def all(cls):
        return [
            User({'id': 1, 'name': 'User 1'}),
            User({'id': 2, 'name': 'User 2'}),
            User({'id': 3, 'name': 'User 3'})
        ]

class UserForm(object):
    
    @classmethod
    def get(cls, name):
        if name == 'new':
            return form.Form(
                form.Textbox('name', form.notnull, description='Name:')
            )
