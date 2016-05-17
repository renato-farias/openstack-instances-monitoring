# -*- coding: utf-8 -*-

from flask import current_app

def index(resource=None):
    return current_app.send_static_file('index.html')


def instances():
    return current_app.send_static_file('instances.html')


def report():
    return current_app.send_static_file('report.html')
