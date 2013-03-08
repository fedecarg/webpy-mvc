import web

# environment
web.config.env = 'development'

# debug error messages
web.config.debug = True
            
# database connectio
web.config.database = web.database(dbn='sqlite', db='db/example.sqlite')
