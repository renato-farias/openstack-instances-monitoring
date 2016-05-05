# -*- coding: utf-8 -*-

import json

from flask import make_response

def myjsonify(data=None, code=200, headers=None):
    data = [] if not data else data
    r = make_response(json.dumps(data,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        encoding='utf8') + '\n',
        code)
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    if headers:
        for k,v in headers.items(): r.headers[k] = v
    return r
