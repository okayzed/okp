from __future__ import print_function

from ..util import *
from .. import analysis
import sys

def var_access(arg):
    return dot_access(arg) or array_access(arg) or ptr_access(arg)

def no_punctuation(arg):
    narg = []
    for c in arg:
        if c.isalnum() or c == '_':
            narg.append(c)

    return ''.join(narg)

DESTRUCTURE_INDEX = 0

DECLARE_VARIABLES = True

# this function splits equals, skipping over '==' and turning '= ' into ''
# we also do not consider equals that are inside brackets to be meaningful
def split_equals(line):
    tokens = []
    prev = []
    i = 0
    brackets = 0
    while i < len(line):
        c = line[i]
        peeked = ''
        if c == '=':
            if i < len(line)-1:
                peeked = line[i+1]

            if peeked == '=':
                prev.append(c)
                prev.append(peeked)
                i += 1
            elif not brackets:
                if prev:
                    tokens.append(''.join(prev))
                prev = []

        else:
            if c == '[':
                brackets += 1
            elif c == ']':
                brackets -= 1
            prev.append(c)
        i += 1

    tokens.append(''.join(prev))

    return tokens

def get_class(line):
    tokens = smart_split(line, ' ')
    if tokens[0] == "class":
        return tokens[1].rstrip(':')
    if tokens[0] == "struct":
        return tokens[1].rstrip(':')
    return ""


def handle_unscoped_variables(line, scope):
    if not DECLARE_VARIABLES:
        return line

    indent = get_indent(line)

    # we need to split on single equals but not double equals
    # we also need to swallow '= ' and turn it into '='
    tokens = split_equals(line.strip())

    # TODO: what do we do if tokens > 2?
    if len(tokens) == 2:
        lhs, rhs = tokens
        rhs = rhs.strip()
        args = smart_split(lhs, ',')
        if len(args) > 1:
            return

        if len(args[0].split()) == 1:
          if args[0].find(".") == -1 and args[0].find(":") == -1:
                arg = args[0].strip()
                carg = no_punctuation(args[0])
                if not var_access(arg) and not carg in scope:
                    line = "%sauto %s = %s" % (' ' * indent, arg, rhs)

    return line

def handle_return_tuples(line, scope):
    indent = get_indent(line)
    args = smart_split(line[indent + len('return'):], ',')
    if len(args) > 1:
        args = ', '.join(args).strip()
        line = "%sreturn make_tuple(%s)" % (' ' * indent, args)
    return line

def handle_destructuring_decls(line, scope):
    global DESTRUCTURE_INDEX

    di = DESTRUCTURE_INDEX
    indent = get_indent(line)

    # we need to split on single equals but not double equals
    # we also need to swallow '= ' and turn it into '='
    tokens = split_equals(line.strip())

    # TODO: what do we do if tokens > 2?
    if len(tokens) == 2:
        lhs, rhs = tokens
        rhs = rhs.strip()
        args = smart_split(lhs, ',')
        if len(args) > 1:

            if lhs.find('[') != -1:
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
                    if arg == '_':
                        continue

                    if not arg in scope:
                        line += '%sauto %s = get<%s>(%s);' % (' ' * indent, arg, j, pname )
                    else:
                        line += '%s%s = get<%s>(%s);' % (' ' * indent, arg, j, pname)

                di += 1

    DESTRUCTURE_INDEX = di
    return line

def handle_for_loop_auto(line, scope):
    # special for loop declarations
    sline = line.strip()
    if sline.startswith('for ') or sline.startswith('for('):
        # if its a for loop, remove ending colon just in case so we don't
        # swallow it when parenthesizing
        sline = sline.rstrip(':')

        args = smart_split(sline, ';')
        if sline.startswith('for('):
            args[0] = args[0][len('for'):]
        else:
            args[0] = args[0][len('for '):]

        args[0] = strip_outer_parens(args[0])

        # if our args are glommed together because of for loop bracketing, we
        # try to unroll it using smart_split on the only item in the array
        if len(args) == 1:
            args = smart_split(args[0], ';')

        stmts = smart_split(args[0], ',')

        arg0 = []
        for j, s in enumerate(stmts):
            toks = s.split(':=')
            if len(toks) == 1:
                toks = s.split('=')

            if len(toks) == 1:
                arg0.append(s)
                continue

            lhs, rhs = toks
            rhs = rhs.strip()

            arg = lhs.strip()

            add_auto = DECLARE_VARIABLES
            if j != 0:
                add_auto = False
            elif s.find(":") != -1:
                add_auto = True
            elif var_access(arg):
                add_auto = False
            elif arg in scope:
                add_auto = False
            elif len(arg.split()) > 1:
                add_auto = False

            if add_auto:
                arg = "auto %s" % (arg)

            arg0.append("%s = %s" % (arg, rhs))

        args[0] = ", ".join(arg0)
        indent = get_indent(line)
        line = "%sfor %s" % (' '*indent, ";".join(args))

    return line

