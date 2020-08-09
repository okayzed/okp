#!/usr/bin/env python
"""

What:

Locates instance variables that are accessed without the this-> prefix and
warns about them.

The idea is that all instance variables should be accessed or modified using
this-> so that it is apparent when they are instance variables vs local
variables.

How it works:

* uses clang's python API to find all classes in the given file to parse.
* parses each class, adding field declarations to the classes' scope.
* go through all nodes inside the class and if it is a BINARY_OPERATOR or CALL_EXPR,
check for assignment and whether the variable is in class scope or not.
* also check for MEMBER_REF_EXPR

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

    return "%s:%s" % (fname, ex.start.line)

def validate_class_func_access(node, scope, depth=0):
    global FUNC
    global HAS_LINT_ISSUES

    ds = " " * depth
    vars = []
    if DEBUG_STMTS:
        debug(ds, str(node.kind), TOKENS(node))
        if node.kind == CI.CursorKind.COMPOUND_STMT:
            for c in node.walk_preorder():
                debug("C", c.kind, TOKENS(c))

    if node.kind in REFERENCE_FUNCS:
        tokens = TOKENS(node)
        if len(tokens) == 1 and tokens[0] in scope:
            ex = node.extent
            path = get_path(node)
            HAS_LINT_ISSUES = True
            debug("%s|referencing '%s' in %s() of class %s without this->" %
                   (path, tokens[0], FUNC, CLASS))

    if node.kind in ASSIGNMENT_FUNCS:
        tokens = TOKENS(node)
        if len(tokens) >= 3:
            for i, op in enumerate(tokens):
                if i == 0 or op != "=":
                    continue
                name = tokens[i-1]
                if i > 2:
                    if tokens[i-2] == "->" or tokens[i-2] == ".":
                        continue
                    skip = False
                    for c in tokens[i-2]:
                        if c.isalpha:
                            skip = True
                            break
                    if skip:
                        continue

                if name in scope:
                    path = get_path(node)
                    HAS_LINT_ISSUES = True
                    debug("%s|assigning to '%s' in %s() of class %s without this->" %
                         (path, tokens[0], FUNC, CLASS))
                    break

    start = time.time()
    if node.kind == CI.CursorKind.CONSTRUCTOR:
        FUNC = node.spelling
#        debug("  ", FUNC)
    elif node.kind == CI.CursorKind.CXX_METHOD:
        FUNC = node.spelling
#        debug("  ", FUNC)

    for c in node.get_children():
        validate_class_func_access(c, scope, depth+1)

    if node.spelling.strip() and time.time() - start > 0.5:
        debug("  ", node.spelling, "TOOK", time.time() - start)

    return vars

def validate_class_var_access(node, depth=0):
    global CLASS
    CLASS = node.spelling
    scope = {}
    fname = node.extent.start.file.name
    if fname.startswith("/usr"):
      return


    for c in node.get_children():
        if c.kind == CI.CursorKind.FIELD_DECL:
            tokens = TOKENS(c)
            if tokens:
              scope[tokens[-1]] = 1

    for c in node.get_children():
        validate_class_func_access(c, scope)


def find_classes(node, out, depth=0):
    ds = depth * " "
    # debug(ds, node.kind)
    try:
      if node.kind == CI.CursorKind.CLASS_DECL:
          out.append(node)
    except:
      pass

    for c in node.get_children():
        find_classes(c, out, depth=depth+1)
    return out

def lint_source_code(s):
    args = []
    IDX = get_idx()
    tu = IDX.parse(s, args)
    for d in list(tu.diagnostics):
        debug("DIAGNOSTIC:", d)
    # debug('Translation unit:', tu.spelling)
    classes = find_classes(tu.cursor, [])

    for class_ in classes:
#        debug("VALIDATING CLASS", class_.spelling)
        validate_class_var_access(class_)
    return HAS_LINT_ISSUES

def find_instance_variable_assignment(fname):
    return lint_source_code(fname)

if __name__ == "__main__":
    find_instance_variable_assignment(sys.argv[1])
