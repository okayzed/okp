from __future__ import print_function

import sys
import shlex

from util import *

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


def visibility_line(line):
    return line.endswith('private:') or line.endswith('public:')

def translate_indents(lines):
    new_lines = []
    indent_levels = [0]
    nb = 0
    for i, line in enumerate(lines):
        line = line.rstrip('\n')
        indent = get_indent(line)
        if not line:
            new_lines.append(line)
            continue

        if visibility_line(line):
            new_lines.append(line)
            continue


        if indent_levels[-1] > indent:
            while indent_levels[-1] > indent:
                indent_levels.pop()
                new_lines[nb] += ' }'

                if indent_levels[-1] == 0:
                    new_lines[nb] += ';'


        if indent_levels[-1] < indent:
            if not visibility_line(new_lines[nb]):
                indent_levels.append(indent)
                new_lines[nb] = new_lines[nb].rstrip(':')
                new_lines[nb] += ' {'

        new_lines.append(line)

        # last non blank line is this one
        nb = i

    while indent_levels:
        if indent_levels[-1] > 0:
            new_lines[nb] += ' }'

        new_lines[nb] += ';';
        indent_levels.pop()
    new_lines.append('')

    return new_lines


# adds tuples to return statements and std::tie to assignments
def add_destructuring(lines):
    new_lines = []
    keywords = [ "for", "while", "do" ]
    for line in lines:
        # remove any trailing ':' and whitespace
        line = line.rstrip()
        sline = line.strip()

        added = False
        for k in keywords:
            if sline.startswith(k):
                new_lines.append(line)
                added = True
                break

        if added:
            continue

        if line.strip().startswith('return'):
            indent = get_indent(line)
            args = get_args(line[indent + len('return'):])
            if len(args) > 1:
                args = ''.join(args).strip()
                line = "%sreturn make_tuple(%s)" % (' ' * indent, args)

        elif line.find('=') != -1:
            indent = get_indent(line)
            tokens = line.split('= ')
            if len(tokens) > 1:
                lhs, rhs = line.split('= ')
                args = get_args(lhs)
                if len(args) > 1:
                    args = ''.join(args).strip()
                    rhs = rhs.strip()
                    line = '%sstd::tie(%s) = %s' % (' ' * indent, args, rhs)

        new_lines.append(line)

    return new_lines

def skip_comments(lines):
    return comment_remover(''.join(lines)).split('\n')

def add_parentheses(lines):
    new_lines = []
    replace = ["if ", "while ", "for "]
    for line in lines:
        indent = get_indent(line)
        sline = line.strip()
        # TODO: join multiple lines (maybe look for next colon?)
        for tok in replace:
            if sline.startswith(tok):
                nline = line[indent+len(tok):].rstrip(':')
                line = "%s%s(%s) " % (' ' * indent, tok, nline)

        new_lines.append(line)

    return new_lines

def io_readline(line, indent, read_token):
    sline = line.strip()
    args = split_quotes(sline[len(read_token):])
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
    return line

def io_printline(line, indent):
    sline = line.strip()
    print_token = None
    # PRINT NO NEWLINE
    if sline.startswith('!!'):
        print_token = "!! "
    if sline.startswith('puts '):
        print_token = 'puts '

    if print_token:
        args = split_quotes(sline[len(print_token):])
        line = "%sstd::cout << %s" % (' ' * indent, " << ".join(args))
        return line

    # PRINT WITH NEWLINE
    if sline == "print":
        return "%sstd::cout << std::endl" % (' ' * indent)

    for tok in ["!", "std::cout ", "cout ", "print "]:
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

    return line

def add_io(lines):
    new_lines = []
    tokens = [ '? ', 'read ', '?? ' ]
    for line in lines:
        indent = get_indent(line)
        sline = line.strip()

        read_token = None
        for tok in tokens:
            if sline.startswith(tok):
                read_token = tok

        if read_token:
            line = io_readline(line, indent, read_token)

        else:
            line = io_printline(line, indent)


        new_lines.append(line)

    return new_lines

def replace_pass(lines):
    new_lines = []
    for line in lines:
        if line.strip() == "pass":
            line = line.replace("pass", "(void)0")

        new_lines.append(line)

    return new_lines
# imply
def imply_functions(lines):
    new_lines = []
    for line in lines:
        cline = line.strip()
        if cline.startswith("def "):
            tokens = cline.split()
            next_word = tokens[1]
            if next_word.find("(") == -1 or cline.find("main(") != -1:
                line = line.replace("def ", "")
            else:
                # is a function
                line = line.replace("def ", "auto ")

        new_lines.append(line)

    return new_lines

def pipeline(lines):
    lines = skip_comments(lines)
    lines = add_destructuring(lines)
    lines = add_parentheses(lines)
    lines = imply_functions(lines)
    lines = replace_pass(lines)
    lines = add_io(lines)
    lines = add_semi_colons(lines)
    lines = translate_indents(lines)
    lines = replace_double_semicolons(lines)

    return lines

lines = sys.stdin.readlines()
lines = pipeline(lines)
print('\n'.join(lines))
