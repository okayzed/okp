from __future__ import print_function

import re
import sys

from . import config

IGNORE_CHAR = '$'



def verbose(*args):
    if config.VERBOSE:
        debug(*args)

def debug(*args):
    print(' '.join(map(str, args)), file=sys.stderr)

def find_matching(line, open, close, start):
    j = start
    count = 1
    while j < len(line):
        if line[j] == close:
            count -= 1
            if count == 0:
                return line[start-1:j+1], j+1

        if line[j] == open:
            count += 1

        j += 1

    return line[start-1], start

# we split with split chars
# anything inside [], (), {} and <> are kept together
# anything inside "" or '' is kept together
# we pass a separator, like ' ' or ',' and we get back the inner pieces
def smart_split(line, split_chars=[], keep_splitters=False):
    split = []
    prev = []


    i = 0
    while i < len(line):
        c = line[i]
        i += 1

        if c in split_chars:
            if prev:
                split.append(''.join(prev))
                prev = []

            if keep_splitters:
                split.append(c)

        elif c == '"':
            p, i = find_matching(line, '"', c, i)
            prev.append(p)
        elif c == '<':
            p, i = find_matching(line, '<', '>', i)
            prev.append(p)
        elif c == '(':
            p, i = find_matching(line, '(', ')', i)
            prev.append(p)
        else:
            prev.append(c)

    if prev:
        split.append(''.join(prev))

    # debug("SPLIT", line, "INTO", split, "USING", split_chars)
    return split


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
        elif c == IGNORE_CHAR:
            continue
        else:
            break

    return indent

def ptr_access(arg):
    return arg.find('->') != -1

def dot_access(arg):
    return arg.find('.') != -1

def array_access(arg):
    return arg.find('[') != -1

def visibility_line(line):
    return line.endswith('private:') or line.endswith('public:')

def hash_line(line):
    cline = line.strip()
    return cline and cline[0] == '#'

def is_def(line):
    return line.strip().find("def ") != -1

def is_struct(line):
    return (line.find(" struct ") != -1 or line.startswith("struct ")) and line.endswith('{')

def is_class(line):
    return line.strip().startswith("class ")

def line_is_include(line):
    return line.startswith("#include")

def line_is_using(line):
    return line.startswith("using ");

def line_is_template(line):
    line = line.strip().lstrip(IGNORE_CHAR).strip()
    return line.startswith("template<") or line.startswith("template <")

def case_statement(line):
    cline= line.strip()
    # default must have a : always
    return cline.startswith('case ')  or cline.startswith("default:")

def strip_outer_parens(s):
    if s[0] == '(' and s[-1] == ')':
        return s[1:-1]

    return s

def ignore_line(s, nl):
    sline = s.strip()
    if sline and sline[0] == IGNORE_CHAR:
        nl.append(s)
        return True

    return False

def extract_until_close(lines, i):
    count = 0
    while i < len(lines):
        line = lines[i]
        for c in line:
            if c == '{':
                count += 1
            if c == '}':
                count -= 1

        i += 1
        if count == 0:
            return i
if __name__ == "__main__":
    smart_split("int main(int argc, char **argv)", [' '])
    smart_split('"foo bar baz", int main', [','])
    smart_split('int main(vector <pair<int, int>> a, b', [','])
    smart_split("int i, j", [','])
