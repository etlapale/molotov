# -*- coding: utf-8; -*-

import logging, urllib
import buffet, cherrypy, kid
import molotov

log = logging.getLogger ("molotov")

running_cocktails = []
"Global running cocktails list."

def expose (template_name = None) :
    """
    Exposed functions can be viewed by web clients.
    """
    def expose_decorator (func) :
        log.debug ('Exposing %s' % str (func))
        
        # Load a relative template
        if template_name and template_name[0] == "." :
            mod = func.__module__
            real_tmpl = mod[:mod.rfind (".")] + template_name
            print "Using template %s for %s" % (real_tmpl, template_name)
        else :
            real_tmpl = template_name
        
        def exposed_func (*args, **kw) :
            # Get the dictionary
            d = func (*args, **kw)
            if not isinstance (d, dict) :
                log.debug ("Not a dictionary: %s" % str (d.__class__))
                if isinstance (d, str) :
                    return d
                else :
                    return d.encode ('utf-8')

            # Given variables
            d['mltv'] = d['molotov'] = molotov
            d['molotov_title'] = cherrypy.config.get ('molotov.title', 'Molotov')
            d['molotov_cocktails'] = molotov.running_cocktails

            # User
            usr = cherrypy.session.get ('molotov.user', None)
            if usr :
                username = usr.name
            else :
                username = None
            d['molotov_user'] = d['mltv_user'] = username
            groups = []
            if not usr is None :
                print usr.groups
                for grp in usr.groups :
                    groups.append (grp.name)
            d['molotov_groups'] = groups
            
            return (real_tmpl, d)
        if template_name :
            return cherrypy.expose (exposed_func)
        else :
            return cherrypy.expose (func)
    return expose_decorator

def flash (msg) :
    "Display a message on next page to be viewed by the current user."
    cherrypy.session['molotov.flash'] = msg

def has_flash () :
    return cherrypy.session.get ('molotov.flash', None) != None

def get_flash () :
    ans = cherrypy.session.get ('molotov.flash', None)
    cherrypy.session['molotov.flash'] = None
    log.debug ("get_flash () = %s" % str (ans))
    return ans

def url (mltv_url_path, mltv_url_params = None, **kw) :

    # Prefix path and params with mltv_url so **kw does not contains them
    
    if not isinstance (mltv_url_path, basestring) :
        mltv_url_path = "/".join (list (mltv_url_path))
    if mltv_url_path.startswith ("/") :
        app_root = "/".join (cherrypy.request.path.split ("/")[:-1])
        if len (app_root) > 1 and app_root[-1] == "/" :
            app_root = app_root[:-1]
        mltv_url_path = app_root + mltv_url_path
        result = mltv_url_path
    else :
        result = mltv_url_path
    if mltv_url_params is not None :
        mltv_url_params.update (kw)
    else :
        mltv_url_params = kw
    args = []
    
    # Process the arguments
    for key, value in mltv_url_params.iteritems () :
        if value is None :
            continue
        if isinstance (value, unicode) :
            value = value.encode ('utf-8')
        args.append ('%s=%s' % (key, urllib.quote (str (value))))
    if len (args) :
        result += "?" + "&".join (args)
    
    return result

def redirect(redirect_path, redirect_params=None, **kw):
    """Redirect (via cherrypy.HTTPRedirect)."""
    raise cherrypy.HTTPRedirect (url (mltv_url_path = redirect_path,
                                      mltv_url_params = redirect_params,
                                      **kw))
