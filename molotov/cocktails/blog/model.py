# -*- coding: utf-8; mode: python; -*-

from datetime import datetime
from sqlobject import DateTimeCol, ForeignKey, IntCol, MultipleJoin, \
     RelatedJoin, SQLObject, UnicodeCol
from molotov.model import MolotovUser

class Billet (SQLObject) :
    title = UnicodeCol ()
    creation_date = DateTimeCol ()
    user = ForeignKey ('MolotovUser')
    data = UnicodeCol ()
    comments = MultipleJoin ('BilletComment')

class BilletComment (SQLObject) :
    data = UnicodeCol ()
    creation_date = DateTimeCol ()
    user = ForeignKey ('MolotovUser')
    billet = ForeignKey ('Billet')

for cls in [Billet, BilletComment] :
    cls.createTable (ifNotExists = True)
