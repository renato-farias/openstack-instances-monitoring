# -*- coding: UTF-8 -*-

from openstack import get_servers, \
                      get_users, \
                      get_flavors, \
                      get_tenants, \
                      get_images, \
                      get_server, \
                      get_user, \
                      get_flavor, \
                      get_tenant, \
                      get_image
from utils import myjsonify

def _servers():
    return myjsonify({'instances': get_servers()})

def _users():
    return myjsonify({'users': get_users()})

def _flavors():
    return myjsonify({'flavors': get_flavors()})


def _tenants():
    return myjsonify({'flavors': get_tenants()})


def _images():
    return myjsonify({'images': get_images()})

def _search(s):
    l = []

    if len(s) >= 3:
        servers = get_servers()
        try:
            for i in servers:
                if s in i['name']:
                    l.append(i)
        except Exception, e:
            print str(e)
    
    return myjsonify({'instances': l})


def _get_server(server_id):
    s = get_server(server_id)
    if s is not None:
        u = get_user(s['user_id'])
        s.pop('user_id')
        s['user'] = u

        f = get_flavor(s['flavor_id'])
        s.pop('flavor_id')
        s['flavor'] = f

        t = get_tenant(s['tenant_id'])
        s.pop('tenant_id')
        s['tenant'] = t

        i = get_image(s['image_id'])
        s.pop('image_id')
        s['image'] = i

    return myjsonify(s)

