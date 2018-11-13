from __future__ import print_function

import sys
import re
import shlex

# cpy transpiler?
#   x indentation
#   x return multiple values
#   x semi-colon optional
#   x destructured assignment
#   x shorthand for printing

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
                if c == quote_char and prev[-1] != '\\':
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

def replace_double_semicolons(lines):
    new_lines = []
    for line in lines:
        while line.endswith(';;'):
            line = line[:-1]
        new_lines.append(line)

    return new_lines


def add_semi_colons(lines):
    new_lines = []
    indents = []
    for line in lines:
        indents.append(get_indent(line))

    indents.append(0)

    for i, line in enumerate(lines):
        line = line.rstrip();

        if not line or line[0] == '#':
            new_lines.append(line)
            continue

        if indents[i] < indents[i+1]:
            new_lines.append(line)
            continue

        if line[-1] != '\\':
            line += ';'

        new_lines.append(line)

    return new_lines


def translate_indents(lines):
    indent_level = 0

    indented_lines = []
    indented = 0
    for line in lines:
        line = line.rstrip('\n')
        indent = get_indent(line)
        if not line:
            continue

        if indent_level > indent:
            indented_lines[-1] += ' }'
            indented -= 1
            indent_level = indent
            indented_lines.append('')

        if indent_level < indent:
            indent_level = indent
            indented += 1
            indented_lines[-1] += ' {'

        indented_lines.append(line)

    while indented > 0:
        indented_lines[-1] += ' }'
        indented -= 1
        indented_lines.append('')

    return indented_lines

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


# adds tuples to return statements and std::tie to assignments
def add_destructuring(lines):
    new_lines = []
    for line in lines:
        line = line.rstrip()
        if line.strip().startswith('return'):
            indent = get_indent(line)
            args = get_args(line[indent + len('return'):])
            if len(args) > 1:
                args = ''.join(args).strip()
                line = "%sreturn make_tuple(%s)" % (' ' * indent, args)

        elif line.find('=') != -1:
            indent = get_indent(line)
            lhs, rhs = line.split('=')
            args = get_args(lhs)
            if len(args) > 1:
                args = ''.join(args).strip()
                rhs = rhs.strip()
                line = '%sstd::tie(%s) = %s' % (' ' * indent, args, rhs)

        new_lines.append(line)

    return new_lines

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

def skip_comments(lines):
    return comment_remover(''.join(lines)).split('\n')

def add_parentheses(lines):

    new_lines = []
    replace = ["if ", "while "]
    for line in lines:
        indent = get_indent(line)
        sline = line.strip()
        # TODO: join multiple lines (maybe look for next colon?)
        for tok in replace:
            if sline.startswith(tok):
                line = "%sif (%s) " % (' ' * indent, line[indent+len(tok):])

        new_lines.append(line)

    return new_lines

def add_io(lines):
    new_lines = []
    for line in lines:
        indent = get_indent(line)
        sline = line.strip()
        if sline.startswith('!!'):
            args = split_quotes(sline[2:])
            line = "%sstd::cout << %s" % (' ' * indent, " << ".join(args))

        elif sline.startswith('?'):
            args = split_quotes(sline[2:])
            tokens = []
            cin_tokens = []
            cout_tokens = []
            for arg in args:
                if arg[0] != '"':
                    if cout_tokens:
                        tokens.append("std::cout")
                        tokens.extend(cout_tokens)
                        tokens.append(';')
                        cout_tokens = []

                    cin_tokens.append(">>")
                    cin_tokens.append(arg)
                else:
                    if cin_tokens:
                        tokens.append("std::cin")
                        tokens.extend(cin_tokens)
                        tokens.append(';')
                        cin_tokens = []

                    cout_tokens.append("<<")
                    cout_tokens.append(arg)

            if cout_tokens:
                tokens.append("std::cout")
                tokens.extend(cout_tokens)
                tokens.append(';')

            if cin_tokens:
                tokens.append("std::cin")
                tokens.extend(cin_tokens)
                tokens.append(';')

            line = "%s%s" % (' ' * indent, " ".join(tokens))

        else:
            for tok in ["!", "std::cout ", "cout "]:
                if sline.startswith(tok):
                    args = split_quotes(sline[len(tok):])
                    no_add = False
                    for arg in args:
                        if arg == "<<":
                            no_add = True
                            break

                    if no_add:
                        continue

                    if not args:
                        line = "%sstd::cout << std::endl" % (' ' * indent)
                    else:
                        line = "%sstd::cout << %s << std::endl" % (' ' * indent, " << ' ' << ".join(args))


        new_lines.append(line)

    return new_lines


def pipeline(lines):
    lines = skip_comments(lines)
    lines = add_destructuring(lines)
    lines = add_parentheses(lines)
    lines = add_io(lines)
    lines = add_semi_colons(lines)
    lines = translate_indents(lines)
    lines = replace_double_semicolons(lines)

    return lines

lines = sys.stdin.readlines()
lines = pipeline(lines)
print('\n'.join(lines))
