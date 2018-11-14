from __future__ import print_function

import sys

from util import *
from transforms.io import *
from transforms.structure import *
from transforms.variables import *
from transforms.keywords import *
from transforms.comments import *
from analysis import *


def pipeline(lines):
    lines = skip_comments(lines)
    lines = replace_tabs(lines)
    lines = replace_for_shorthand(lines)

    scopings = read_scopings(lines)
    lines = remove_knowns(lines)
    lines = remove_blocks(lines)
    lines = add_auto_declarations(lines, scopings)
    lines = add_destructuring(lines, scopings)
    lines = add_parentheses(lines)
    lines = imply_functions(lines)
    lines = replace_pass(lines)
    lines = add_io(lines)
    lines = add_semi_colons(lines)

    # indents have to be last???
    lines = translate_indents(lines)

    return lines

lines = sys.stdin.readlines()
lines = pipeline(lines)
print('\n'.join(lines))
