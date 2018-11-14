from __future__ import print_function

import sys
import shlex

from util import *
import clanger

def dot_access(arg):
    return arg.find('.') != -1

def array_access(arg):
    return arg.find('[') != -1

def add_semi_colons(lines):
    new_lines = []
    indents = []
    for line in lines:
        indents.append(get_indent(line))

    indents.append(0)

    for i, line in enumerate(lines):
        line = line.rstrip();
        cline = line.strip()

        if not line or line[0] == '#':
            new_lines.append(line)
            continue

        if indents[i] < indents[i+1]:
            new_lines.append(line)
            continue

        add_semi = True
        # there are a lot of reasons not to add a semicolon, like
        # if the line doesn't end with a backslash, colon or start with class keyword
        # or if the line has a template< decl on it
        if cline[-1] == '\\':
            add_semi = False
        elif cline[-1] == ':':
            add_semi = False
        elif cline[-1] == ';':
            add_semi = False
        elif cline.startswith('class '):
            add_semi = False
        elif cline.startswith("template<") or cline.startswith("template <"):
            add_semi = False

        if add_semi:
            line += ';'

        new_lines.append(line)

    return new_lines


def visibility_line(line):
    return line.endswith('private:') or line.endswith('public:')

def remove_blocks(lines):
    new_lines = []
    for line in lines:
        indent = get_indent(line)
        cline = line.strip()
        if cline.startswith('block:'):
            line = "%s/* %s */" % (' ' * indent, cline)

        new_lines.append(line)
    return new_lines

def remove_knowns(lines):
    new_lines = []
    for line in lines:
        indent = get_indent(line)
        cline = line.strip()
        if cline.startswith('known '):
            line = "%s// %s" % (' ' * indent, cline)

        new_lines.append(line)
    return new_lines

def read_scopings(lines):
    indent_levels = [0]
    nb = 0
    scopings = {}
    scope = {}
    scope_stack = { 0: scope }


    for i, line in enumerate(lines):
        line = line.rstrip('\n')
        indent = get_indent(line)

        if indent in scope_stack:
            scope = scope_stack[indent]
        else:
            scope = {}
            scope_stack[indent] = scope

        scopings[i] = [c for c in scope]

        if not line:
            continue

        if visibility_line(line):
            continue

        if indent_levels[-1] > indent:
            while indent_levels[-1] > indent:
                indent_levels.pop()
                scope = scope_stack[indent_levels[-1]]


        if indent_levels[-1] < indent:
            if not visibility_line(lines[nb]):
                indent_levels.append(indent)

                scope = dict([(c, c) for c in scope])
                scope_stack[indent] = scope

        if i < len(lines) - 1:
            next_line = lines[i+1]
            next_indent = get_indent(next_line)

            if indent < next_indent:
                scope = dict([(c, c) for c in scope])
                scope_stack[next_indent] = scope

        new = clanger.add_identifiers(line, scope)

        # last non blank line is this one
        nb = i

    return scopings

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

                if indent_levels[-1] == 0 and new_lines[nb][-1] != ';':
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

        if new_lines[nb][-1] != ";":
            new_lines[nb] += ';';

        indent_levels.pop()
    new_lines.append('')

    return new_lines


def make_declarations(line, scope):
    global DESTRUCTURE_INDEX

    di = DESTRUCTURE_INDEX
    indent = get_indent(line)
    tokens = line.strip().split('= ')
    if len(tokens) > 1:
        lhs, rhs = line.split('= ')
        args = smart_split(lhs, ',')
        if len(args) > 1:

            if lhs.find(' ') > lhs.find(','):
                return line

            need_args = False
            for arg in args:
                arg = arg.strip(',').strip()
                if arg not in scope:
                    need_args = True
            rhs = rhs.strip()

            if not need_args:
                args = ','.join(args).strip()
                line = '%sstd::tie(%s) = %s' % (' ' * indent, args, rhs)
            else:
                pname = "structuredArgs_%s" % (di)
                line = '%sauto %s = %s;' % (' ' * indent, pname, rhs)
                for j, arg in enumerate(args):
                    arg = arg.strip(',').strip()
                    if not arg in scope:
                        line += '\n%sauto %s = get<%s>(%s);' % (' ' * indent, arg, j, pname )
                    else:
                        line += '\n%s%s = get<%s>(%s);' % (' ' * indent, arg, j, pname)

                di += 1

        elif len(args[0].split()) == 1:
            arg = args[0].strip()
            if not array_access(arg) and not dot_access(arg) and not arg in scope:
                line = "%sauto %s = %s" % (' ' * indent, arg, rhs)

    DESTRUCTURE_INDEX = di
    return line

