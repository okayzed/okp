from __future__ import print_function
from .transforms import comments, io, keywords, structure, variables
from . import analysis
from . import util

import os


def pipeline(lines, base_dir=None, add_source_map=True):
    lines = comments.skip_comments(lines) # can change line numbers
    tlines = [(i+1, line) for i,line in enumerate(lines)]
    tlines = structure.join_backslash_lines(tlines) # can change tline numbers
    tlines = structure.join_open_bracketed_lines(tlines) # can change tline numbers
    tlines = structure.join_percent_bracketed_lines(tlines) # can change tline  numbers
    lines = [line for line_no,line in tlines]
    line_nos = [line_no for line_no,_ in tlines]
    num_lines = len(lines)

    lines = structure.add_preceding_ignore_chars(lines) # replaces ```
    if add_source_map:
      assert(len(lines) == num_lines)

    lines = keywords.replace_raw(lines, base_dir or os.getcwd())
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = keywords.replace_tabs(lines)
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = keywords.replace_pass(lines)
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = keywords.replace_for_shorthand(lines)
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = keywords.replace_blocks(lines)
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = keywords.replace_defs(lines)
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = keywords.replace_self(lines)
    if add_source_map:
      assert(len(lines) == num_lines)

    # replaces !, ?, ??, print, read, etc
    lines = io.replace_io_keywords(lines)
    if add_source_map:
      assert(len(lines) == num_lines)

    # scopings is a per line scope of seen variables
    lines = variables.replace_walrus_operator(lines)
    if add_source_map:
      assert(len(lines) == num_lines)
    lines = variables.add_auto_declarations(lines) # can change line numbers
    if add_source_map:
      assert(len(lines) == num_lines)

    # known keyword replacement has to happen after auto declarations
    lines = keywords.replace_knowns(lines)
    if add_source_map:
      assert(len(lines) == num_lines)

    lines = structure.add_parentheses(lines)
    if add_source_map:
      assert(len(lines) == num_lines)

    lines = structure.add_trailing_semicolons(lines)
    if add_source_map:
      assert(len(lines) == num_lines)

    # add curly braces (from indentation) has to be last
    lines = structure.add_curly_braces(lines)  # can change line numbers
    if add_source_map:
      assert(len(lines) == num_lines)

    # TODO: decide on whether to remove from generated code or not
    lines = structure.remove_preceding_ignore_chars(lines)
    if add_source_map:
      assert(len(lines) == num_lines)

    requires = analysis.guess_required_files(lines)
    lines = requires + lines

    if add_source_map:
        line_nos = [0]*len(requires)+line_nos
        assert(len(line_nos) == len(lines))
        tlines = zip(line_nos, lines)
        # #line <line> <file>
        return ["#line {}\n{}".format(ln, line) for ln,line in tlines]
    else:
        return lines
