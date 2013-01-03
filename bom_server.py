#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
from pprint import pprint

urls = (
  '/', 'index',
  '/after/(.*)', 'after',
)


db = web.database(dbn="sqlite", db="bom.db")


def json_encode_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


class index:
    def GET(self):

        upcs = []

        for upc in db.select('upc'):
            upcs.append(upc)

        web.header('Content-Type', 'application/json')
        return json.dumps(upcs, default=json_encode_handler)


class after:
    def GET(self, after_id):

        upcs = []

        vars = dict(id = after_id)
        for upc in db.select('upc', vars, where="id > $id"):
            upcs.append(upc)

        web.header('Content-Type', 'application/json')
        return json.dumps(upcs, default=json_encode_handler)


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()