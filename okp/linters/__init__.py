from __future__ import print_function

#from .class_vars_without_this import lint_source_code
def lint_source_code(*args, **kwargs):
    pass

from .. import config

import os
def run(tmp_dir, args):
    if not config.LINT:
        return

    errored = False
    print("RUNNING LINT")
    for file in args.files:
        if lint_source_code(os.path.join(tmp_dir, file)):
            errored = True
    if errored:
        raise Exception("Code did not pass linter inspection, see messages above")

