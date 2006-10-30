# -*- coding: utf-8; -*-

from datetime import datetime
from sqlobject import *

class Revision (SQLObject) :
    "Revision of a wiki page."
    rev = UnicodeCol ()
    "Revision number in ``major.minor`` format."
    date = DateTimeCol ()
    "Date at which the revision was created."
    user = ForeignKey ('MolotovUser')
    "User who create the revision."
    ip = UnicodeCol ()
    "IP address who create the revision."
    comment = UnicodeCol ()
    "Optional comment describing the revision."
    data = UnicodeCol ()
    "Revision content."
    page = ForeignKey ('Page')
    "Page associated to the revision."

class Uploaded (SQLObject) :
    "Files uploaded on the server."
    filename = UnicodeCol (alternateID = True)
    "Filename as used for reference in the wiki."
    path = UnicodeCol ()
    "Path to the file on the filesystem."
    size = IntCol ()
    "File size."
    date = DateTimeCol ()
    "Date at which the file was uploaded."
    user = ForeignKey ('MolotovUser')
    "User who uploaded the file."
    ip = UnicodeCol ()
    "IP address who uploaded the file."
    references = RelatedJoin ('Page')
    "Pages which references the file."

class Page (SQLObject) :
    "A simple wiki page."
    pagename = UnicodeCol (alternateID = True)
    "Wiki page name."
    attached = RelatedJoin ('Uploaded')
    "Attached files."
    revisions = MultipleJoin ('Revision')
    "Wiki page revisions."

# Create the tables if needed
for cls in [Revision, Uploaded, Page] :
    cls.createTable (ifNotExists = True)
