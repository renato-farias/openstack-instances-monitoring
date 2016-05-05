# -*- coding: UTF-8 -*-

from openstack import get_servers
from utils import myjsonify

def servers():
    return myjsonify({'instances': get_servers()})

def search(s):
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

