from util import *

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

def make_declarations(line, scope):
    global DESTRUCTURE_INDEX

    di = DESTRUCTURE_INDEX
    indent = get_indent(line)
    tokens = line.strip().split('= ')

    # TODO: what do we do if tokens > 2?
    if len(tokens) == 2:
#        lhs = tokens[0]
#        rhs = tokens[1]
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
                    if arg == '_':
                        continue

                    if not arg in scope:
                        line += '\n%sauto %s = get<%s>(%s);' % (' ' * indent, arg, j, pname )
                    else:
                        line += '\n%s%s = get<%s>(%s);' % (' ' * indent, arg, j, pname)

                di += 1

        elif len(args[0].split()) == 1:
            arg = args[0].strip()
            carg = no_punctuation(args[0])
            if not var_access(arg) and not carg in scope:
                line = "%sauto %s = %s" % (' ' * indent, arg, rhs)

    DESTRUCTURE_INDEX = di
    return line

# adds tuples to return statements and std::tie to assignments
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
            if DECLARE_VARIABLES:
                line = make_declarations(line, scope)


        new_lines.append(line)

    return new_lines

def add_auto_declarations(lines, scopings):
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
            line = "%sfor %s" % (' '*indent, ";".join(args))



        new_lines.append(line)
    return new_lines

