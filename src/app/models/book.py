import web

from web import form
from vendor.orm import ActiveRecord


class Book(ActiveRecord):
    
    def publisher(self, options=None):
        return Publisher.find(self.publisher_id)
        #return Publisher.find(self.publisher_id)
    
    def authors(self, options=None):
        return BookAuthor.all(self.author_id, options)
        #return BookAuthor.find_all(options, where={'id':self.author_id})


class BookAuthor(ActiveRecord):
    pass