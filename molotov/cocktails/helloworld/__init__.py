# -*- coding: utf-8; -*-

import cherrypy

class HelloWorld :
    def index (self) :
        return "Hello world!"
    index.exposed = True
    
controller = HelloWorld

