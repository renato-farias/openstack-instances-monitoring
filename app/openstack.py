import app
import json
import caching
import requests
import settings

os_token = None
headers = {'content-type': 'application/json'}

def auth():
    global os_token, tenant_id, admin_url
    json_post = {
        "auth": {
            "tenantName": "B2W Digital",
            "passwordCredentials": {
                "username": "zabbix",
                "password": "qbXFWHjBZD6S"
            }
        }
    }
    r = requests.post("http://api.fr.cloudopen.com.br:35357/v2.0/tokens",
        data=json.dumps(json_post), headers=headers)
    os_token = r.json()['access']['token']['id']
    tenant_id = r.json()['access']['token']['tenant']['id']
    admin_url = r.json()['access']['serviceCatalog'][0]['endpoints'][0]['adminURL'].replace('http://', '')


def get_token():
    if not os_token:
        auth()
    return os_token


def load_servers_list():
    l = []
    headers['X-Auth-Token'] = get_token()
    r = requests.get("http://%s/servers?all_tenants=true" % admin_url, headers=headers)
    for s in r.json()['servers']:
        # l.append(s['id'])
        l.append(s)
    return l


def list_servers():
    return app.cache.get('servers_list')


def get_servers():
    return list_servers()

