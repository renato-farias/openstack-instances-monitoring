#!/usr/bin/env python
# -*- coding: utf-8 -*-

import caching
import settings
import openstack

from flask import Flask
from routes import routes
from werkzeug.contrib.cache import MemcachedCache

app = Flask(settings.APPLICATION_NAME, static_url_path='')
app.secret_key = 'openstack_monitoring'

app.register_blueprint(routes)

cache = MemcachedCache(['127.0.0.1:11211'])

def setup_app(app):
    caching.load_servers()
    
setup_app(app)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception, e:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
        print str(e)
