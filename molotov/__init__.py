# -*- coding: utf-8; -*-

import logging, os, os.path, sys, urllib
import cherrypy
import kid
from docutils.core import publish_parts
import molotov

log = logging.getLogger("molotov")

running_cocktails = []
"Global running cocktails list."

def find_template(template) :
    tmpl_path = template.replace(".", os.sep)
    ppath = ''
    if 'PYTHONPATH' in os.environ:
	ppath = os.environ['PYTHONPATH'].split(':')
    exts = ['.kid', '']
    for d in ppath :
        for e in exts :
            path = os.path.join(d, tmpl_path + e)
            if os.path.isfile(path) :
                return path
    return None

def expose(template_name = None) :
    """
    Exposed functions can be viewed by web clients.
    """
    def expose_decorator(func) :
        log.debug('Exposing %s' % str(func))
        
        # Load a relative template
        if template_name and template_name[0] == "." :
            pers_tmpl = cherrypy.config.get("molotov.templates")
            if pers_tmpl :
                mod = func.__module__
                real_tmpl = pers_tmpl + "." \
                            + mod[:mod.rfind(".")] + template_name
            else :
                mod = func.__module__
                real_tmpl = mod[:mod.rfind(".")] + template_name
        else :
            real_tmpl = template_name

        if real_tmpl :
            tpath = find_template(real_tmpl)
            if tpath is None :
                print "Could find the template %s" % real_tmpl
                sys.exit(1)
        
        def exposed_func(*args, **kw) :
            # Get the dictionary
            d = func(*args, **kw)
            if not isinstance(d, dict) :
                log.debug("Not a dictionary: %s" % str(d.__class__))
                if isinstance(d, str) :
                    return d
                else :
                    return d.encode('utf-8')

            # Given variables
            d['mltv'] = d['molotov'] = molotov
            d['molotov_title'] = cherrypy.config.get('molotov.title', 'Molotov')
            d['molotov_cocktails'] = molotov.running_cocktails

            # User
            usr = cherrypy.session.get('molotov.user', None)
            if usr :
                username = usr.name
            else :
                username = None
            d['molotov_user'] = d['mltv_user'] = username
            groups = []
            if not usr is None :
                print usr.groups
                for grp in usr.groups :
                    groups.append(grp.name)
            d['mltv_groups'] = d['molotov_groups'] = groups

            # Templatize
            tmpl_obj = kid.Template(name=real_tmpl)
            for(k, v) in d.iteritems() :
                setattr(tmpl_obj, k, v)
            tmpl_obj.assume_encoding = cherrypy.config.get('molotov.charset')
            return tmpl_obj.serialize(output=cherrypy.config.get('molotov.output'))
        if template_name :
            return cherrypy.expose(exposed_func)
        else :
            return cherrypy.expose(func)
    return expose_decorator

def flash(msg) :
    "Display a message on next page to be viewed by the current user."
    cherrypy.session['molotov.flash'] = msg

def has_flash() :
    return cherrypy.session.get('molotov.flash', None) != None

def get_flash() :
    ans = cherrypy.session.get('molotov.flash', None)
    cherrypy.session['molotov.flash'] = None
    log.debug ("get_flash () = %s" % str (ans))
    return ans

def url (mltv_url_path, mltv_url_params = None, **kw) :
    
    # Prefix path and params with mltv_url so **kw does not contains them
    
    if not isinstance (mltv_url_path, basestring) :
        mltv_url_path = "/".join (list (mltv_url_path))
    if mltv_url_path.startswith ("/") :
        app_root = "/".join (cherrypy.request.path_info.split ("/")[:-1])
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

def format_rst (data, format='html') :
    defaults = {'file_insertion_enabled': 0,
                'raw_enabled': 0,
                '_disable_config': 1}
    return publish_parts (data,
                          parser=molotov.rst_parser,
                          writer_name=format,
                          settings_overrides=defaults)

def has_user_cocktail () :
    for (cocktail, name, prefix) in molotov.running_cocktails :
        if cocktail == 'user' :
            return True
    return False

def cocktail_prefix (cocktail) :
    for (cock, name, prefix) in molotov.running_cocktails :
        if cock == cocktail :
            return prefix
    return None
