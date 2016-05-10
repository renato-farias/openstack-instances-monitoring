# -*- coding: utf-8 -*-

import yaml

from os import getenv

config = yaml.load(open('config/application.yaml'))

APP_ENV             = getenv('APP_ENV', 'development')
APPLICATION_NAME    = 'openstack_monitoring'

MONGODB_HOST        = config.get('mongodb', {}).get('host', 'localhost')
MONGODB_PORT        = config.get('mongodb', {}).get('port', 27017)
MONGODB_BASE        = config.get('mongodb', {}).get('base', APPLICATION_NAME)

PROJECTS            = config.get('projects', [])