# adds tuples to return statements and std::tie to assignments
DESTRUCTURE_INDEX = 0
def add_destructuring(lines, scopings):
    new_lines = []
    keywords = [ "for", "while", "do" ]
    for i, line in enumerate(lines):
        # remove any trailing ':' and whitespace
        line = line.rstrip()
        sline = line.strip()

        if i in scopings:
            scope = scopings[i]
        else:
            scope = {}

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
            args = smart_split(line[indent + len('return'):], ',')
            if len(args) > 1:
                args = ', '.join(args).strip()
                line = "%sreturn make_tuple(%s)" % (' ' * indent, args)

        elif line.find('=') != -1:
            line = make_declarations(line, scope)


        new_lines.append(line)

    return new_lines

def skip_comments(lines):
    return comment_remover(''.join(lines)).split('\n')

def replace_tabs(lines):
    return [ line.replace('\t', '    ') for line in lines ]

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
                if nline[0] != '(':
                    line = "%s%s(%s) " % (' ' * indent, tok, nline)

        new_lines.append(line)

    return new_lines

def io_readline(line, indent, read_token):
    sline = line.strip()
    args = smart_split(sline[len(read_token):], ' ,')
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
        args = smart_split(sline[len(print_token):], ' ,')
        line = "%sstd::cout << %s" % (' ' * indent, " << ".join(args))
        return line

    # PRINT WITH NEWLINE
    if sline == "print":
        return "%sstd::cout << std::endl" % (' ' * indent)

    for tok in ["!", "std::cout ", "cout ", "print "]:
        if sline.startswith(tok):
            args = smart_split(sline[len(tok):], ' ,')
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

def replace_for_shorthand(lines):
    new_lines = []
    for line in lines:
        sline = line.strip()

        if sline.startswith("for ") and sline.find(";") == -1:
            # check if we are in a range loop
            range_loop = False
            if sline.find(':') != -1 and sline.find(':') != len(sline) - 1:
                range_loop = True

            if not range_loop:
                rem = sline[len("for "):].rstrip(':')
                args = rem.split()

                ind = ' ' * get_indent(line)

                if len(args) == 2:
                    line = "%sfor auto %s = 0; %s < %s; %s++" % (ind, args[0], args[0], args[1], args[0])
                if len(args) == 3:
                    line = "%sfor auto %s = %s; %s < %s; %s++" % (ind, args[0], args[1], args[0],
                        args[2], args[0])
                if len(args) == 4:
                    line = "%sfor auto %s = %s; %s < %s; %s += %s" % (ind, args[0], args[1], args[0],
                        args[2], args[0], args[3])


        new_lines.append(line)

    return new_lines

def add_declarations(lines, scopings):
    new_lines = []
    for i, line in enumerate(lines):
        sline = line.strip()
        scope = scopings[i]
        indent = get_indent(line)
        if indent == 0:
            type = ""
            var = ""
            pr = line.find("(")
            if pr > 0:
                lp = line.find(")")
                params = smart_split(line[pr+1:lp], ",")
                before_p = line[:pr]
                after_p = line[lp+1:]
                prev = None

                new_params = []
                # if any param has spaces in it, then we think it is a function declaration
                # foo(int a) vs foo(10, 20, "abc")
                for p in params:
                    args = smart_split(p, " ")
                    if len(args) == 1:
                        var = args[0]
                    elif len(args) >= 2:
                        type = " ".join(args[:-1])
                        var = args[-1]

                    if type:
                        new_params.append("%s %s" % (type, var))
                    else:
                        new_params.append(var)

                args = before_p.split()
                if len(args) == 1 and before_p != "main":
                    line = "auto %s(%s)%s" % (before_p, ", ".join(new_params), after_p)
                else:
                    line = "%s(%s)%s" % (before_p, ", ".join(new_params), after_p)


        # special for loop declarations
        if sline.startswith('for '):
            args = sline.split(';')
            args[0] = args[0][len('for '):]

            stmts = smart_split(args[0], ',')
            arg0 = []
            for j, s in enumerate(stmts):
                toks = s.split('=')
                if len(toks) == 1:
                    arg0.append(s)
                    continue

                lhs, rhs = toks
                rhs = rhs.strip()

                arg = lhs.strip()
                add_auto = True
                if j != 0:
                    add_auto = False
                elif array_access(arg):
                    add_auto = False
                elif dot_access(arg):
                    add_auto = False
                elif arg in scope:
                    add_auto = False
                elif len(arg.split()) > 1:
                    add_auto = False
                if add_auto:
                    arg = "auto %s" % (arg)

                arg0.append("%s = %s" % (arg, rhs))

            args[0] = ", ".join(arg0)
            line = "%sfor %s" % (' '*indent, ";".join(args))



        new_lines.append(line)
    return new_lines

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
    lines = replace_tabs(lines)
    lines = replace_for_shorthand(lines)

    scopings = read_scopings(lines)
    lines = remove_knowns(lines)
    lines = remove_blocks(lines)
    lines = add_declarations(lines, scopings)
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
