# -*- coding: utf-8; -*-

from datetime import datetime
from sqlobject import DateTimeCol, ForeignKey, RelatedJoin, SQLObject, \
     SQLObjectNotFound, UnicodeCol
from molotov.model import MolotovUser


class EmailAccount(SQLObject) :
    email = UnicodeCol(alternateID=True)
    user = ForeignKey('MolotovUser')

class EmailAlias(SQLObject):
    email = UnicodeCol(alternateID=True)
    target = UnicodeCol()
    user = ForeignKey('MolotovUser')

# Create the tables if needed
for cls in [EmailAccount, EmailAlias]:
    cls.createTable(ifNotExists=True)
