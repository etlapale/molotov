# -*- coding: utf-8; mode: python; -*-
# © 2006, Émilien TLAPALE

import logging
from datetime import datetime
import cherrypy
from docutils.core import publish_parts
from docutils.parsers.rst import Parser
from molotov import expose, redirect, url
from molotov.cocktails.blog.model import Billet, BilletComment
#from molotov.cocktails.wiki.wiki import WikiNameInliner

log = logging.getLogger ("molotov.cocktails.blog")

def rst2html (data) :
    # TODO: a global main rst2html
    root = str (url ("/"))
    #inliner = WikiNameInliner (root)
    #parser = Parser (inliner = inliner)
    return publish_parts (data, #parser = parser,
                          writer_name = 'html')['html_body']

class Blog :
    "Blog controller for Molotov."

    def __init__ (self, config) :
        "Init the Blog controller."
        pass

    @expose ("molotov.cocktails.blog.templates.blog")
    def index (self) :
        "Display the list of blog billets."
        billets = Billet.select (orderBy = 'creation_date').reversed ()
        return dict (billets = list (billets), rst2html = rst2html)

    @expose ("molotov.cocktails.blog.templates.billet")
    def billet (self, billet) :
        "Display a specific billet."
        b = Billet.get (billet)
        return dict (billet = b, rst2html = rst2html)
    
    @expose ("molotov.cocktails.blog.templates.new_billet")
    def new_billet (self) :
        return dict ()

    @expose ()
    def do_new_billet (self, title, data) :
        if data and title :
            usr = cherrypy.session.get ("molotov.user", None)
            b = Billet (title = title, creation_date = datetime.now (),
                        user = usr, data = data)
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
