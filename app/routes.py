# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app

from api import servers, search
from static import index
from caching import renew

routes = Blueprint('routes', __name__, static_folder='../static')

routes.add_url_rule('/', view_func=index, methods=['GET'])
routes.add_url_rule('/servers', view_func=servers, methods=['GET'])
routes.add_url_rule('/search/<s>', view_func=search, methods=['GET'])
routes.add_url_rule('/renew', view_func=renew, methods=['GET'])

