import sys
import os
import clang.cindex as CI
import time

from ..util import debug

IDX = None
DEBUG_CLANG_SO=False
def detect_clang_path():
    global IDX
    clang_paths = os.popen("locate libclang.so").read().split('\n')
    for path in clang_paths:
        CI.Config.set_library_file(path)
        try:
            IDX = CI.Index.create()
            if DEBUG_CLANG_SO:
                debug("Set clang .so to", path)
            break
        except (Exception, e):
            continue

def get_idx():
    global IDX
    try:
        IDX = CI.Index.create()
    except:
        if DEBUG_CLANG_SO:
            debug("Couldn't create clang index, looking for .so files")
        detect_clang_path()
    return IDX
