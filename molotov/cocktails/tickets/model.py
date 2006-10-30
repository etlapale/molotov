# -*- coding: utf-8; -*-

from datetime import datetime
from sqlobject import DateTimeCol, ForeignKey, MultipleJoin, \
     IntCol, RelatedJoin, SQLObject, UnicodeCol
from molotov.model import MolotovUser

class TicketType :
    defect, task, enhancement = range (3)
    strings = ["défaut", "tâche", "amélioration"]

class TicketPriority :
    lowest, low, normal, high, highest = range (5)
    strings = ["la plus basse", "basse", "normale", "haute", "la plus haute"]

class TicketStatus :
    new, assigned, closed, reopened = range (4)
    strings = ["nouveau", "assigné", "fermé", "réouvert"]

class Ticket (SQLObject) :
    title = UnicodeCol ()
    creation_date = DateTimeCol ()
    change_date = DateTimeCol ()
    reporter = ForeignKey ('MolotovUser')
    ticket_type = IntCol ()
    ticket_priority = IntCol ()
    owner = ForeignKey ('MolotovUser')
    status = IntCol ()
    comments = MultipleJoin ('TicketComment')

class TicketComment (SQLObject) :
    data = UnicodeCol ()
    creation_date = DateTimeCol ()
    user = ForeignKey ('MolotovUser')
    ticket = ForeignKey ('Ticket')

# Create the tables if needed
for cls in [Ticket, TicketComment] :
    cls.createTable (ifNotExists = True)
