from __future__ import print_function

import re
import sys

def debug(*args):
    print(' '.join(map(str, args)), file=sys.stderr)

# splits a 'b c' d into [a, 'b c', d]
def split_quotes(line):
#    return filter(lambda w: w, re.split(' (?=\[)',line))

    in_quotes = 0
    quote_char = None
    quotes = [ "'", '"' ]

    prev = []
    args = []
    for c in line:
        if c in quotes:
            if in_quotes:
                if c == quote_char and (not prev or prev[-1] != '\\'):
                    in_quotes -= 1
                    args.append('"%s"' % (''.join(prev)))
                    prev = []
                else:
                    prev.append(c)
            elif not in_quotes:
                quote_char = c
                in_quotes += 1
                if prev:
                    args.append(''.join(prev))
                    prev = []
        else:
            if c == ' ' and not in_quotes:
                if prev:
                    args.append(''.join(prev))
                prev = []
            else:
                prev.append(c)

    if prev:
        args.append(''.join(prev))

    return args

def get_indent(line):
    indent = 0
    for c in line:
        if c == ' ':
            indent += 1
        elif c == '\t':
            indent += 8
        else:
            break

    return indent

def get_args(line):
    args = []
    nested = 0
    prev = []
    for c in line:
        if c == '(':
            nested += 1
        elif c == ')':
            nested -= 1

        prev.append(c)
        if c == ',' and nested == 0:
            args.append(''.join(prev))
            prev = []

    args.append(''.join(prev))

    return args

# from stack overflow somewhere
def comment_remover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

