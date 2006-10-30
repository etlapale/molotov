# -*- coding: utf-8; -*-
# Tickets manager

from datetime import datetime
import cherrypy
from sqlobject import SQLObjectNotFound
import molotov
from molotov import expose, flash, redirect
from molotov.model import MolotovUser
from molotov.cocktails.tickets.model \
     import Ticket, TicketComment, TicketPriority, TicketStatus, TicketType

class Tickets :

    def __init__ (self, config) :
        "Init the Tickets controller."
        pass

    @expose ("molotov.cocktails.tickets.templates.view")
    def index (self) :
        "Display a list of all tickets."
        tickets = Ticket.select (orderBy = 'change_date')
        return dict (tickets = list (tickets))

    @expose ("molotov.cocktails.tickets.templates.ticket")
    def ticket (self, ticket) :
        try :
            t = Ticket.get (ticket)
        except SQLObjectNotFound :
            flash ("Ticket #%s not found" % ticket)
            redirect ("/")
        return dict (ticket = t,
                     priority = TicketPriority.strings[t.ticket_priority],
                     type = TicketType.strings[t.ticket_type],
                     status = TicketStatus.strings[t.status])

    @expose ("molotov.cocktails.tickets.templates.new")
    def new (self, title="", type=0, priority=2, owner="", comment="") :
        "Create a new ticket."

        # Check that we are logged
        if cherrypy.session.get ('molotov.user', None) is None :
            flash ("Please log in to report a bug.")
            redirect ("/")

        types = {0 : "bogue",
                 1 : "tâche",
                 2 : "amélioration"}
        priorities = {0 : "la plus basse",
                      1 : "basse",
                      2 : "normale",
                      3 : "haute",
                      4 : "la plus haute"}
        
        return dict (types=types, priorities=priorities,
                     title=title, type=int (type), priority=int (priority),
                     owner=owner, comment=comment)

    @expose ()
    def do_new (self, title, type, priority, owner, comment) :

        # Get and check the user
        usr = cherrypy.session.get ('molotov.user', None)
        if usr is None :
            flash ("Please log in to report a bug.")
            redirect ("/")

        # Verify the owner
        owner = owner.strip ()
        if len (owner) :
            try :
                owner = MolotovUser.byName (owner.strip ())
            except SQLObjectNotFound :
                flash ("Unknown user as ticket owner.")
                redirect ("/new", title=title, type=type, priority=priority,
                          owner=owner, comment=comment)
            status = TicketStatus.assigned
        else :
            owner = None
            status = TicketStatus.new

        # Check type and priority
        type = int (type)
        priority = int (priority)
        
        # Create a new ticket
        now = datetime.now ()
        t = Ticket (title = title, creation_date = now, change_date = now,
                    reporter = usr, ticket_type = type,
                    ticket_priority = priority, owner = owner,
                    status = status)

        # Check the comment
        comment = comment.strip ()
        if len (comment) :
            comm = TicketComment (data = comment,
                                  creation_date = datetime.now (),
                                  user = usr, ticket = t)
        
        flash ("New ticket created.")
        redirect ("/")
