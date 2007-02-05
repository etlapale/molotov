# -*- coding: utf-8; mode: python; -*-
# © 2006-2007, Émilien TLAPALE

import logging
import re
import smtplib
from subprocess import Popen, PIPE
from xml.dom.minidom import parse as xml_parse

from pgdb import connect
import cherrypy
from sqlobject import SQLObjectNotFound

import molotov
from molotov import expose, flash, identity
import molotov.captcha
import molotov.config
from molotov.captcha import create_captcha, check_captcha
from molotov.model import MolotovGroup
from molotov.cocktails.nxpanel.model import EmailAccount, EmailAlias
from molotov.util import valid_email
from molotov.xml import xml_node_get_text


log = logging.getLogger("molotov.cocktails.nxpanel")


class NXPanel:

    email_re = re.compile(ur"([a-zA-Z][A-Za-z0-9_\-\.]*)@([a-z\.\-]*)")

    def __init__(self, config):
        htxt = config.get("molotov.cocktails.nxpanel.email_hosts", "")
        domains = htxt.split(",")
        self.email_domains = map(lambda x : x.strip(), domains)
        self.pgdb_host = config.get("molotov.cocktails.nxpanel.pgdb_host")
        self.pgdb_db = config.get("molotov.cocktails.nxpanel.pgdb_db")
        self.pgdb_user = config.get("molotov.cocktails.nxpanel.pgdb_user")
        self.pgdb_pass = config.get("molotov.cocktails.nxpanel.pgdb_pass")
        self.log_email = config.get("molotov.cocktails.nxpanel.log_email")
        self.smtpd = config.get("molotov.smtpd")

    @expose("molotov.cocktails.nxpanel.templates.nxpanel")
    @identity.require(identity.valid_user)
    def index(self):
        user = cherrypy.session.get("molotov.user")
        if not identity.in_group("nxpanel_user")(user):
            return self.first_time()
        
        emails = EmailAccount.select(EmailAccount.q.userID == user.id)
        mailaliases = EmailAlias.select(EmailAlias.q.userID == user.id)
        return dict(emails=list(emails), mailaliases=list(mailaliases))

    @expose()
    def nxpanel(self):
        return self.index()

    @expose("molotov.cocktails.nxpanel.templates.first_time")
    @identity.require(identity.valid_user)
    def first_time(self, name="", address="", email=""):
        user = cherrypy.session.get("molotov.user")
        captcha = create_captcha()
        return dict(name=name, address=address, email=user.email,
                    captcha_src=captcha.src, captcha_id=captcha.captcha_id)

    @expose()
    @identity.require(identity.valid_user)
    def do_first_time(self, name, address, email, captcha_id, \
                      captcha_answer, chart=False):
        if not name or not address or not email or not chart:
            flash("Incomplete form")
            return self.first_time(name, address, email)
        if not check_captcha(captcha_id, captcha_answer):
            flash("Bad captcha answer, try again!")
            return self.first_time(name, address, email)
        
        # Mark as data provided
        user = cherrypy.session.get("molotov.user")
        try:
            grp = MolotovGroup.byName("nxpanel_user")
        except SQLObjectNotFound:
            grp = MolotovGroup(name="nxpanel_user")
        grp.addMolotovUser(user)

        # Send an email to save the data
        server = smtplib.SMTP(self.smtpd)
        msg = ["From: %s" % self.log_email,
               "Subject: [Next-Touch] Member personal data: %s" % user.name,
               "To: %s" % self.log_email,
               "",
               "User %s '%s'" % (user.name, user.display_name),
               "Email: %s" % email,
               "Address:",
               address]
        msg = ("\r\n".join(msg)).encode('latin-1')
        server.sendmail(self.log_email, self.log_email, msg)
        server.quit()
        
        flash("Information saved")
        return self.nxpanel()

    @expose("molotov.cocktails.nxpanel.templates.email")
    @identity.require(identity.in_group("nxpanel_user"))
    def email(self, address1="", address2="", pass1="", pass2=""):
        user = cherrypy.session.get("molotov.user")
        emails = EmailAccount.select(EmailAccount.q.userID == user.id)
        mailaliases = EmailAlias.select(EmailAlias.q.userID == user.id)
        return dict(emails=list(emails), mailaliases=list(mailaliases),
                    domains=self.email_domains, address1=address1,
                    address2=address2, pass1=pass1, pass2=pass2)

    @expose()
    @identity.require(identity.valid_user)
    def create_alias(self, alias, target):
        # Check for valid email address
        if not valid_email(alias) or not valid_email(target):
            flash("Invalid email address format")
            return self.email()
        
        # Create the SMTP alias
        p = Popen(["/var/mail/addmailuser", "alias", alias, target],
                  stdout=PIPE)
        (output,err) = p.communicate()
        log.debug(output)
        log.debug(err)

        # Bind the email account to the molotov user
        usr = cherrypy.session.get("molotov.user")
        email_account = EmailAlias(email=alias, target=target, user=usr)

        # Logging and notification
        server = smtplib.SMTP(self.smtpd)
        msg = ["From: %s" % self.log_email,
               "Subject: [Next-Touch] New e-mail alias: %s" % alias,
               "To: %s" % self.log_email,
               "",
               "Email alias created: %s => %s" % (alias, target)]
        msg = ("\r\n".join(msg)).encode('latin-1')
        server.sendmail(self.log_email, self.log_email, msg)
        server.quit()
        log.debug("Creating email account for %s" % alias)
        
        flash("E-mail alias created!")
        return self.nxpanel()

    @expose()
    @identity.require(identity.in_group("nxpanel_user"))
    def create_email(self, address1, address2, pass1, pass2):
        
        # Check parameters validity
        if address1 != address2:
            flash("Email addresses do not match!")
            return self.email(address1, address2, pass1, pass2)
        if pass1 != pass2:
            flash("Given passwords do not match!")
            return self.email(address1, address2, pass1, pass2)
        m = self.email_re.match(address1)
        if m is None or m.group(0) != address1:
            flash("Provided email address has got an invalid format.")
            return self.email(address1, address2, pass1, pass2)
        if m.group(2) not in self.email_domains:
            flash("Unknows domain name in email address.")
            return self.email(address1, address2, pass1, pass2)

        # Make sure the email address doesn't exists
        p = Popen(["grep", "-c", "--", address1,
                   "/etc/postfix/valias", "/etc/postfix/vmail"],
                  stdout=PIPE)
        output = p.communicate()[0]
        for line in output.splitlines():
            res = line.index(':')
            if line[res + 1] != "0":
                flash("E-mail address '%s' already exists!" % address1)
                return self.email(address1, address2, pass1, pass2)
        
        # Create the IMAP account
        db = connect(user=self.pgdb_user, password=self.pgdb_pass,
                     host=self.pgdb_host, database=self.pgdb_db)
        curs = db.cursor()
        mdir = "/home/vmail/domains/%s/%s" % (m.group(1), m.group(2))
        curs.execute("INSERT INTO courier " \
                     + "(id, clear, name, uid, gid, home, maildir) " \
                     + "VALUES (%s, %s, '', 1003, 410, '/home/vmail', %s)",
                     (address1, pass1, mdir))
        curs.close()
        db.commit()
        db.close()
        
        # Create the SMTP account
        p = Popen(["/var/mail/addmailuser", "account", m.group(1), m.group(2)],
                  stdout=PIPE)
        output = p.communicate()[0]

        # Bind the email account to the molotov user
        usr = cherrypy.session.get("molotov.user")
        email_account = EmailAccount(email=address1, user=usr)

        # Logging and notification
        server = smtplib.SMTP(self.smtpd)
        msg = """From: %s\r\nTo: %s\r
Subject: [Next-Touch] New email address: %s\r\n\r
E-mail address created: %s\r""" % (self.log_email, self.log_email, address1, address1)
        server.sendmail(self.log_email, self.log_email, msg)
        server.quit()
        log.debug("Creating email account for %s" % address1)
        
        flash("E-mail account created!")
        return self.nxpanel()

    @expose()
    @identity.require(identity.in_group("nxpanel_user"))
    def webaccount(self):
        return self.questions(cherrypy.config["molotov.prefix"] + "/share/cocktails/nxpanel/hosting-questions.xml", self.do_webaccount)

    @expose()
    @identity.require(identity.in_group("nxpanel_user"))
    def do_webaccount(self, answers, rejected=False):
        if not rejected:
            variables = cherrypy.session.get("molotov.questions.variables")
            server = smtplib.SMTP(self.smtpd)
            msg = ["From: %s" % self.log_email,
                   "Subject: [Next-Touch] Hosting request",
                   "To: %s" % self.log_email,
                   ""]
            for key, value in variables.iteritems():
                msg.append("%s: %s" % (key, value))
            msg = ("\r\n".join(msg)).encode('latin-1')
            server.sendmail(self.log_email, self.log_email, msg)
            server.quit()
            flash("Votre demande a bien été prise en compte ! " \
                  + "Vous recevrez une réponse par e-mail.")
        return self.nxpanel()

    def search_question(self, path, qid = None):
        dom = xml_parse(path)
        q = None
        if not qid:
            q = dom.getElementsByTagName("question")[0]
        else:
            for e in dom.getElementsByTagName("question"):
                if e.getAttribute("id") == qid:
                    q = e
                    break
            if q is None:
                raise Exception("Question node %s not found!" % qid)
        
        qtitle = xml_node_get_text(q.getElementsByTagName("title")[0])
        qtext = xml_node_get_text(q.getElementsByTagName("text")[0])

        return (dom, q, qtitle, qtext)
    
    @expose("molotov.templates.questions")
    def questions(self, path, callback, qid=None):

        if qid is None:
            cherrypy.session["molotov.questions.path"] = path
            cherrypy.session["molotov.questions.variables"] = dict()
            cherrypy.session["molotov.questions.callback"] = callback
        
        dom, q, qtitle, qtext = self.search_question(path, qid)

        xtags = {"checkbox" : "checkbox",
                 "field" : "textfield"}
        inputs = []
        submits = []
        xanswers = q.getElementsByTagName("answers")
        for answers in xanswers:
            next = answers.getAttribute("next")
            for node in answers.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    if node.tagName == "answer":
                        submits.append(xml_node_get_text(node))
                    elif node.tagName in xtags:
                        label = node.getAttribute("label")
                        content = xml_node_get_text(node).strip()
                        itype = xtags[node.tagName]
                        var = node.getAttribute("var")
                        inputs.append((label, itype, var, content))
                    elif node.tagName == "textarea":
                        label = node.getAttribute("label")
                        var = node.getAttribute("var")
                        inputs.append((label, "textarea", var, None))
                    else:
                        print "************ UNKNOWS TYPE: %s ************" \
                              % node.tagName
        if not submits:
            submits.append("OK")
        
        dom.unlink()
        del dom
        return dict(qtitle=qtitle, qtext=qtext, qid=qid,
                    inputs=inputs, submits=submits)

    @expose()
    def do_questions(self, qid, submit, **kargs):
        callback = cherrypy.session.get("molotov.questions.callback")
        variables = cherrypy.session.get("molotov.questions.variables")
        path = cherrypy.session["molotov.questions.path"]
        
        dom, q, qtitle, qtext = self.search_question(path, qid)

        # Search the next question
        xanswers = q.getElementsByTagName("answers")
        next = None
        for answers in xanswers:
            if not next:
                next = answers.getAttribute("next")
        submits = []
        answer = None
        answers = q.getElementsByTagName("answer")
        for ans in answers:
            if submit == xml_node_get_text(ans):
                answer = ans
                break
        if not next and answer is not None:
            next = answer.getAttribute("next")

        # Update the variables
        for key, val in kargs.iteritems():
            variables[key] = val
        if len (kargs):
            cherrypy.session["molotov.questions.variables"] = variables

        # We are done
        if not next:
            if answer is not None and answer.getAttribute("reject"):
                flash(answer.getAttribute("reject"))
                dom.unlink()
                del dom
                return callback(variables, True)
            else:
                return callback(variables, False)
            
        # Go to the next question
        return self.questions(path, callback, next)
