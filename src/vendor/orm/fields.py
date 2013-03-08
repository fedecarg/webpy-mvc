# orm.py is an extension to the database layer supplied with web.py.
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

import web

class Field(object):
    
    PROPERTIES = ['type', 'max_length', 'key', 'auto_increment', 'null', 'default']
    
    def __init__(self, **kwargs):
        for property in Field.PROPERTIES:
            method = 'set_%s' % property
            if not kwargs.get(property, None):
                getattr(self, method)()
            else:
                getattr(self, method)(kwargs[property])
    
    def set_type(self, type):
        types = ['varchar', 'tinyint', 'text', 'int', 'float', 'char',  'date', 'datetime', 'timestamp', 'enum', 'set', 'bool', 'binary']
        if not type in types:
            raise ValueError(type)
        self.type = type
    
    def set_max_length(self, max_length):
        self.max_length = int(max_length)
    
    def set_key(self, key=None):
        keys = ['primary', 'index', 'unique']
        if key and not key in keys:
            raise ValueError(key)
        self.key = key
    
    def set_auto_increment(self, value=False):
        if not isinstance(value, bool):
            raise ValueError(value)
        self.auto_increment = value
    
    def set_null(self, value=False):
        if not isinstance(value, bool):
            raise ValueError(value)
        self.null = value
    
    def set_default(self, value=None):
        self.default = value


class RelatedField(object):
    
    def __init__(self, model, field=None):
        self.model = model
        if isinstance(self.model, basestring):
            self.model = activerecords.get(model)
        self.field = field


class ForeignKeyField(RelatedField):
    
    def __get__(self, instance, owner):
        if not instance:
            return self.model
        if not self.field:
            self.field = '%s_id' % self.model.Meta.table
        conditions = {self.model.Meta.pk: getattr(instance, self.field)}
        return Query(model=self.model, conditions=conditions)[0]

class OneToManyField(RelatedField):
    
    def __get__(self, instance, owner):
        if not instance:
            return self.model
        if not self.field:
            self.field = '%s_id' % instance.Meta.table
        conditions = {self.field: getattr(instance, instance.Meta.pk)}
        return Query(model=self.model, conditions=conditions)

class ManyToManyField(RelatedField):
    pass


if __name__ == "__main__":
    import doctest
    web.config.istest = True
    doctest.testmod()