from util import *

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

        j = i+1
        while j < len(lines) and not lines[j].strip():
            j += 1

        if indents[i] < indents[j]:
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
            # we have `do` here, just in case
            for tok in ['for ', 'while ', 'do ', 'else if', 'if ']:
                if cline.startswith(tok):
                    add_semi = False
                    break

        if add_semi:
            line += ';'

        new_lines.append(line)

    return new_lines

def add_curly_braces(lines):
    new_lines = []
    indent_levels = [0]
    nb = 0

    for i, line in enumerate(lines):
        line = line.rstrip('\n')
        indent = get_indent(line)
        if not line.strip():
            new_lines.append(line)
            continue

        if visibility_line(line):
            # TODO: when we hit a public line, i guess we reset indent levels?
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
                if not case_statement(new_lines[nb]):
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

def join_backslash_lines(lines):
    new_lines = ['']

    i = 0
    full_line = []
    while i < len(lines):
        line = lines[i].rstrip()
        if full_line:
            line = line.strip()
        if line.endswith('\\'):
            # strip off the backslash, strip off the remaining spaces
            full_line.append(line.rstrip('\\').rstrip())
        else:
            if full_line:
                full_line.append(line.strip())
            else:
                full_line.append(line)
            new_lines.append(' '.join(full_line))
            full_line = []

        i += 1

    return new_lines






def add_parentheses(lines):
    new_lines = []
    replace = ["if ", "while ", "for ", "else if ", "switch " ]
    for line in lines:
        indent = get_indent(line)
        sline = line.strip()
        # TODO: join multiple lines (maybe look for next colon?)
        for tok in replace:
            if sline.startswith(tok):
                nline = line[indent+len(tok):].rstrip(':')
                if nline[0] != '(' or nline[-1] != ')':
                    line = "%s%s(%s) " % (' ' * indent, tok, nline)

        new_lines.append(line)

    return new_lines

