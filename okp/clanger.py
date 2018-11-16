# WARNING: THIS FILE IS DEPRECATED
# clanger is too slow (adds hundreds of ms per file). trying out custom code
# to recognize identifiers. the code is in id_recognizer.py

import clang.cindex
import os

from .util import *
IDX = None
def detect_clang_path():
    global IDX
    clang_paths = os.popen("locate libclang.so").read().split('\n')
    for path in clang_paths:
        clang.cindex.Config.set_library_file(path)
        try:
            IDX = clang.cindex.Index.create()
            debug("Set clang .so to", path)
            break
        except:
            continue

try:
    IDX = clang.cindex.Index.create()
except:
    debug("Couldn't create clang index, looking for .so files")
    detect_clang_path()

TokenKind = clang.cindex.TokenKind


# TODO: build a simple parser here that finds identifiers
# foo.obj.baz = '12'; should return [foo, '.', obj, '.', baz]
def parse_line(line):
    tu = IDX.parse('tmp.cpp', args=['-std=c++11'],
                    unsaved_files=[('tmp.cpp', line)],  options=0)
    for t in tu.get_tokens(extent=tu.cursor.extent):
        yield t


# we do some touchups to remove something like foo.bar.baz
# into only foo
def add_identifiers(line, scope):
    toks = parse_line(line)
    new = []

    new_toks = []
    toks = list(toks)
    while toks:
        t = toks.pop()
        new_toks.append(t)

        if toks:
            nt = toks[-1]
            if nt.spelling == '.' or nt.spelling == '->':
                toks.pop()
                new_toks.pop()


    for t in new_toks:
        if t.kind == TokenKind.IDENTIFIER:
            if t.spelling not in scope:
                new.append(t.spelling)
                scope[t.spelling] = 1

    return new

if __name__ == "__main__":
    scope = {}
    add_identifiers("vector<int> n", scope)
    add_identifiers("foo.bar. baz", scope)
