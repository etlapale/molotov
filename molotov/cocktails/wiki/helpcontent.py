# -*- coding: utf-8; -*-

import codecs, logging, os, os.path
from datetime import datetime

import cherrypy
from sqlobject import SQLObjectNotFound

from molotov.cocktails.wiki.model import Page, Revision

log = logging.getLogger("molotov.cocktails.wiki")

def generateHelpContent (force = False) :
    "Generate all the help wiki pages from the ``help`` directory."

    helpdir = cherrypy.config.get ("molotov.cocktails.wiki.helpdir")
    
    # List the help directory
    for filename in os.listdir (helpdir) :
        
        # We only process the *.rst files
        if not filename.endswith (".rst") :
            #log.debug ("Not a RST file `%s`" % filename)
            continue

        # Check the wiki page does not exists
        pagename = filename[:-4]
        try :
            page = Page.byPagename (pagename)
            page.destroySelf ()
            del page
            log.warning ("Generating content pages but page `%s` exists [force=%s]" % (pagename, force))
            if not force :
                continue
        except SQLObjectNotFound :
            pass

        # Get page data
        path = os.path.join (helpdir, filename)
        f = codecs.open (path, "r")
        content = f.read ()
        f.close ()

        log.debug ("Generating page `%s`" % pagename)
                
        # Create the wiki page
        page = Page (pagename = pagename)
        revision = Revision (rev = "0.0", date = datetime.now (),
                             user = None, ip = "127.0.0.1",
                             comment = "Automatic help content",
                             data = content, page = page)
