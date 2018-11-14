from util import *

import clanger
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

def extract_functions(lines):
    extracted = []
    for line in lines:
        if line_is_function(line):
            func_decl = line.rstrip('{')
            func_decl += ';'
            extracted.append(func_decl)

    return extracted
