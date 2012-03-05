# Introduction

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

## Routing

web.py's URL handling scheme is simple yet powerful and flexible. at the top of each application, you usually see the full URL dispatching scheme defined as a tuple:

```python
urlpatterns = (
    '/books/new',    {'controller':'books', 'action':'new'},
    '/books/create', {'controller':'books', 'action':'create'},
    '/books',        {'controller':'books', 'action':'index'},
    '/',             {'controller':'index', 'action':'index'}
)
```
Routes have priority defined by the order of appearance of the routes. The priority goes from top to bottom. The last route in that file is at the lowest priority will be applied last. If no route matches, 404 is returned.

You can utilize the power of regular expressions to design more flexible url patterns. For example, /books/(new|create) will catch either new or create. The key point to understand is that this matching happens on the path of your URL. For example:

```python
urlpatterns = (
    '/books/(new|create)', {'controller':'books', 'action':'{0}'},
    '/books',              {'controller':'books', 'action':'index'},
    '/',                   {'controller':'index', 'action':'index'}
)
```

In the url pattern you can catch parameters which can be used in your handler class:

```python
urlpatterns = (
    '/books/(new|create)',          {'controller':'books', 'action':'{0}'},
    '/books/(\d+)/(edit|delete)',   {'controller':'books', 'action':'{1}', 'id':'{0}'},
    '/books/(\d+)',                 {'controller':'books', 'action':'show', 'id':'{0}'},
    '/books',                       {'controller':'books', 'action':'index'},
    '/',                            {'controller':'index', 'action':'index'}
)
```

## Controllers

Controller classes inherit from ApplicationController, a base class that contains code that can be run in all your controllers. Controllers are made up of one or more actions that are executed on request and then either render a template or redirect to another action. It's up to you what name you want to give to these methods. Everything is done very much “the rails way”. Here is a sample rails controller and its equivalent in mvc.py:

### rails controller

```ruby
class BooksController < ApplicationController

    def index
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
            redirect_to :action => 'index'
        else
            @subjects = Subject.find(:all)
            render :action => 'new'
        end
    end
    
    def delete
        Book.find(params[:id]).destroy
        redirect_to :action => 'index'
    end
end
```

### mvc.py controller

```python
class BooksController(ApplicationController)

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
```

## Views

If you look in the app/views directory, you will see one subdirectory for each of the controllers we have in app/controllers. Application Controller sends content to the user by using the render method, which enables rendering of HTML templates:

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


### The default 500 and 404 templates

By default an application will render either a 404 or a 500 error message. These messages are contained in static HTML files in the app/views/errors folder, in 404.html and 500.html respectively. You can customize these files to add some extra information and layout.

## Feedback

If for whatever reason you spot something to fix but cannot patch it yourself, please open an issue.  Also, any kind of discussion regarding web frameworks is more than welcome.



 