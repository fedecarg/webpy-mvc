#!/usr/bin/env python

import web

from config import routes, environment
from vendor import mvc

app = mvc.application(routes.urls, {}, autoreload=True)
env = web.config.get('env')

if __name__ == '__main__':
    app.run()
