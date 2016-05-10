# -*- coding: UTF-8 -*-

import pymongo

import settings

def get_mongodb():
    try:
        c = pymongo.MongoClient(settings.MONGODB_HOST,
                                settings.MONGODB_PORT)
        return c[settings.MONGODB_BASE]
    except:
        return None

def get_instance_collection(instance_id):
    c = get_mongodb()
    if c:
        return c['instance_%s' % instance_id]
    return None
