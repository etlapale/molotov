#! /usr/bin/env python
# -*- coding: utf-8; mode: python; -*-

import codecs, locale, logging, optparse, os.path, sys
import cherrypy
from cherrypy.config import dict_from_config_file
from cherrypy.lib import autoreload
from sqlobject import connectionForURI, sqlhub

import molotov

def update_config (conf, env) :
    d = {}
    if conf not in autoreload.reloadFiles:
        autoreload.reloadFiles.append (conf)
        d = dict_from_config_file (conf, False, env)
    cherrypy.config.update (updateMap = d)

def main () :
    "Start a Molotov website."

    # Load the default locale
    locale.setlocale (locale.LC_ALL, '')

    # Parse the arguments
    parser = optparse.OptionParser ()
    (options, args) = parser.parse_args ()
    if len (args) != 1 :
        print >>sys.stderr, "Usage: %s [options] config_file" % sys.argv[0]
        sys.exit ()

    # Load the default config
    prefix_dir = os.path.dirname (sys.argv[0])
    generic_config = os.path.join (prefix_dir, "share", "generic.conf")
    env = {"molotov_prefix" : prefix_dir}
    update_config (generic_config, env)
    logging.basicConfig (level = logging.DEBUG,
                         format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    log = logging.getLogger ('molotov')

    # Load the specific config
    if not os.path.isfile (args[0]) :
        print >>sys.stderr, "Config file not found: `%s`" % args[0]
        sys.exit ()
    update_config (args[0], env)
    cherrypy.config.update ({"global" : {"molotov.cocktails.wiki.helpdir" :
                                         os.path.join (prefix_dir,
                                                       cherrypy.config.get ("molotov.cocktails.wiki.helpdir"))}})

    # SQL initialization
    db_uri = cherrypy.config.get ("molotov.sql_engine")
    sql_con = connectionForURI (db_uri)
    sqlhub.processConnection = sql_con
    import molotov.model
    
    # Load the required cocktails
    cocktails = map (lambda s : s.strip (),
                     cherrypy.config.get ("molotov.cocktails").split (","))
    log.debug ('Loading cocktails: %s' % str (cocktails))
    root = None
    for cocktail in cocktails :
        log.debug ('  Init cocktail %s' % cocktail)
        mod = __import__ ("molotov.cocktails." + cocktail,
                          globals (), locals (),
                          ["molotov_controller", "molotov_name"])
        if hasattr (mod, "molotov_controller") :
            child = mod.molotov_controller (cherrypy.config)
            if hasattr (mod, "molotov_name") :
                name = mod.molotov_name
            else :
                name = child.__class__.__name__
            if root == None :
                root = child
                molotov.running_cocktails.append ((name, "/"))
            else :
                setattr (root, cocktail, child)
                molotov.running_cocktails.append ((name, "/" + cocktail))
        else :
            log.error ("%s seems not being a valid cocktail" % cocktail)

    # Start the CherryPy server
    cherrypy.root = root
    cherrypy.server.start ()

if __name__ == '__main__' :
    main ()
