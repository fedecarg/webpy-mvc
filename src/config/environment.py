import os
import web

if 'production' == os.environ.get('APP_ENV'):
    import config.environments.production
else:
    import config.environments.development
