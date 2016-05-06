import app
import settings

from openstack import load_servers_list, load_users_list, load_flavors_list, load_tenants_list, load_images_list


def load_users():
    users = load_users_list()
    app.cache.set('users_list', users, timeout=0)


def load_servers():
    servers = load_servers_list()
    app.cache.set('servers_list', servers, timeout=0)


def load_flavors():
    flavors = load_flavors_list()
    app.cache.set('flavors_list', flavors, timeout=0)


def load_tenants():
    tenants = load_tenants_list()
    app.cache.set('tenants_list', tenants, timeout=0)


def load_images():
    images = load_images_list()
    app.cache.set('images_list', images, timeout=0)


def renew():
    load_images()
    load_tenants()
    load_flavors()
    load_users()
    load_servers()
    print 'Cache loaded'
    return 'okay'
