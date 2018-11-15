from __future__ import print_function

import sys
import os

from transforms import comments, io, keywords, structure, variables
import analysis
import util


def print_lines(lines):
    print('\n'.join(lines))

def pipeline(lines, base_dir=None):
    lines = comments.skip_comments(lines)
    lines = structure.join_backslash_lines(lines)

    lines = keywords.replace_raw(lines, base_dir or os.getcwd())
    lines = keywords.replace_tabs(lines)
    lines = keywords.replace_pass(lines)
    lines = keywords.replace_for_shorthand(lines)
    lines = keywords.replace_knowns(lines)
    lines = keywords.replace_blocks(lines)
    lines = keywords.replace_defs(lines)

    # replaces !, ?, ??, print, read, etc
    lines = io.replace_io_keywords(lines)

    # scopings is a per line scope of seen variables
    scopings = analysis.read_scopings(lines)
    lines = variables.add_auto_declarations(lines, scopings)
    lines = variables.add_destructuring(lines, scopings)

    lines = structure.add_parentheses(lines)
    lines = structure.add_semi_colons(lines)

    # add curly braces (from indentation) has to be last
    lines = structure.add_curly_braces(lines)

    return lines

OUTPUT_DIR=None

def process_file(fname):
    basedir, name = os.path.split(fname)
    with open(fname) as f:
        lines = f.readlines()

    lines = pipeline(lines, basedir)
    header = analysis.extract_header(lines)


    # TODO:
    # extract exports to fname.h
    # print("\n".join(exports))
    # print("/* END HEADER */")

    print_lines(lines)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: py++ <input file> <input file> -")
    else:
        if sys.argv[1] == '-':
            lines = sys.stdin.readlines()
            lines = pipeline(lines)
            print_lines(lines)
        else:
            for arg in sys.argv[1:]:
                process_file(arg)
