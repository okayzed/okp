from ..util import *


def add_trailing_semicolons(lines):
    new_lines = []
    indents = []
    for line in lines:
        indents.append(get_indent(line))

    indents.append(0)
    double_ignore = IGNORE_CHAR + IGNORE_CHAR

    for i, line in enumerate(lines):
        line = line.rstrip();
        cline = line.strip()

        # we dont ignore lines with preceding semicolons
        if ignore_line(line, new_lines):
            continue
        if cline == double_ignore:
            new_lines.append(line)
            continue

        if not cline or cline[0] == '#':
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
        elif cline[-1] == '{':
            add_semi = False
        elif cline.startswith('class '):
            add_semi = False
        elif line_is_template(cline):
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

    outer_indent = 0

    for i, line in enumerate(lines):
        line = line.rstrip('\n')
        indent = get_indent(line)
        if not line.strip():
            new_lines.append(line)
            continue

        if ignore_line(line, new_lines):
            continue

        if visibility_line(line):
            # TODO: when we hit a public line, i guess we reset indent levels?
            new_lines.append(line)
            continue

        if hash_line(line):
            new_lines.append(line)
            continue

        if is_class(line):
            outer_indent = indent

        if indent_levels[-1] > indent:
            while indent_levels[-1] > indent:
                indent_levels.pop()
                new_lines[nb] += ' }'

                if indent_levels[-1] == outer_indent and new_lines[nb][-1] != ';':
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

        if len(new_lines[nb]) and new_lines[nb][0] != "#" and new_lines[nb][-1] != ";":
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



def add_preceding_ignore_chars(lines):
    new_lines = []
    in_ignore_block = False
    ig = IGNORE_CHAR
    for line in lines:
        if line.strip().startswith('```'):
            in_ignore_block = not in_ignore_block
        elif in_ignore_block:
            new_lines.append('%s%s%s' % (ig, ig, line))
        else:
            new_lines.append(line)

    return new_lines

def remove_preceding_ignore_chars(lines):
    new_lines = []
    double_ignore = IGNORE_CHAR + IGNORE_CHAR
    for line in lines:
        indent = get_indent(line)
        sline = line.strip()

        if sline.find(double_ignore) != -1:
            line = line.replace(double_ignore, '', 1)

        if sline and sline[0] == IGNORE_CHAR:
            line = line.replace(IGNORE_CHAR, ' ', 1)

        new_lines.append(line)

    return new_lines


# we might have a case like: if (a) || (b): which still needs parentheses
# the only good case is when the first paren is matching the last paren
def needs_parens(nline):
    if nline[0] != '(' or nline[-1] != ')':
        return True

    paren_stack = []
    last_pop = 0
    for i, c in enumerate(nline):
        if c == '(':
            paren_stack.append(i)
        elif c == ')':
            last_pop = paren_stack.pop()

    if paren_stack or last_pop != 0:
        return True


def add_parentheses(lines):
    new_lines = []
    replace = ["if ", "while ", "for ", "else if ", "switch " ]
    for line in lines:
        if ignore_line(line, new_lines):
            continue

        indent = get_indent(line)
        sline = line.strip()
        # TODO: join multiple lines (maybe look for next colon?)
        for tok in replace:
            if sline.startswith(tok):
                nline = line[indent+len(tok):].rstrip(':')
                if nline[-1] != ';' and needs_parens(nline):
                    line = "%s%s(%s) " % (' ' * indent, tok, nline)

        new_lines.append(line)

    return new_lines