def handle_function_decls(line, scope, in_class):
    # check for function level declarations,
    # they either happen at the toplevel (0)
    # or inside a class and on the first level
    # TODO: figure out where more of these can happen
    type = ""
    var = ""
    pr = line.find("(")
    if pr > 0:
        lp = line.find(")")
        if lp == -1:
            return line

        params = smart_split(line[pr+1:lp], ",")

        before_p = line[:pr]
        after_p = line[lp+1:]

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
        class_func = False

        if in_class:
            class_name, _ = in_class[-1]
            if before_p.strip() == class_name.strip():
                class_func = True
            elif before_p.strip() == "~%s" % class_name.strip():
                class_func = True

        lambda_func = False
        if line.find('](') != -1:
            lambda_func = True

        if not lambda_func:
            indent = get_indent(line)

            if before_p == "main":
                if len(args) == 1:
                    line = "%sint %s(%s)%s" % (' ' * indent, before_p, ", ".join(new_params), after_p)
            elif len(args) == 1 and not class_func:
                # this clause is for functions that leave off their return type:
                # main():
                #   pass
                before_p = before_p.strip()
                line = "%sauto %s(%s)%s" % (' ' * indent, before_p, ", ".join(new_params), after_p)
            else:
                line = "%s(%s)%s" % (before_p, ", ".join(new_params), after_p)

    return line

def add_auto_declarations(lines):
    new_lines = []
    class_start = 0
    scopings = analysis.read_scopings(lines)

    keywords = ["if", "do ", "while", "else", "class", "struct", "typedef", "try", "catch"]
    in_class = []
    for i, line in enumerate(lines):
        if ignore_line(line, new_lines):
            continue
        sline = line.strip()
        scope = scopings[i]
        indent = get_indent(line)

        if sline != "":
            while in_class and in_class[-1][1] >= indent:
                in_class.pop()

        if is_class(line) or is_struct(line):
            in_class.append((get_class(line), indent))


        skip_line = False
        for k in keywords:
            if sline.startswith(k) or sline.endswith('{'):
                new_lines.append(line)
                skip_line = True
                break

        if skip_line:
            continue

        next_indent = indent
        if i < len(lines) - 1:
            next_line = lines[i+1]
            next_indent = get_indent(next_line)

        if sline.startswith('for ') or sline.startswith('for('):
            line = handle_for_loop_auto(line, scope)
        if indent == 0 or indent < next_indent:
            line = handle_function_decls(line, scope, in_class)
        if line.strip().startswith('return'):
            line = handle_return_tuples(line, scope)
        if line.find('=') != -1 and not sline.endswith(':'):
            line = handle_destructuring_decls(line, scope)
            line = handle_unscoped_variables(line, scope)

        new_lines.append(line)
    return new_lines


def replace_walrus_operator(lines):
    newlines = []
    for line in lines:
        sline = line.strip()
        if sline.startswith("for ") or sline.startswith("for("):
            newlines.append(line)
            continue

        tokens = smart_split(line, [" "])
        indent = get_indent(line)
        walrus_toks = [t for t in tokens if ":=" in t and not t.startswith('"')]
        if walrus_toks:
            # for destructuring tuples, we let replace_destructuring_decls() handle
            # the auto declaration
            if "," in line and line.index(",") < line.index(":="):
                newlines.append(line.replace(":=","="))
            else:
                new_toks = [indent*" "+"auto"]
                for tok in tokens:
                    if ":=" in tok and (not tok.startswith('"')):
                        new_toks.append(tok.replace(":=","="))
                    else:
                        new_toks.append(tok)
                newlines.append(" ".join(new_toks))
        else:
            newlines.append(line)
    return newlines
