# -*- coding: utf-8; -*-

from datetime import datetime
from sqlobject import DateTimeCol, RelatedJoin, SQLObject, SQLObjectNotFound, UnicodeCol

class MolotovUser (SQLObject) :
    "A Molotov user."
    name = UnicodeCol (alternateID = True)
    display_name = UnicodeCol ()
    password = UnicodeCol ()
    email = UnicodeCol ()
    "User email address."
    creation = DateTimeCol ()
    "Date at which the user was created."
    groups = RelatedJoin ('MolotovGroup')
    "Groups to which the user is affiliated."

class MolotovGroup (SQLObject) :
    "A Molotov user group."
    name = UnicodeCol (alternateID = True)
    "The group name."
    users = RelatedJoin ('MolotovUser')
    "Users affiliated to the group."

class Captcha(SQLObject):
    captcha_id = UnicodeCol(alternateID=True)
    text = UnicodeCol()
    src = UnicodeCol()
    creation = DateTimeCol()

# Create the tables if needed
for cls in [MolotovUser, MolotovGroup, Captcha] :
    cls.createTable (ifNotExists = True)

# Create the `molotov_admin` group if needed
try :
    adm_grp = MolotovGroup.byName ('molotov_admin')
except SQLObjectNotFound :
    adm_grp = MolotovGroup (name = 'molotov_admin')
