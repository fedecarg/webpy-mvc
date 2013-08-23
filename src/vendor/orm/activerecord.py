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
from vendor.orm.fields import Field, RelatedField


db = web.config.get('database', None)
ModelStorage = web.utils.Storage()


class ActiveRecordMetaclass(type):
    
    def __new__(cls, record_name, bases, dct):
        if record_name == 'ActiveRecord':
            return super(ActiveRecordMetaclass, cls).__new__(cls, record_name, bases, dct)
        elif hasattr(ModelStorage, record_name):
            return ModelStorage[record_name]
        
        record = type.__new__(cls, record_name, bases, dct)
        if not getattr(record, 'id', None):
            record.id = Field(type='int', max_length='11', key='primary', auto_increment=True)
        record.__add_metadata()
        ModelStorage[record_name] = record
        
        return record
    
    def __add_metadata(self):
        if not hasattr(self, 'Meta'):
            self.Meta = type('Meta', (), {})        
        self.Meta.table = self.__name__.lower() if not hasattr(self.Meta, 'table') else self.Meta.table
        self.Meta.ordering = 'id ASC' if not hasattr(self.Meta, 'ordering') else self.Meta.ordering
        self.Meta.fields = self.__dict__.keys()
        self.Meta.data = Data()
        self.Meta.associations = {}
        # columns for the table associated with this class
        self.Meta.columns = {}
        self.Meta.column_aliases = []
        for k, v in self.__dict__.items():            
            if isinstance(v, RelatedField):
                self.Meta.associations.setdefault(v.__class__.__name__, []).append(v)
            elif isinstance(v, Field):
                self.Meta.columns[k] = v
                self.Meta.column_aliases.append('%s.%s AS "%s.%s"' % (self.Meta.table, k, self.__name__, k))


