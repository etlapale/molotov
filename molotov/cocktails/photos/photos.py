# -*- coding: utf-8; mode: python; -*-
# © 2007, Émilien TLAPALE <emilien at tlapale dot com>


import logging
from datetime import datetime

import cherrypy

from docutils.core import publish_parts
from docutils.parsers.rst import Parser

from molotov import identity
from molotov import expose, flash, redirect, url
from molotov.captcha import create_captcha, check_captcha
from molotov.cocktails.photos.model import Photo


log = logging.getLogger("molotov.cocktails.photos")


class Photos :
    '''A tagged photography album for Molotov.'''

    def __init__ (self, config) :
        pass

    @expose (".templates.main")
    def index (self) :
        "Welcome page for the photo album website."
        billets = Billet.select (orderBy = 'creation_date').reversed()
        return dict (billets=list (billets))
