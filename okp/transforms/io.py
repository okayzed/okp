from ..util import *

def io_readline(line, read_token):
    sline = line.strip()

    is_readline = False
    if read_token.startswith('raw_input'):
        is_readline = True
    if is_readline:
        args = smart_split(sline[len(read_token):], ' ,')
    else:
        args = smart_split(sline[len(read_token):], ' ,')

    # if the line already has >> or << on it, we don't process it
    for arg in args:
        if arg == "<<" or arg == ">>":
            return line

    tokens = []
    cin_tokens = []
    cout_tokens = []
    for arg in args:
        if arg[0] != '"':
            if cout_tokens:
                tokens.append("cout")
                tokens.extend(cout_tokens)
                tokens.append(';')
                cout_tokens = []

            cin_tokens.append(">>")
            cin_tokens.append(arg)
        else:
            if cin_tokens:
                tokens.append("cin")
                tokens.extend(cin_tokens)
                tokens.append(';')
                cin_tokens = []

            cout_tokens.append("<<")
            cout_tokens.append(arg)

    if cout_tokens:
        tokens.append("cout")
        tokens.extend(cout_tokens)
        tokens.append(';')

    if cin_tokens:
        tokens.append("cin")
        tokens.extend(cin_tokens)

    line = " ".join(tokens)
    return line

def io_printline(line, indent):
    sline = line.strip()
    print_token = None
    # PRINT NO NEWLINE
    add_space = True
    if sline.startswith('!!'):
        print_token = "!! "
    if sline.startswith('puts '):
        print_token = 'puts '
        if sline.endswith(","):
            add_space = False

    if print_token:
        args = smart_split(sline[len(print_token):], ' ,')
        line = "%scout << %s" % (' ' * indent, " << ".join(args))
        if add_space:
            line = '%s << " "' % (line)
        return line

    # PRINT WITH NEWLINE
    if sline == "print":
        return "%scout << endl" % (' ' * indent)

    for tok in ["!", "std::cout ", "cout ", "print "]:
        if sline.startswith(tok):
            if tok == "print ":
                args = smart_split(sline[len(tok):], ',')
            else:
                args = smart_split(sline[len(tok):], ' ,')
            no_add = False
            for arg in args:
                if arg == "<<":
                    no_add = True
                    break

            if no_add:
                continue

            spc = "endl";
            if sline.endswith(','):
                spc = "' '";

            if not args:
                line = "%scout << %s" % (' ' * indent, spc)
            else:
                line = "%scout << %s << %s" % (' ' * indent, " << ' ' << ".join(args), spc)

    return line

def replace_io_keywords(lines):
    new_lines = []
    tokens = [ '?', '??', 'cin', 'raw_input']
    for line in lines:
        if ignore_line(line, new_lines):
            continue
        indent = get_indent(line)
        sline = line.strip()

        read_token = None
        toks = smart_split(line, '(): ')

        for i, t in enumerate(toks):
            for tok in tokens:
                if i > 0 and (tok[0] == '?'):
                    continue

                if t == tok:
                    read_token = tok
                    rtoks = toks[i:]
                    rline = " ".join(rtoks)
                    pline = toks[:i]

        if read_token:
            if len(pline):
                pline = " ".join(pline) + " "
            else:
                pline = ""

            rline = io_readline(rline, read_token)
            line = "%s%s%s" % (' ' * indent, pline, rline)

        else:
            line = io_printline(line, indent)


        new_lines.append(line)

    return new_lines