class ActiveRecord(object):
    """
    ActiveRecord closely follows the standard ORM model, which is as follows:

      - Tables map to classes
      - Rows map to objects and
      - Columns map to object attributes
      
    To translate a domain model into SQL, you have to follow certain rules:
    
      - Each entity class (such as User) gets a table in the database named after it.
      - Each such entity-matching table has a field called id, which contains a unique 
        integer for each record inserted into the table.
      - Given entity x and entity y, if entity y belongs to entity x, then table y has 
        a field called x_id.
      - Database fields map to entity's class attributes.        
    """
    __metaclass__ = ActiveRecordMetaclass
    
    
    @classmethod
    def find(cls, id=None, options={}, **params):
        """
        Find operates with different retrieval approaches:
        
        1. find(id): This will return the record matched by the given id.
        2. find('all', options): This will return all the records matched by the options used. 
        
            >>> class User(ActiveRecord):
            ...     class Meta:
            ...         table = 'users'
            ... 
            >>> User.find(1)
            <sql: 'SELECT * FROM users WHERE id = 1'>
            >>> User.find()
            <sql: 'SELECT * FROM users ORDER BY id LIMIT 50 OFFSET 0'>
            >>> User.find('all')
            <sql: 'SELECT * FROM users ORDER BY id LIMIT 50 OFFSET 0'>
            >>> User.find('all', what='name', where={'name':'foo'})
            <sql: "SELECT name FROM users WHERE name = 'foo' ORDER BY id LIMIT 50 OFFSET 0">
            >>> User.find('all', {'limit':5}, what='name', where={'name':'foo'})
            <sql: "SELECT name FROM users WHERE name = 'foo' ORDER BY id LIMIT 5 OFFSET 0">
        """
        if id and isinstance(id, int):
            return cls.find_by_id(id, **params)
        elif id and isinstance(id, str):
            return cls.find_by_id(int(id), **params)
        else:
            return cls.find_all(options, **params)
    
    
    @classmethod
    def find_by_id(cls, id, **params):
        """        
        This will return the record matched by the id. If no record can be found 
        for the given id, then False is returned.        
        
            >>> class User(ActiveRecord):
            ...     pass
            ... 
            >>> User.find_by_id(1)
            <sql: 'SELECT * FROM user WHERE id = 1'>
            >>> User.find_by_id(1, what='name', where={'gender':'m'})
            <sql: "SELECT name FROM user WHERE gender = 'm' AND id = 1">
        """
        where = {'id': int(id)}
        if 'where' in params:
            where = dict(params['where'].items() + where.items())
            del params['where']
        row = db.select(cls.Meta.table, where=web.db.sqlwhere(where), **params)
        if web.config.istest: return row
        try:
            return cls(dict(row[0]))
        except:
            return False
    
    
    @classmethod
    def find_all(cls, **options):
        """
        This will return all the records matched by the options used. If no records 
        are found, an empty array is returned.
        
            >>> class User(ActiveRecord):
            ...     pass
            ... 
            >>> User.find_all()
            <sql: 'SELECT * FROM user ORDER BY id LIMIT 50 OFFSET 0'>
            >>> User.find_all(what='name', where={'name':'foo'})
            <sql: "SELECT name FROM user WHERE name = 'foo' ORDER BY id LIMIT 50 OFFSET 0">
            >>> User.find_all(where={'name':'foo'}, limit=5, page=2)
            <sql: "SELECT * FROM user WHERE name = 'foo' ORDER BY id LIMIT 5 OFFSET 5">
        """        
        opts = cls.merge_options(options)
        rows = db.select(cls.Meta.table, _test=web.config.istest, **opts)
        #if web.config.istest: return rows
        
        records = []
        for row in rows:
            records.append(cls(row))

        """
        page = 1 if not 'page' in options else int(options['page'])
        num_of_rows = db.query('SELECT COUNT(*) AS count FROM %s' % cls._table)[0].count
        next_page = page + 1 if (page + 1) * 5 < num_of_rows else None
        previous_page = page - 1 if page > 0 else None
        """
        return records
    
    
    @classmethod
    def all(cls, **options):
        return cls.find_all(**options)
    
    
    @classmethod
    def delete_all(cls, ids, **options):
        """
        Deletes multiple rows using a SQL DELETE statement, and returns the number of rows deleted. 
        Objects are not instantiated with this method.
        
            >>> class User(ActiveRecord):
            ...     pass
            ... 
            >>> User.delete([1, 2])
            <sql: "DELETE FROM user WHERE id IN ('1', '2')">
        """
        if not isinstance(ids, list):
            raise ValueError(ids)
        where = 'id IN (%s)' % ', '.join(["'%s'" % n for n in ids])
        return db.delete(cls.Meta.table, where=where, _test=web.config.istest, **options)
    
    
    @classmethod
    def merge_options(cls, options, opts={}):
        opts['limit'] = 100 if not 'limit' in options else int(options['limit'])
        opts['offset'] = 0 if options['page'] <= 1 else (options['page'] - 1) * options['limit']
        opts['order'] = 'id ASC' if not 'order' in options else options['order']
        if 'where' in options and isinstance(options['where'], dict):
            opts['where'] = web.db.sqlwhere(options['where'])
        return opts
        
    
    def __init__(self, data=None, **kwargs):
        """
        Active Records accept constructor parameters in a dictionary data type. 
        This is useful when you are receiving the data from somewhere else.
        
            >>> class User(ActiveRecord):
            ...     class Meta:
            ...         table = 'users'
            ... 
            >>> user = User({'name':'foo'})
            >>> user.get_attrs()
            {'name': 'foo'}
            >>> user.email = 'foo@email.com'
            >>> user.get_attrs()
            {'name': 'foo', 'email': 'foo@email.com'}
            >>> user.id
            >>> user.save()
            >>> user.id
        """
        data = data or kwargs
        for field in self.Meta.fields:
            self.__dict__[field] = data.get(field, None)
        self.Meta.data.new(data)
    
    
    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.Meta.data)    

    
    def __setattr__(self, attr, value):
        if isinstance(self.Meta.columns.get(attr, None), Field): 
            self.Meta.data[attr] = value
        self.__dict__[attr] = value
                    
    
    def respond_to(self, method):
        """
        Returns true if self responds to the given method. If the method is not 
        defined, false is returned.
        
            >>> class Post(ActiveRecord):
            ...    pass
            ...
            >>> class User(ActiveRecord):
            ...     posts = has_many(Post)
            ... 
            >>> user = User()
            >>> user.respond_to('posts')
            True
            >>> user.respond_to('account')
            False
        """
        return hasattr(getattr(self, method, None), '__call__')
    
    
    def create(self, **kwargs):
        """
        Creates an object and saves it to the database, if validations pass. The resulting 
        object is returned whether the object was saved successfully to the database or not.
        
        The attributes parameter is a dictionary that describe the attributes on the object 
        that is to be created. 
        """
        pass
    
    
    def save(self):
        """
        Saves the model. If the model is new a record gets created in the database, 
        otherwise the existing record gets updated.
        
            >>> class User(ActiveRecord):
            ...     class Meta:
            ...         table = 'users'            
            ... 
            >>> user = User({'name':'foo'})
            >>> user.email = 'foo@email.com'
            >>> user.save()
            <sql: "INSERT INTO users (name, email) VALUES ('foo', 'foo@email.com')">
            >>> user = User({'id':1, 'name':'foo'})
            >>> user.name = 'updated'
            >>> user.save()
            <sql: "UPDATE users SET name = 'updated' WHERE id = 1">
        """
        istest = web.config.istest
        if not self.Meta.data:
            return False
        elif self.id:
            where = "id='%s'" % self.id
            affected_rows = db.update(self.Meta.table, where, _test=istest, **self.Meta.data)
            if affected_rows > 0:
                self.Meta.data.clear()
            return affected_rows
        else:
            inserted_id = db.insert(self.Meta.table, _test=istest, **self.Meta.data)
            if inserted_id:
                self.__dict__['id'] = '0' if istest else inserted_id 
                self.Meta.data.clear()
            return inserted_id
        
    
    def count(self, where=None, **options):
        """
        Returns the total count of rows or False on error. Count operates using two different approaches:
         
        1. Count all: By not passing any parameters to count, it will return a count of all the 
           rows for the model. 
        
            >>> class User(ActiveRecord):
            ...     __docttest__ = True
            ... 
            >>> User.count()
            
        2. Count using options will find the row count matched by the options used.
        
            >>> User.count({'name':'foo'}) 
        """
        if isinstance(where, dict):
            where = web.db.sqlwhere(where)
        istest = web.config.istest
        result = db.select(self.Meta.table, what='COUNT(*) AS count', where=where, _test=istest, **options)
        try:
            return result[0].count
        except IndexError:
            return False


class Data(dict):
    
    def __init__(self, dct={}):
        if dct: self.new(dct)
    
    def __setitem__(self, key, value):
        if key == 'id':
            raise KeyError(key)
        super(Data, self).__setitem__(key, value)
    
    def new(self, dct):
        if 'id' in dct:
            return False
        elif not isinstance(dct, dict):
            raise TypeError(dct)
        elif isinstance(dct, web.utils.Storage):
            dct = dict(dct)
        for k, v in dct.items():
            self[k] = v
            

web.config.istest = False

if __name__ == "__main__":
    import doctest
    web.config.istest = True
    doctest.testmod()
