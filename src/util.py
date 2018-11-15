from __future__ import print_function

import re
import sys

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
        else:
            break

    return indent

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


def ptr_access(arg):
    return arg.find('->') != -1

def dot_access(arg):
    return arg.find('.') != -1

def array_access(arg):
    return arg.find('[') != -1

def visibility_line(line):
    return line.endswith('private:') or line.endswith('public:')

if __name__ == "__main__":
    smart_split("int main(int argc, char **argv)", [' '])
    smart_split('"foo bar baz", int main', [','])
    smart_split('int main(vector <pair<int, int>> a, b', [','])
    smart_split("int i, j", [','])
