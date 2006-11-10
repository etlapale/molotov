# -*- coding: utf-8; -*-

import re
from datetime import datetime
import cherrypy
from sqlobject import SQLObjectNotFound
import molotov
from molotov import expose, flash, redirect, url
from molotov.model import MolotovUser, MolotovGroup

class Controller :
    "The user controller."

    box_ur = ur"[A-Za-z][A-Za-z0-9\-_\.]+"
    host_ur = ur"[A-Za-z0-9\-_\.]+\.[A-Za-z]{2,3}"
    email_re = re.compile (box_ur + "@" + host_ur + "$")
    user_re = re.compile (ur"[a-z0-9\-_\.]{3,30}$")

    def __init__ (self, config) :
        "Init the user Controller"
        pass

    @expose ()
    def login (self, username, password, from_url) :
        try:
            usr = MolotovUser.byName (username)
            if usr.password == password :
                flash ("Successful log-in!")
                cherrypy.session['molotov.user'] = usr
            else :
                flash ("Invalid login/pass pair")
        except SQLObjectNotFound:
            flash ("Invalid login/pass pair")
        raise cherrypy.HTTPRedirect (from_url)

    @expose ()
    def logout (self, from_url = "/") :
        cherrypy.session['molotov.user'] = None
        flash ("Logged out")
        raise cherrypy.HTTPRedirect (from_url)
    
    @expose ("molotov.cocktails.user.templates.register")
    def register (self, name = "", pass1 = "", pass2 = "", email = "") :
        "Display the registration formular."
        return dict (name = name, pass1 = pass1, pass2 = pass2, email = email)

    @expose ()
    def do_register (self, name, pass1, pass2, email) :
        "Register a Molotov user."

        # Check the username
        if self.user_re.match (name) is None :
            flash ("Bad username")
            return self.register (name, pass1, pass2, email)
        
        # Check the passwords
        # TODO: Check password complexity
        if pass1 != pass2 :
            flash ("Not the same passwords")
            return self.register (name, pass1, pass2, email)

        # Check the email address
        if self.email_re.match (email) is None :
            flash ("Bad email address")
            return self.register (name, pass1, pass2, email)

        # Check the username existence
        try:
            u = MolotovUser.byName (name)
            flash ("Username already existing")
            return self.register (name, pass1, pass2, email)
        except SQLObjectNotFound:
            pass

        # Register the user
        u = MolotovUser (name = name, password = pass1, email = email,
                         display_name = name, creation = datetime.now ())

        # If first user, then molotov admin
        if MolotovUser.select ().count () == 1 :
            adm_grp = MolotovGroup.byName ('molotov_admin')
            adm_grp.addMolotovUser (u)
            flash ("You are now registred as administrator")
        else :
            flash ("Registration successful")
        return self.register (name, pass1, pass2, email)

    @expose ("molotov.cocktails.user.templates.admin")
    def admin (self) :
        return dict (groups = MolotovGroup.select (orderBy='name'),
                     users = MolotovUser.select (orderBy='name'))

    @expose ()
    def add_member (self, group, user) :
        grp = MolotovGroup.byName (group)
        usr = MolotovUser.byName (user)
        grp.addMolotovUser (usr)
        flash ("User %s added to group %s" % (user, group))
        raise redirect ("/admin")

    @expose ()
    def remove_member (self, group, user) :
        grp = MolotovGroup.byName (group)
        usr = MolotovUser.byName (user)
        grp.removeMolotovUser (usr)
        flash ("User %s removed from %s" % (user, group))
        raise redirect ("/admin")

    @expose ()
    def create_group (self, group) :
        grp = MolotovGroup (name=group)
        flash ("Group %s created" % group)
        raise redirect ("/admin")

    @expose ()
    def delete_group (self, group) :
        grp = MolotovGroup.byName (group)
        if len (grp.users) :
            flash ("Could not destroy group %s (not empty)" % group)
        else :
            grp.destroySelf ()
            flash ("Group %s destroyed" % group)
        raise redirect ("/admin")
