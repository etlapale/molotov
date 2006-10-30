# -*- coding: utf-8; -*-
# Diffutils for Python

import logging
import difflib

log = logging.getLogger("next.controllers")


def patch (orig, pstr) :
    """
    Apply a patch to a text string and return the result.
    
    The patch is given in the ``diff`` classical format.
    """

    def readnum (str, pos) :
        "Read a number and return it as a string."
        ans = ""
        while str[pos].isdigit () :
            ans += str[pos]
            pos += 1
        return ans

    def readpair (str, pos) :
        "Read and return a line number or a line number pair."
        a = readnum (str, pos)
        pos += len (a)
        if str[pos] == ',' :
            pos += 1
            b = readnum (str, pos)
            return (int (a), int (b), len (a) + 1 + len (b))
        else :
            if not a.isdigit () :
                raise Exception ("Need a digit but got `%s`" % a)
            return (int (a), int (a), len (a))

    def newline (str, pos) :
        "Return the size of the newline string."
        if pos == len (str) :
            return 0
        elif str[pos] == '\r' :
            if str[pos + 1] == '\n' :
                return 2
            else :
                return 1
        elif str[pos] == '\n' :
            return 1
        else :
            raise Exception ('Expecting a newline but got `%s`' % str[pos])

    def lines (str, pos, n) :
        "Return `n` lines from the string `str`."
        log.debug ("lines (%d)" % n)
        i = pos
        count = 0
        sz = len (str)
        while count < n and i < sz :
            if str[i] == '\n' :
                count += 1
            i += 1
        log.debug ("LINES: %s" % str[pos:i])
        return str[pos:i]

    def check_lines (o, p) :
        "Check patch lines agains original text."

        while pstr[p:p + 3] != '---' :
            
            # Skip first '>'
            if pstr[p:p + 2] != '< ' :
                log.error ('Expecting `< ` instead of `%s` at %d' \
                           % (pstr[p:p+2], p))
                raise Exception ('Expecting `< `')
            p += 2
        
            # Compare a single line
            e = pstr.find ('\n', p)
            if e == -1 :
                raise Exception ('Expecting newline')
            if pstr[e - 1] == '\r' :
                e -= 1
            sz = e - p
            
            if pstr[p:e] != orig[o:o + sz] :
                log.debug ("HUNK failed: `%s` != `%s`" \
                           % (pstr[p:e], orig[o:o + sz]))
                raise Exception ('Hunk checking failed at %d-%d' % (o, p))
            p += sz
            o += sz
            p += newline (pstr, p)
            o += newline (orig, o)

        p += 3
        p += newline (pstr, p)
            
        return (o, p)

    def patched_lines (p) :
        "Return patched lines."

        ans = ''
        
        while pstr[p:p + 2] == '> ' :
            
            p += 2
            
            # Compare a single line
            e = pstr.find ('\n', p)
            if e == -1 :
                raise Exception ('Expecting newline')
            if pstr[e - 1] == '\r' :
                e -= 1
            sz = e - p

            ans += pstr[p:e]
            p += sz
            nl = newline (pstr, p)
            ans += pstr[p:p + nl]
            p += nl
            
        return (ans, p)
    
    ans = ""
    o = 0
    p = 0
    line = 1

    while p < len (pstr) :
        log.debug ("We are at line %d" % line)
        log.debug ("Searching hunk at %d in %d" % (p, len (pstr)))
        
        # Read the hunk informations
        (src_a, src_b, sz) = readpair (pstr, p)
        p += sz
        cmd = pstr[p]
        p += 1
        (dst_a, dst_b, sz) = readpair (pstr, p)
        p += sz
        p += newline (pstr, p)
        log.debug ("HUNK: %d,%d%s%d,%d" % (src_a, src_b, cmd, dst_a, dst_b))
    
        # Process the previous lines
        log.debug ("Processing prev lines: %d-%d" % (line, src_a))
        ln = lines (orig, o, src_a - line)
        ans += ln
        o += len (ln)
    
        # Replace command (c)
        if cmd == 'c' :
            (o, p) = check_lines (o, p)
            (s, p) = patched_lines (p)
            ans += s
        # Append command (a)
        elif cmd == 'a' :
            if src_a != src_b :
                raise Exception ('Strange append command (range: `%d,%d`)' \
                                 % (src_a, src_b))
            # Process current line
            ln = lines (orig, o, 1)
            ans += ln
            o += len (ln)
            # Append the lines in the patch
            (s, p) = patched_lines (p)
            ans += s
        # Unknown command
        else :
            raise Exception ("Unknown patch command: `%s`" % cmd)
        line = src_b + 1

    # Process the trailing lines
    ans += orig[o:]
    
    return ans

def diff_table (a, b) :
    "Return an HTML table comparing, side by side, two texts."

    def lines (k) :
        if len (k) == 0 :
            return u" "
        ans = ""
        for x in k :
            ans += x + "<br/>\n"
        return ans
    
    def update (i, j) :
        if len (i) or len (j) :
            if not len (i) :
                return '<tr><td>%s</td><td class="added">%s</td></tr>\n' % (lines (i), lines (j))
            elif not len (j) :
                return '<tr><td class="deleted">%s</td><td>%s</td></tr>\n' % (lines (i), lines (j))
            else :
                return '<tr><td class="deleted">%s</td><td class="added">%s</td></tr>\n' % (lines (i), lines (j))
        else :
            return ""
        
    diffs = difflib.ndiff (a.splitlines (), b.splitlines ())
    table = u'''
    <table class="diff">
      <tr><th>Texte supprimmé</th><th>Texte ajouté</th></tr>
    '''
    i, j = [], []
    for diff in diffs :
        if diff[0] == ' ' :
            table += update (i, j)
            i = []
            j = []
        elif diff[0] == '?' :
            pass
        elif diff[0] == '-' :
            i.append (diff)
        elif diff[0] == '+' :
            j.append (diff)
        else :
            raise Exception ("Unknown diff prefix: `%s`" % diff[0:2])
    table += update (i, j)
    table += '</table>\n'
    return table
