from util import *

import id_recognizer
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

        # last non blank line is now this one
        nb = i

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

        new = id_recognizer.add_identifiers(line, scope)

        # compare libclang vs. our own version
        # import clanger
        # new2 = clanger.add_identifiers(line, bscope)
        # debug("TOKENS", line, new, new2)


    return scopings

# after line is already decorated, we can check if its a function
# so we can make a .h file for this .cpp file
CONTROL_WORDS = [
    'else',
    'if',
    'class',
    'struct',
    'typedef',
    'for',
    'while']

def line_is_function(line):
    args = smart_split(line, ' ')
    if not args:
        return

    if args[0] in CONTROL_WORDS:
        return False

    if args[-1].endswith('{') and line.find('(') != -1:
        return True

    return False


def extract_header(lines):
    extracted = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if line_is_include(line) or line_is_using(line):
            extracted.append(line)

        if line_is_function(line):
            func_decl = line.rstrip('{')
            func_decl += ';'
            extracted.append(func_decl)


        if is_struct(line) or is_class(line):
            until = extract_until_close(lines, i)
            ex = lines[i:until]
            extracted.extend(ex)
            i = until
        else:
            i += 1

    return extracted

def remove_structs_and_classes(lines):
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_struct(line) or is_class(line):
            until = extract_until_close(lines, i)
            i = until
        else:
            i += 1
            new_lines.append(line)

    return new_lines
