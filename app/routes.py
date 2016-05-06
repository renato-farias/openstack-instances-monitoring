# -*- coding: UTF-8 -*-

from flask import Blueprint, current_app

from api import _servers, _search, _users, _get_server, _flavors, _tenants, _images
from static import index
from caching import renew

routes = Blueprint('routes', __name__, static_folder='../static')

routes.add_url_rule('/', view_func=index, methods=['GET'])
routes.add_url_rule('/users', view_func=_users, methods=['GET'])
routes.add_url_rule('/servers', view_func=_servers, methods=['GET'])
routes.add_url_rule('/flavors', view_func=_flavors, methods=['GET'])
routes.add_url_rule('/tenants', view_func=_tenants, methods=['GET'])
routes.add_url_rule('/images', view_func=_images, methods=['GET'])
routes.add_url_rule('/server/<server_id>', view_func=_get_server, methods=['GET'])
routes.add_url_rule('/search/<s>', view_func=_search, methods=['GET'])
routes.add_url_rule('/renew', view_func=renew, methods=['GET'])

