# -*- coding: utf-8; -*-
# Controller for the Wiki module

import logging

import cherrypy
from sqlobject import SQLObjectNotFound

import molotov
from molotov import expose, flash, redirect, url
from molotov.cocktails.wiki.model import Revision, Page
from molotov.cocktails.wiki.diffutils import diff_table

import os, re, codecs, subprocess
from datetime import datetime

from docutils import nodes
from docutils.utils import unescape
from docutils.core import publish_parts, publish_string
from docutils.parsers.rst import Parser, states

log = logging.getLogger("molotov.cocktails.wiki")

def next_revision (rev, major_update = False) :
    "Return the next revision number as a string."
    dot = rev.index ('.')
    major = int (rev[:dot])
    minor = int (rev[dot + 1:])
    if major_update :
        major += 1
        minor = 0
    else :
        minor += 1
    return "%d.%d" % (major, minor)

def previous_revision (revision) :
    prev = None
    for rev in revision.page.revisions :
        if rev == revision :
            return prev
        prev = rev
    return None

class WikiNameInliner (states.Inliner) :
    "Inliner for WikiNames."

    h_upper = u"A-ZÀÂÄÅÉÈÊËÎÏÔÖÛÜ"
    h_upper_re = ur"[" + h_upper + "]"
    h_lower = ur"a-zàåâäéèêëîïìôöòüûù"
    h_lower_re = "[" + h_lower + "]"
    h_any_re = ur"[0-9" + h_upper + h_lower + "]"
    wikiname_re = re.compile (ur"\b(" + h_upper_re \
                             + h_lower_re + "+" \
                             + h_upper_re + "+" \
                             + h_any_re + "*)",
                              re.LOCALE | re.UNICODE)
    #wikilink_re = re.compile (ur"\[[^\]]+\]", re.LOCALE | re.UNICODE)
    
    def __init__ (self, root) :
        states.Inliner.__init__ (self)
        self.root = root
        self.implicit_dispatch.append ((self.wikiname_re, self.wikiname))
        #self.implicit_dispatch.append ((self.wikilink_re, self.wikilink))
        
    def wikiname (self, match, lineno) :
        text = match.group (0)
        ref = self.root + text
        unescaped = unescape (text, 0)
        r = nodes.reference (unescape (text, 1), unescaped, refuri = ref)
        r["classes"].append ("wikiname")
        return [r]
        
    def wikilink (self, match, lineno) :
        text = match.group (0)[1:-1]
        ref = self.root + text
        unescaped = unescape (text, 0)
        r = nodes.reference (unescape (text, 1), unescaped, refuri = ref)
        r["classes"].append ("wikiname")
        return [r]

