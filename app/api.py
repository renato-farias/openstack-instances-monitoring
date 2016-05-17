# -*- coding: UTF-8 -*-

import re
import datetime

from flask import request
from utils import myjsonify
from mongo import get_instance_collection
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


def _post_monitoring():
    f = request.form
    instance_id = f['instance_id']
    cpu_usage   = f['cpu']
    mem_usage   = f['mem']

    if cpu_usage == '' or cpu_usage is None:
        cpu_usage = 0

    if mem_usage == '' or mem_usage is None:
        mem_usage = 0

    d = {
        'log_date': datetime.datetime.now(),
        'cpu': float(cpu_usage),
        'mem': float(mem_usage)
    }
    get_instance_collection(instance_id).insert_one(d)
    return myjsonify({'status': 200})


def _get_monitoring(instance_id, monitorying_type):

    q = {}
    s = {
        '_id': 0,
        'log_date': 1
    }

    if monitorying_type == 'cpu':
        s['cpu'] = 1
    elif monitorying_type == 'mem':
        s['mem'] = 1

    d = []
    result = get_instance_collection(instance_id).find(q, s).sort('log_date')
    for r in result:
        if r[monitorying_type] == '' or r[monitorying_type] == None:
            r[monitorying_type] = 0
        d.append([
            # new_date,
            int(r['log_date'].strftime('%s')) * 1000,
            float(r[monitorying_type])
        ])
    return myjsonify({'data': d})


def _get_usage_report():
    # initializing the counter
    counter_zero = {'vms': 0, 'mem': 0, 'cpu': 0, 'disk': 0}
    report = {'_total': counter_zero.copy()}
    servers = get_servers()
    flavors = get_flavors()
    for s in servers:
        if s['project'] not in report.keys():
            report[s['project']] = counter_zero.copy()
        # increasing the vm number
        report['_total']['vms'] += 1
        report[s['project']]['vms'] += 1
        # get flavor's information
        for f in flavors:
            if f['id'] == s['flavor_id']:
                # increasing the cpu number
                report['_total']['cpu'] += f['vcpus']
                report[s['project']]['cpu'] += f['vcpus']
                # increasing the mem number
                report['_total']['mem'] += (f['ram']/1024)
                report[s['project']]['mem'] += (f['ram']/1024)
                # increasing the mem number
                report['_total']['disk'] += f['disk']
                report[s['project']]['disk'] += f['disk']
                break

    report['_size'] = len(report.keys())-1

    return myjsonify(report)
