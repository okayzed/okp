from __future__ import print_function
from .transforms import comments, io, keywords, structure, variables
from . import analysis
from . import util

import os

ASSERT_SOURCE_MAP = True


def pipeline(lines, base_dir=None, add_source_map=True, fname=None):
    lines = comments.skip_comments(lines)
    # all functions modifying tlines can change the line numbers
    # of the source code by removing or adding new lines
    tlines = [(i+1, line) for i, line in enumerate(lines)]
    tlines = structure.join_backslash_lines(tlines)
    tlines = structure.join_open_bracketed_lines(tlines)
    tlines = structure.join_percent_bracketed_lines(tlines)
    lines = [line for line_no, line in tlines]
    line_nos = [line_no for line_no, _ in tlines]
    num_lines = len(lines)

    def runner(lines):
        def run(step, *args):
            new_lines = step(lines, *args)
            if add_source_map and ASSERT_SOURCE_MAP:
                assert(len(new_lines) == num_lines)

            del lines[:]
            lines.extend(new_lines)
            return lines

        return run

    run = runner(lines)
    run(structure.add_preceding_ignore_chars)
    run(keywords.replace_raw, base_dir or os.getcwd())
    run(keywords.replace_tabs)
    run(keywords.replace_pass)
    run(keywords.replace_for_shorthand)
    run(keywords.replace_blocks)
    run(keywords.replace_defs)
    run(keywords.replace_self)

    # replaces !, ?, ??, print, read, etc
    run(io.replace_io_keywords)
    # scopings is a per line scope of seen variables
    run(variables.replace_walrus_operator)
    run(variables.add_auto_declarations)
    # known keyword replacement has to happen after auto declarations
    run(keywords.replace_knowns)
    run(structure.add_parentheses)
    run(structure.add_trailing_semicolons)
    # add curly braces (from indentation) has to be last
    run(structure.add_curly_braces)  # can change line numbers
    # TODO: decide on whether to remove from generated code or not
    run(structure.remove_preceding_ignore_chars)

    requires = analysis.guess_required_files(lines)
    lines = requires + lines

    if add_source_map and ASSERT_SOURCE_MAP:
        line_nos = [0]*len(requires)+line_nos
        assert(len(line_nos) == len(lines))

        tlines = zip(line_nos, lines)
        new_lines = []
        cur_line = 0
        # GCC / MSVCC directive for #line is:
        # #line <line> "<file>"
        # we only label lines if their labeling is off from what
        # we expect so we don't bloat our output files up
        for line_no, line in tlines:
            if cur_line != line_no:
                new_lines.append("#line %s" % line_no)
            new_lines.append(line)
            cur_line = line_no
            cur_line += 1

        if fname:
            new_lines = ['#line 0 "%s"' % fname] + new_lines
        return new_lines
    else:
        return lines