class Wiki :
    "Wiki controller for Molotov."

    frontpage_name = "FrontPage"
    "Wiki front page name."

    max_history = 3
    "Maximum history length."

    def __init__ (self, config) :
        "Init a Wiki controller."
        pass

    def update_history (self, pagename, history) :
        "Update the user history with a new pagename."

        h = history

        # Remove any previous occurence
        if pagename in h :
            h.remove (pagename)
        
        # Append the new pagename
        h = [pagename] + history

        # Check the history size
        if len (h) > self.max_history :
            h = h[:self.max_history]
        
        return h
    
    @molotov.expose ('.templates.page')
    def index (self, pagename = frontpage_name, format = "web") :
        
        # Search for an existing page
        try :
            page = Page.byPagename (pagename)
        except SQLObjectNotFound :
            # Not yet a FrontPage => fresh install => generate help content
            if pagename == self.frontpage_name :
                from helpcontent import generateHelpContent
                generateHelpContent ()
                flash ("Help pages generated")
                page = Page.byPagename (pagename)
            else :
                raise redirect ('/edit', pagename = pagename)

        # Update the user page history
        history = self.update_history (pagename,
                                       cherrypy.session.get ('history', []))
        cherrypy.session['history'] = history

        # Get last page modifier
        revision = page.revisions[-1]

        # Check the format
        if format == "plain" :
            cherrypy.response.headers['Content-Type'] = \
                    'text/plain; charset=%s' % \
                    cherrypy.config.get ("molotov.charset", "utf-8")
            return revision.data
        elif format == "xml" :
            cherrypy.response.headers['Content-Type'] = 'text/xml'
            return molotov.format_rst (revision.data, format='xml')
        
        # Convert the WikiSyntax format to HTML
        content = molotov.format_rst (revision.data, format='html')['html_body']
        
        return dict (data=content, page=page, revision=revision,
                     history = history)

    @expose ()
    def default (self, pagename = frontpage_name, **kw) :
        "Make a catch-all redirection to `index ()`."
        return self.index (pagename)

    @molotov.expose ('.templates.pagelist')
    def pagelist (self) :
        pages = [page.pagename for page \
                 in Page.select (orderBy = Page.q.pagename)]
        return dict (page = None, pages = pages,
                     history = cherrypy.session.get ('history', []))
    
    @molotov.expose ('.templates.edit')
    def edit (self, pagename, major = False) :
        "Edit a wiki page."
        data = None
        page = None
        try :
            page = Page.byPagename (pagename)
            data = page.revisions[-1].data
        except SQLObjectNotFound :
            data = u""
        # We give pagename as page can be None
        return dict (page = page, pagename = pagename, data = data,
                     major = major,
                     history = cherrypy.session.get ('history', []))

    @expose ()
    def save (self, pagename, data, title, major, submit) :
        "Save changed made to a page."

        print submit, submit.__class__, str (submit)
        if submit == u"Previsualiser" :
            return self.preview (pagename=pagename, data=data,
                                 title=title, major=major)

        # Existing page
        try :
            page = Page.byPagename (pagename)

            # Get previous revision number
            prev = page.revisions[-1].rev
            dot = page
            
            # Create the new Revision
            revision = Revision (rev = next_revision (prev, major),
                                 date = datetime.now (),
                                 user = cherrypy.session.get ('molotov.user', None),
                                 ip = "127.0.0.1",
                                 comment = title, data = data, page = page)
        # New page
        except SQLObjectNotFound :
            page = Page (pagename = pagename)
            revision = Revision (rev = "0.0", date = page.modif_date,
                                 user = identity.current.user,
                                 ip = "127.0.0.1",
                                 comment = title, data = data, page = page)
        flash ("Changes saved!")
        raise redirect (url ("/%s" % page.pagename))

    @expose (".templates.preview")
    def preview (self, pagename, data, title, major = False) :
        "Preview a change in a wiki page."

        # Fetch the edited page
        page = None
        try :
            page = Page.byPagename (pagename)
        except SQLObjectNotFound :
            pass
        
        # Convert the WikiSyntax format to HTML
        content = molotov.format_rst (data, format='html') ['html_body']
        
        return dict (page = page, pagename = pagename, data = data,
                     html_data = content,
                     modif_title = title,
                     user = cherrypy.session.get ('user', None),
                     major = major,
                     history = cherrypy.session.get ('history', []))

    @expose ()
    def preview_revision (self, modif) :
        "Preview a previous wiki page modification."

        # Fetch the given Revision
        mod = None
        try :
            mod = Revision.get (modif)
        except SQLObjectNotFound :
            flash ("Revision not found")
            raise redirect (url ("/"))

        # Preview
        return self.preview (mod.page.pagename, mod.data,
                             'Retour à une version précédente')

    @expose (".templates.revision")
    def revision (self, modif, prev = None) :

        # Fetch the given Revision
        rev = None
        try :
            rev = Revision.get (modif)
        except SQLObjectNotFound :
            flash ("Revision not found")
            raise redirect (url ("/"))
        
        # Get the previsous revision
        if not prev :
            prev = previous_revision (rev)
        else :
            prev = Revision.get (prev)

        # Diff the data
        html_diff = ""
        if prev :
            html_diff = diff_table (prev.data, rev.data)

        # Wiki presentation
        data = molotov.format_rst (rev.data)['html_body']
        
        # Preview
        return dict (diff = html_diff,
                     history = cherrypy.session.get ('history', []),
                     data = data, page = rev.page, revision = rev)

    @expose ()
    def diff (self, rev1, rev2, submit = None) :
        return self.revision (modif = rev2, prev = rev1)

    @expose (".templates.modifs")
    def modifs (self, pagename) :
        "Display the successive modifications of a wiki page."

        # Get the page
        page = None
        try :
            page = Page.byPagename (pagename)
        except SQLObjectNotFound :
            flash ("Wiki page not found")
            raise redirect (url ("/"))

        # Fetch the modifs
        return dict (page = page,
                     history = cherrypy.session.get ('history', []))

    @expose ()
    def generate_help (self, force = False) :
        "Regenerate the help content."
        from helpcontent import generateHelpContent
        generateHelpContent (force = force)
        flash ("Help pages generated")
        raise redirect (url ("/"))

    @expose ()
    def upload (self, upload_file, pagename, new, **kw) :
        "Attach a file to the given page."
        page = None
        try :
            page = Page.byPagename (pagename)
        except SQLObjectNotFound :
            flash ("Page not found: `%s`" % pagename)
            raise redirect (url ("/"))

        target_path = os.path.join (cherrypy.config.get ("wiki.uploads"),
                                    upload_file.filename)
        try :
            u = Uploaded.byFilename (upload_file.filename)
            flash ("File `%s` already uploaded" % upload_file.filename)
            raise redirect (url ("/"))
        except SQLObjectNotFound :
            f = open (target_path, 'wb')
            f.write (upload_file.file.read ())
            f.close ()
            u = Uploaded (filename = upload_file.filename, path = target_path,
                          size = 0, date = datetime.now (),
                          user = identity.current.user, ip = "127.0.0.1")
        page.addUploaded (u)
        raise redirect (url ("/%s" % pagename))
