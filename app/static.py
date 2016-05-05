# -*- coding: utf-8 -*-

from flask import current_app

def index():
    return current_app.send_static_file('index.html')
