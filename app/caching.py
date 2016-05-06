import app
import settings

from openstack import load_servers_list

def load_servers():
    app.cache.set('servers_list', load_servers_list(), timeout=0)

def renew():
    load_servers()
    return 'okay'
