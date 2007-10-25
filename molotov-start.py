#! /usr/bin/env python
# -*- coding: utf-8; mode: python; -*-

import cherrypy
import molotov.support

def main() :
    "Start a Molotov website."
    molotov.support.prepare()
    cherrypy.server.quickstart()
    cherrypy.engine.start()

if __name__ == '__main__' :
    main()
