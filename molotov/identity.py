#! /usr/bin/env python
# -*- coding: utf-8; -*-

import cherrypy
import molotov


def check (identity_constraint) :
    user = cherrypy.session.get ('molotov.user', None)
    if (user is None) or (not identity_constraint (user)) :
        raise cherrypy.HTTPRedirect ("/user/forbidden")

def require (identity_constraint) :
    def require_decorator (func) :
        def require_call (*args, **kw) :
            check (identity_constraint)
            # Call the decorated function
            return func (*args, **kw)
        return require_call
    return require_decorator

def in_group (group_name) :
    def func (user) :
        for group in user.groups :
            if group.name == group_name :
                return True
        return False
    return func
