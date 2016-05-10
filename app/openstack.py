import app
import json
import requests
import settings

os_token = None
headers = {'content-type': 'application/json'}

auth_cache = {}

projects = settings.PROJECTS

def auth(project_name):
    project = projects[project_name]
    auth_cache[project_name] = {}

    json_post = {
        'auth': {
            'tenantName': project['auth_tentant'],
            'passwordCredentials': {
                'username': project['auth_user'],
                'password': project['auth_pass']
            }
        }
    }

    # cleaning up older token
    if 'X-Auth-Token' in headers.keys():
        headers.pop('X-Auth-Token')

    r = requests.post('%s/v2.0/tokens' % project['auth_url'], data=json.dumps(json_post), headers=headers)
    auth_cache[project_name]['token'] = r.json()['access']['token']['id']
    for item in r.json()['access']['serviceCatalog']:
        if item['name'] == 'nova':
            auth_cache[project_name]['nova_admin_url'] = item['endpoints'][0]['publicURL']
        if item['name'] == 'keystone':
            auth_cache[project_name]['keystone_admin_url'] = item['endpoints'][0]['adminURL']


def get_token(project_name):
    if project_name not in auth_cache.keys():
        auth(project_name)
    return auth_cache[project_name]['token']


def load_tenants_list():
    l = []
    for project in projects.keys():
        headers['X-Auth-Token'] = get_token(project)
        r = requests.get("%s/tenants" % auth_cache[project]['keystone_admin_url'], headers=headers)
        for t in r.json()['tenants']:
            l.append({
                'id': t['id'],
                'name': t['name']
            })
    return l


def load_images_list():
    l = []
    for project in projects.keys():
        headers['X-Auth-Token'] = get_token(project)
        r = requests.get("%s/images/detail?all_tenants=1" % auth_cache[project]['nova_admin_url'], headers=headers)
        for i in r.json()['images']:
            l.append({
                'id': i['id'],
                'name': i['name']
            })
    return l


def load_servers_list():
    l = []
    for project in projects.keys():
        headers['X-Auth-Token'] = get_token(project)
        r = requests.get("%s/servers/detail?all_tenants=1" % auth_cache[project]['nova_admin_url'], headers=headers)
        for s in r.json()['servers']:

            networks = []
            for nets in s['addresses']:
                for net in s['addresses'][nets]:
                    networks.append({
                        'type': net['OS-EXT-IPS:type'],
                        'addr': net['addr'],
                    })

            l.append({
                'id': s['id'],
                'name': s['name'],
                'status': s['status'].lower(),
                'networks': networks,
                'user_id': s['user_id'],
                'flavor_id': s['flavor']['id'],
                'image_id': s['image']['id'],
                'tenant_id': s['tenant_id'],
                'hypervisor': s['OS-EXT-SRV-ATTR:host'],
                'project': str(project)
            })
    return l


def load_users_list():
    l = []
    for project in projects.keys():
        headers['X-Auth-Token'] = get_token(project)
        r = requests.get("%s/users" % auth_cache[project]['keystone_admin_url'], headers=headers)
        for u in r.json()['users']:
            l.append({
                'id': u['id'],
                'name': u['name'],
                'email': u['email'],
                'username': u['username']
            })
    return l


def load_flavors_list():
    l = []
    for project in projects.keys():
        headers['X-Auth-Token'] = get_token(project)
        r = requests.get('%s/flavors/detail' % auth_cache[project]['nova_admin_url'], headers=headers)
        for f in r.json()['flavors']:
            l.append({
                'id': f['id'],
                'name': f['name'],
                'ram': f['ram'],
                'vcpus': f['vcpus'],
                'disk': f['disk']
            })
    return l


def list_servers():
    return app.cache.get('servers_list')


def list_users():
    return app.cache.get('users_list')


def list_flavors():
    return app.cache.get('flavors_list')


def list_tenants():
    return app.cache.get('tenants_list')


def list_images():
    return app.cache.get('images_list')


def get_servers():
    return list_servers()


def get_server(server_id):
    for s in get_servers():
        if s['id'] == server_id:
            return s
    return None


def get_users():
    return list_users()


def get_user(user_id):
    for u in get_users():
        if u['id'] == user_id:
            return u
    return None


def get_flavors():
    return list_flavors()


def get_flavor(flavor_id):
    for f in get_flavors():
        if f['id'] == flavor_id:
            return f
    return None


def get_tenants():
    return list_tenants()


def get_tenant(tenant_id):
    for t in get_tenants():
        if t['id'] == tenant_id:
            return t
    return None


def get_images():
    return list_images()


def get_image(image_id):
    for i in get_images():
        if i['id'] == image_id:
            return i
    return None
