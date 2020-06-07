from .transforms import comments, io, keywords, structure, variables
from . import analysis
from . import util

import os

def pipeline(lines, base_dir=None):
    lines = comments.skip_comments(lines)
    lines = structure.join_backslash_lines(lines)
    lines = structure.add_preceding_ignore_chars(lines)

    lines = keywords.replace_raw(lines, base_dir or os.getcwd())
    lines = keywords.replace_tabs(lines)
    lines = keywords.replace_pass(lines)
    lines = keywords.replace_for_shorthand(lines)
    lines = keywords.replace_blocks(lines)
    lines = keywords.replace_defs(lines)
    lines = keywords.replace_self(lines)

    # replaces !, ?, ??, print, read, etc
    lines = io.replace_io_keywords(lines)

    # scopings is a per line scope of seen variables
    scopings = analysis.read_scopings(lines)
    lines = variables.add_auto_declarations(lines, scopings)
    lines = variables.add_destructuring(lines, scopings)

    # known keyword replacement has to happen after auto declarations
    lines = keywords.replace_knowns(lines)

    lines = structure.add_parentheses(lines)
    lines = structure.add_trailing_semicolons(lines)

    # add curly braces (from indentation) has to be last
    lines = structure.add_curly_braces(lines)

    # TODO: decide on whether to remove from generated code or not
    lines = structure.remove_preceding_ignore_chars(lines)

    requires = analysis.guess_required_files(lines)

    lines = requires + lines
    return lines
