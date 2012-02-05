## Introduction

The module mvc.py provides MVC support to the existing [web.py](http://webpy.org/) Python framework.

## Requirements

* Python 2.6+
* web.py 0.36+

## Installation

1. Install web.py using pip ([other options here](http://webpy.org/install))

```
    $ pip install web.py
```

2. Download mvc.py

```    
    $ curl -L https://github.com/fedecarg/webpy-mvc/tarball/ | tar xzf
```

3. Start up the web server

```
    $ python app.py
```

4. Have a cup of tea (optional)

## Configuration

The configuration file config/application.py and environment-specific configuration files (such as config/environments/production.py) allow you to specify the various settings that you want to pass down to the mvc.py module.

For example, the default config/application.py file includes this setting:

```python
# debug error messages
web.config.debug = True
```

### Configuring a database

web.py works with many database systems, including MySQL, PostgreSQL and SQLite.

**SQLite**

```python
# database connection
web.config.database = web.database(dbn='sqlite', db='db/example.sqlite')
```

**MySQL and Postgres**

If you choose to use MySQL or Postgres instead of the shipped SQLite database, your config/application.py will look a little different: 

```python
# database connection
web.config.database = web.database(dbn='mysql', user='username', pw='password', db='example')
```

## Directory structure

You will find a directory structure as follows:

+ **app**: Application package that organizes your application MVC components.  
+ **app/controllers**: The controllers subdirectory is where mvc.py looks to find controller classes.   
+ **app/helpers**: The helpers subdirectory holds any helper classes used to assist the model, view, and controller classes.    
+ **app/models**: The models subdirectory holds the classes that model and wrap the data stored in our application's database.  
+ **app/views**: The views subdirectory holds the display templates to fill in with data from our application, convert to HTML, and return to the user's browser.   
+ **app/views/layouts**: Holds the template files for layouts to be used with views.    
+ **config**: This directory contains the small amount of configuration code that your application will need, including your database configuration (in database.yml), your mvc.py environment structure (environment.rb), and routing of incoming web requests (routes.rb). You can also tailor the behavior of the three mvc.py environments for test, development, and deployment with files found in the environments directory.    
+ **db**: Database schema, data and migration files.    
+ **lib**: You'll put libraries here, unless they explicitly belong elsewhere.  
+ **static**: This directory has web files that don't change, such as JavaScript files, graphics and stylesheets.   
+ **test**: The unit tests and doctests you write go here.  
+ **vendor**: Libraries provided by third-party vendors go here.    

## Feedback

If for whatever reason you spot something to fix but cannot patch it yourself, please open an issue.  Also, any kind of discussion regarding web frameworks is more than welcome.




 