#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Andrés J. Díaz <ajdiaz@connectical.com>
#                  Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import os
import sys

from ntpapi import app


DEFAULT_DEVEL_PORT = 9099
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 9009


def wsgi(app_environ='production'):
    """Return WSGI handler for application."""
    return app.AppAPI([app_environ])


def dev():
    """dev [port]
    Run a development server in specific port (NTPAPI_PORT variable is valid too).
    Aditionally you can use NTPAPI_ENVIRON variable to force diferent environment to test.

    Never use this server for production.
    """
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = int(os.environ.get('NTPAPI_PORT', DEFAULT_DEVEL_PORT))

    wsgi(os.environ.get("NTPAPI_ENVIRON", 'development')).run(port=port)


def server():
    """server [host] [port]
    Run a production server in specific port (NTPAPI_HOST and NTPAPI_PORT variable is valid too).
    Aditionally you can use NTPAPI_ENVIRON variable to force diferent environment name.
    """
    host = sys.argv[2] if len(sys.argv) > 2 else os.environ.get('NTPAPI_HOST', DEFAULT_HOST)
    port = int(sys.argv[3]) if len(sys.argv) > 3 else int(os.environ.get('NTPAPI_PORT', DEFAULT_PORT))

    from gevent.pywsgi import WSGIServer
    print('Serving on {}:{}...'.format(host, port))
    WSGIServer((host, port), wsgi(os.environ.get("NTPAPI_ENVIRON", 'development'))).serve_forever()


def cli():
    """Command line script."""
    if len(sys.argv) > 1:
        if sys.argv[1] == 'cli':
            print('Nope')
        else:
            try:
                return globals()[sys.argv[1]]()
            except KeyError:
                print('{} is not a valid argument'.format(sys.argv[1]))
    else:
        for x, y in globals().items():
            if x != 'cli' and x != 'wsgi' and x[0] != '_' and hasattr(y, '__call__') and hasattr(y, '__doc__'):
                print('%s' % (y.__doc__,))
