# -*- coding: utf-8; -*-
# Controller for the Wiki module

import logging, os.path, sys, time
from datetime import datetime

import cherrypy
from sqlobject import SQLObjectNotFound

import molotov
from molotov import expose, flash, url

import svn.fs, svn.core, svn.repos

dlog = logging.getLogger("molotov.cocktails.repository")

def printable_size (size) :
    "Return a printable version of the size."
    return "%d bytes " % size

def printable_date (date) :

    d = datetime.fromtimestamp (time.mktime (time.strptime \
                                             (date[0:19], "%Y-%m-%dT%H:%M:%S")))
    diff = datetime.now () - d
    if diff.days > 365 :
        years = diff.days / 365
        if years == 1 :
            return "1 year"
        else :
            return "%d years" % years
    elif diff.days > 7 :
        weeks = diff.days / 7
        if weeks == 1 :
            return "1 week"
        else :
            return "%d weeks" % weeks
    elif diff.days > 1 :
        return "%d days" % diff.days
    elif diff.days == 1 :
        return "1 day"
    elif diff.seconds > 3600 :
        hours = diff.seconds / 3600
        if hours == 1 :
            return "1 hour"
        else :
            return "%d hours" % hours
    else :
        minutes = diff.seconds / 60
        if minutes > 1 :
            return "%d minutes" % minutes
        else :
            return "1 minute"

def last_index (str, c) :
    pos = len (str) - 1
    while pos >= 0 :
        if str[pos] == c :
            return pos
        pos -= 1
    raise Exception ("Character not found: `%s` in `%s`" % (c, str))

def get_parent (dirname) :
    if not dirname or len (dirname) == 0:
        return dirname
    pos = last_index (dirname, '/')
    if pos == 0 :
        return "/"
    return dirname[:pos]

def dirname (path) :
    post = last_index (path, '/')
    return path[post+1:]

def get_parents (path) :
    parents = []
    while len (path) > 1 :
        name = dirname (path)
        parents = [(name, path)] + parents
        path = path[:len (path) - len (name) - 1]
        dlog.debug (path)
        dlog.debug (parents)
    return parents

class Repository :
    "Subversion repository viewer."

    def __init__ (self, config) :
        "Create a new repository viewer."
        repo_path = config.get ("molotov.cocktails.repository.repo_path")
        self.path = repo_path
        self.repo = svn.repos.open (repo_path)
        self.fs = svn.repos.fs (self.repo)

    @expose ("molotov.cocktails.repository.templates.repository")
    def index (self, directory = "", revision = None) :
        """
        List a repository directory for a given revision.
        """

        last_revision = svn.fs.youngest_rev (self.fs)
        if revision :
            revision = int (revision)
        else :
            revision = last_revision

        # Nicer root path
        if directory == "/" :
            directory = ""

        # Open the directory for the given revision
        root = svn.fs.revision_root (self.fs, revision)

        # List the directory children
        entries = svn.fs.dir_entries (root, directory)
        keys = entries.keys ()
        keys.sort ()

        dirs = []
        files = []
        for name in keys :
            path = directory + '/' + name
            created_rev = svn.fs.node_created_rev (root, path)
            author = svn.fs.revision_prop (self.fs, created_rev,
                                           svn.core.SVN_PROP_REVISION_AUTHOR)
            date = svn.fs.revision_prop (self.fs, created_rev,
                                         svn.core.SVN_PROP_REVISION_DATE)
            date = printable_date (date)
            log = svn.fs.revision_prop (self.fs, created_rev,
                                        svn.core.SVN_PROP_REVISION_LOG)
            if author is None :
                auth_log = log
            else :
                auth_log = author + ": " + log
            max_log_len = cherrypy.config.get (
                "molotov.cocktails.repository.max_log_len", 60)
            if max_log_len >= 0 and len (auth_log) > max_log_len :
                auth_log = auth_log[:max_log_len - 3] + "..."
            
            if svn.fs.is_dir (root, path) :
                dirs.append ((name, created_rev, date, auth_log))
            else :
                size = printable_size (svn.fs.file_length (root, path))
                files.append ((name, size, created_rev, date, auth_log))

        return dict (dirs = dirs, files = files, parent=get_parent (directory),
                     parents=get_parents (directory),
                     last_revision=last_revision,
                     directory = directory, revision = revision, 
                     history = [], page = None)

    @expose ("molotov.cocktails.repository.templates.view")
    def view (self, path, revision = None) :
        
        if revision :
            revision = int (revision)
        else :
            revision = svn.fs.youngest_rev (self.fs)

        # Open the root for the given revision
        root = svn.fs.revision_root (self.fs, revision)

        # Open and read the file
        stream = svn.fs.file_contents (root, path)
        size = int (svn.fs.file_length (root, path))
        data = svn.core.svn_stream_read (stream, size)
        svn.core.svn_stream_close (stream)

        parent = get_parent (path)
        return dict (path = path, lines = data.splitlines (),
                     parents = get_parents (parent), revision = revision,
                     history = [], page = None)

    @expose ("molotov.cocktails.repository.templates.log")
    def log (self) :
        last_rev = svn.fs.youngest_rev (self.fs)
        revisions = []

        for i in xrange (last_rev, 0, -1) :
            date = svn.fs.revision_prop (self.fs, i,
                                         svn.core.SVN_PROP_REVISION_DATE)
            d = datetime.fromtimestamp (time.mktime (time.strptime \
                                                     (date[0:19], "%Y-%m-%dT%H:%M:%S")))
            author = svn.fs.revision_prop (self.fs, i,
                                           svn.core.SVN_PROP_REVISION_AUTHOR)
            log = svn.fs.revision_prop (self.fs, i,
                                        svn.core.SVN_PROP_REVISION_LOG)
            revisions.append ([i, d, author, log])
        
        return dict (revisions = revisions)
