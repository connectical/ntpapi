#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Andrés J. Díaz <ajdiaz@connectical.com>
#                  Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import os
import bottle
import ntplib
from time import gmtime, asctime


NTP_SERVER = os.environ.get('NTPAPI_NTP_SERVER', '127.0.0.1')


def get_data():
    try:
        c = ntplib.NTPClient()
        response = c.request(NTP_SERVER, version=3)
        return response
    except:
        bottle.abort(500,'Time server not reachable')


@bottle.get('/api/1/offset')
def offset():
    response = get_data()

    if bottle.request.query.get('raw') is not None:
        bottle.response.content_type = 'text/plain'
        return "%s" % response.offset
    if bottle.request.query.get('json') is not None:
        return {"format": "json",
                "offset": response.offset}
    return bottle.abort(400, "Bad Request")


@bottle.get('/api/1/time')
def time():
    response = get_data()

    if bottle.request.query.get('raw') is not None:
        bottle.response.content_type = 'text/plain'
        return "%s" % asctime(gmtime(response.tx_time))
    if bottle.request.query.get('json') is not None:
        return {"format": "json",
                "time": asctime(gmtime(response.tx_time)),
                "timestamp": response.tx_time}
    return bottle.abort(400, "Bad Request")


@bottle.get('/api/1/stats')
def stats():
    response = get_data()

    return {
            "time": asctime(gmtime(response.tx_time)),
            "offset": response.offset,
            "leap": ntplib.leap_to_text(response.leap),
            "delay": response.root_delay,
            "ref": ntplib.ref_id_to_text(response.ref_id),
            "stratum": ntplib.stratum_to_text(response.stratum),
            "timestamp": response.tx_time
    }
