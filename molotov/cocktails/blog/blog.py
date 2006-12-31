# -*- coding: utf-8; mode: python; -*-
# © 2006-2007, Émilien TLAPALE

import logging
from datetime import datetime
import cherrypy
from docutils.core import publish_parts
from docutils.parsers.rst import Parser
from molotov import expose, redirect, url
from molotov.cocktails.blog.model import Billet, BilletComment
#from molotov.cocktails.wiki.wiki import WikiNameInliner

log = logging.getLogger ("molotov.cocktails.blog")

class Blog :
    "Blog controller for Molotov."

    def __init__ (self, config) :
        "Init the Blog controller."
        pass

    @expose (".templates.blog")
    def index (self) :
        "Display the list of blog billets."
        billets = Billet.select (orderBy = 'creation_date').reversed ()
        return dict (billets=list (billets))

    @expose (".templates.billet")
    def billet (self, billet) :
        "Display a specific billet."
        b = Billet.get (billet)
        return dict (billet=b)
    
    @expose (".templates.new_billet")
    def new_billet (self, title=None, data=None, billet=None) :
        return dict (title=title, data=data, billet=billet)

    @expose ()
    def do_new_billet (self, billet, title, data, submit) :
        if data and title:
            if submit == "preview" :
                return self.new_billet (title, data, billet=billet)
            if billet :
                return self.do_modify (billet, title, data)
            usr = cherrypy.session.get ("molotov.user", None)
            b = Billet (title = title, creation_date = datetime.now (),
                        user = usr, data = data)
        raise redirect ("/")

    @expose ()
    def modify (self, billet) :
        b = Billet.get (billet)
        return self.new_billet (b.title, b.data, b.id)

    @expose ()
    def do_modify (self, billet, title, data) :
        b = Billet.get (billet)
        b.title = title
        b.data = data
        raise redirect ("/")

    @expose ()
    def do_new_comment (self, billet, data) :
        if billet and data :
            usr = cherrypy.session.get ("molotov.user", None)
            print billet
            b = Billet.get (billet)
            c = BilletComment (data = data, creation_date = datetime.now (),
                               user = usr, billet = b)
        raise redirect ("/billet", billet=billet)
