## Introduction
- - -

mvc.py provides mvc support to the existing [web.py](http://webpy.org/) python framework.

## Requirements

* Python 2.6+
* web.py 0.36+

## Installation

1. Install web.py using pip:

        $ pip install web.py

2. Download mvc.py:

        $ curl -L https://github.com/fedecarg/webpy-mvc/tarball/ | tar xzf

3. Start up the web server:

        $ python app.py

4. Have a cup of tea (optional)

## Configuration

The configuration file config/application.py and environment-specific configuration files allow you to specify the various settings that you want to pass down to the mvc.py module.

For example, the default config/application.py file includes this setting:

```python
# debug error messages
web.config.debug = True
```

### Configuring a database

web.py works with many database systems, including MySQL, PostgreSQL and SQLite.

**SQLite**

```python
web.config.database = web.database(dbn='sqlite', db='db/example.sqlite')
```

**MySQL and Postgres**

If you choose to use MySQL or Postgres instead of the shipped SQLite database, your config/application.py will look something like this: 

```python
web.config.database = web.database(dbn='mysql', user='username', pw='password', db='example')
```

## Directory structure

+ **app**: Application package that organizes your application MVC components.  
+ **app/controllers**: The controllers subdirectory is where mvc.py looks to find controller classes.   
+ **app/helpers**: The helpers subdirectory holds any helper classes used to assist the model, view, and controller classes.    
+ **app/models**: The models subdirectory holds the classes that model and wrap the data stored in our application's database.  
+ **app/views**: The views subdirectory holds the display templates to fill in with data from our application, convert to HTML, and return to the user's browser.   
+ **app/views/layouts**: Holds the template files for layouts to be used with views.    
+ **config**: This directory contains the small amount of configuration code that your application will need, including your database configuration and mvc.py environment structure.    
+ **db**: Database schema, data and migration files.    
+ **lib**: You'll put libraries here, unless they explicitly belong elsewhere.  
+ **static**: This directory has web files that don't change, such as JavaScript files, graphics and stylesheets.   
+ **test**: The unit tests and doctests you write go here.  
+ **vendor**: Libraries provided by third-party vendors go here.    

## Controllers

Controller classes inherit from ApplicationController, a base class that contains code that can be run in all your controllers. Controllers are made up of one or more actions that are executed on request and then either render a template or redirect to another action. It's up to you what name you want to give to these methods. Everything is done very much “the rails way”. Here is a sample rails controller and its equivalent in mvc.py:

### rails controller

```ruby
class BooksController < ApplicationController

    def list
        @books = Book.find(:all)
    end
    
    def show
        @book = Book.find(params[:id])
    end
    
    def new
        @book = Book.new
        @subjects = Subject.find(:all)
    end
    
    def create
        @book = Book.new(params[:book])
        if @book.save
            redirect_to :action = > 'list'
        else
            @subjects = Subject.find(:all)
            render :action = > 'new'
        end
    end
    
    def delete
        Book.find(params[:id]).destroy
        redirect_to :action = > 'list'
    end
end
```

### mvc.py controller

```python
class BooksController(ApplicationController)

    def index(self):
        books = Book.find('all')
        return self.render(books=books)
        
    def show(self, id):
        book = Book.find(id)
        return self.render(book=book)
        
    def new(self):
        book = Book()
        subjects = Subject.find('all')
        return self.render(book=book, subjects=subjects)
    
    def create(self):
        book = Book(self.params['book'])
        if book.save():
            return self.redirect_to(action='index')
        else:
            subjects = Subject.find('all')
            return self.render('new', book=book, subjects=subjects, error='Error message') 
    
    def delete(self, id):
        Book.find(id).delete()
        return self.redirect_to(action='index')
```

## Views

If you look in the app/views directory, you will see one subdirectory for each of the controllers we have in app/controllers.Application Controller sends content to the user by using the render method, which enables rendering of HTML templates. The controller passes a dictionary to the view using the render method:

```python
class BooksController(ApplicationController)
    def index(self):
        return self.render(title='home')
```

Accessing URL parameters in your controller action:

```python
class BooksController(ApplicationController)
    def edit(self, id):
        return self.render(id=id)
```

Rendering a view that corresponds to a different action within the same controller:

```python
class BooksController(ApplicationController)
    def index(self):
        return self.render('foo')
```

Rendering an action's template from another controller:

```python
class BooksController(ApplicationController)
    def index(self):
        return self.render('books/index')
```

Specifying a layout for a current controller:

```python
class BooksController(ApplicationController)
    layout = 'mobile'
    
    def index(self):
        return self.render()
```

Specifying a layout for a current action:

```python
class BooksController(ApplicationController)
    def index(self):
        return self.render(layout='mobile')
```

Using the initialize method to put default values into instance variables:

```python
class BooksController(ApplicationController)
    def initialize(self):
        self.title = 'home page'

    def index(self):
        return self.render(title=self.title)
```


## The Default 500 and 404 Templates

By default an application will render either a 404 or a 500 error message. These messages are contained in static HTML files in the app/views/errors folder, in 404.html and 500.html respectively. You can customize these files to add some extra information and layout.

## Feedback

If for whatever reason you spot something to fix but cannot patch it yourself, please open an issue.  Also, any kind of discussion regarding web frameworks is more than welcome.




 