import hashlib, time
import web

from app.controllers.application import ApplicationController
from app.models.book import Book


class BooksController(ApplicationController):

    def index(self):
        self.books = Book.find("all")

    def show(self, id):
        self.book = Book.find(id)

    def new(self):
        self.book = Book()
        self.subjects = Subject.find("all")

    def create(self):
        self.book = Book(self.input('book'))
        if self.book.save():
            self.redirect_to(action="index")
        else:
            self.subjects = Subject.find("all")
            self.render("new") 

    def delete(self, id):
        Book.find(id).delete()
        self.redirect_to(action='index')
