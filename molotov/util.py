# -*- coding: utf-8; -*-

import re


email_re = re.compile(ur"[A-Za-z0-9\-_\.]+@[a-z0-9\-\.]+[a-z]{2,3}")

def valid_email(address):
    m = email_re.match(address)
    return m is not None and m.group(0) == address
