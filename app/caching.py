import app
import pickle
import settings
import openstack

def save_obj(obj):
    with open(settings.CACHE_FILENAME, 'wb') as f:
        print 'aqui 123'
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        app.cache.set('servers_list', obj, timeout=0)

def load_obj():
    try:
        with open(settings.CACHE_FILENAME, 'rb') as f:
            app.cache.set('servers_list', pickle.load(f), timeout=0)
    except:
        save_obj(openstack.load_servers_list())

def renew():
    save_obj(openstack.load_servers_list())
    return 'okay'
