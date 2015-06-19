#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json

urls = (
  '/', 'index',
  '/after/(.*)', 'after',
)

db = web.database(dbn="sqlite", db="bom.db")


def json_encode_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError(
            'Object of type {0} with value of {1} is not JSON serializable.'.format(
                type(obj),
                repr(obj)
            )
        )


class index:
    def GET(self):

        upcs = []

        for upc in db.select('upc'):
            upcs.append(upc)

        web.header('Content-Type', 'application/json')
        return json.dumps(upcs, default=json_encode_handler)


class after:
    def GET(self, after_uuid):

        upcs = []

        results = db.select(
            'upc',
            dict(after_uuid = after_uuid),
            where="uuid = $after_uuid"
        )

        # Find the UPC we want all the UPCs after.
        after_upc = None
        for upc in results:
            after_upc = upc

        if after_upc:
            # If we find it, get all the UPCs after this one.
            results = db.select(
                'upc',
                dict(after_id = after_upc.id),
                where="id > $after_id"
            )

            for upc in results:
                upcs.append(upc)
        else:
            # Can't find the 'after' UPC so just select them all.
            for upc in db.select('upc'):
                upcs.append(upc)

        web.header('Content-Type', 'application/json')
        return json.dumps(upcs, default=json_encode_handler)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()