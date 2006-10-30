# -*- coding: utf-8; -*-
# Controller for the Control Panel

import cherrypy
from cherrypy import expose
#from sqlobject import SQLObjectNotFound

#from next.model import User

import smtplib

class ControlPanel :
    "Control Panel controller."    

    def __init__ (self, config) :
        pass

    @expose ("next.templates.contact")
    def contact (self, username = None, name = None, email = None,
                 message = None) :

        # Send the message
        if (message) :
            subject = u"[Next-Touch] Formulaire de contact"
            header = u"From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" \
                     % ('neil@next-touch.com', 'neil@next-touch.com',
                        subject)
            body = u"""Utilisateur : %s
            Nom : %s
            E-mail : %s

            %s""" % (username, name, email, message)

            server = smtplib.SMTP ('localhost')
            server.sendmail ('neil@next-touch.com', 'neil@next-touch.com',
                             header + body)
            server.quit ()
            flash ('Message envoyé')
            raise redirect (url ('/'))
        
        return dict (page = None,
                     user = cherrypy.session.get ('user', None),
                     history = cherrypy.session.get ('history', []))

    @expose ()
    def login (self, username, password) :
        "Authenticate a user."

        failure_str = "Invalid login/password pair."
        
        # Search for the user
        user = None
        try :
            user = User.byUsername (username)
        except SQLObjectNotFound :
            flash (failure_str)
            raise redirect (url ("/"))

        # Check the password
        if password != user.password :
            flash (failure_str)
            raise redirect (url ("/"))
        
        cherrypy.session['user'] = user
        flash ("Logged in as %s." % user.username)
        raise redirect (url ("/"))

    @expose ()
    def logout (self) :
        "Disconnect an authenticated user."

        cherrypy.session['user'] = None
        flash ("Session terminated.")
        raise redirect (url ("/"))
    
    @expose ("next.templates.register")
    def register (self) :
        "Register as a control panel user."
        return dict (page = None,
                     user = cherrypy.session.get ('user', None),
                     history = cherrypy.session.get ('history', []))

    @expose ()
    def doregister (self, username, realname, pwd1, pwd2) :
        "Try the registration."

        reg = url ("register")
        
        # Check the passwords are the same
        if pwd1 != pwd2 :
            flash ("Not the same passwords.")
            raise redirect (reg)

        # Check the user does not exists
        try :
            user = User.byUsername (username)
            flash ("User already exists.")
            raise redirect (reg)
        except SQLObjectNotFound :
            pass

        # Do the registration
        user = User (username = username, password = pwd1)
        
        flash ("User created.")
        raise redirect (url ("/"))

    @expose ("next.templates.email")
    def email (self) :
        "E-mail accounts manager."
        
        return dict (page = None,
                     user = cherrypy.session.get ('user', None),
                     history = cherrypy.session.get ('history', []))
