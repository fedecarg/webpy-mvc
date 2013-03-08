import web

# environment
web.config.env = 'production'

# debug error messages
web.config.debug = False
            
# required adapter MySQLdb http://sourceforge.net/projects/mysql-python
web.config.database = web.database(dbn='mysql', user='username', pw='password', db='example')
