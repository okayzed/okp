#!/usr/bin/env python
"""

What:

Locates instance variables that are accessed without the this-> prefix and
warns about them.

The idea is that all instance variables should be accessed or modified using
this-> so that it is apparent when they are instance variables vs local
variables.

"""

import sys
import os
import time

from ..util import debug
from .clanger import CI, get_idx

FUNC = None
CLASS = None
ASSIGNMENT_FUNCS = [CI.CursorKind.BINARY_OPERATOR, CI.CursorKind.CALL_EXPR]
REFERENCE_FUNCS = [ CI.CursorKind.MEMBER_REF_EXPR ]

HAS_LINT_ISSUES=False
def TOKENS(n):
    return [t.spelling for t in n.get_tokens()]

DEBUG_STMTS = False

import os
def get_path(node):
    ex = node.extent
    fname = ex.start.file
    fname = os.path.normpath(fname.name)

    return "%s|%s|" % (fname, ex.start.line)

def validate(node):
    # debug(ds, node.kind)
    try:
        fname = node.extent.start.file.name
        if fname.startswith("/usr"):
            return
    except:
        pass

    global HAS_LINT_ISSUES, CLASS, FUNC
    kind = node.kind
    if node.kind == CI.CursorKind.CLASS_DECL:
        CLASS = node.spelling
    elif node.kind == CI.CursorKind.CONSTRUCTOR:
        FUNC = node.spelling
    elif node.kind == CI.CursorKind.CXX_METHOD:
        FUNC = node.spelling
    elif node.kind in REFERENCE_FUNCS:
        tokens = TOKENS(node)
        if len(tokens) == 1:
            path = get_path(node)
            HAS_LINT_ISSUES = True
            debug("%s referencing '%s' in %s() of class %s without this->" %
                   (path, tokens[0], FUNC, CLASS))

    for c in node.get_children():
        validate(c)

def lint_source_code(s):
    args = []
    IDX = get_idx()
    tu = IDX.parse(s, args)
    for d in list(tu.diagnostics):
        debug("DIAGNOSTIC:", d)
    # debug('Translation unit:', tu.spelling)
    validate(tu.cursor)

    return HAS_LINT_ISSUES

def find_instance_variable_assignment(fname):
    return lint_source_code(fname)

if __name__ == "__main__":
    find_instance_variable_assignment(sys.argv[1])
