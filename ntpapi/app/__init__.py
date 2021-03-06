#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Andrés J. Díaz <ajdiaz@connectical.com>
#                  Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

import bottle

from gevent import monkey; monkey.patch_all()

class AppAPI(bottle.Bottle):
    def __init__(self, configs=[]):
        """Start a new Keybox application API

        :param config: a list of configuration files to read
        """
        bottle.Bottle.__init__(self)

        # Push application to bottle as default_app stack.
        bottle.app.push(self)

        # Enable debug mode if it's setted in configuration.
        bottle.debug(self.config.get('debug', False))
        bottle.DEBUG = self.config.get('debug', False)

        from . import apiv1

        # Nothing useful here, but lint checker likes it :)
        apiv1._loaded = True

    def run(self, *args, **kwargs):
        bottle.run(app=self, server='gevent', *args, **kwargs)
