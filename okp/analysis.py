from __future__ import print_function
from .util import *

import os

from . import id_recognizer
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
            x = 1
            # skip empty-ish lines when figuring out next indent
            while i+x < len(lines) -1 and not lines[i+x].strip() :
                x += 1

            next_line = lines[i+x]
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

def line_is_class_definition(line):
    args = smart_split(line, ' ')
    if not args:
        return

    if args[0].find('::') != -1 or args[1].find('::') != -1:
        return True

def file_contains_main(lines):
    i = 0
    while i < len(lines):
        line = lines[i]
        if is_struct(line) or is_class(line):
            until = extract_until_close(lines, i)
            if until:
                i = until
                continue


        if re.search("main(.*) {", line):
            return True

        i += 1

    return False

def gather_includes(file, includes, base_dir=None):
    if file in includes:
        return

    dirname = os.path.dirname(file)
    fname = os.path.basename(file)

    if base_dir == None:
        base_dir = dirname
    else:
        base_dir = os.path.join(base_dir, dirname)

    file = os.path.join(base_dir, fname)
    includes[file] = True


    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        cline = line.strip()
        if cline.startswith("#include"):
            tokens = cline.split()
            include = tokens[1]
            if include[0] != '"':
                continue
            include = include.strip('"')

            fname, ext = os.path.splitext(include)
            cpyname = "%s.cpy" % fname
            if os.path.exists(os.path.join(base_dir, cpyname)):
                gather_includes(cpyname, includes, base_dir)
            else:
                gather_includes(include, includes, base_dir)

        if cline.startswith("import"):
            tokens = cline.split()
            include = tokens[1]
            fname = "%s.cpy" % include

            gather_includes(fname, includes, base_dir)

    return includes

def gather_files(files):
    ret = {}
    original_dir = os.getcwd()
    for file in files:
        if file == '-':
            ret[file] = True
            continue

        if not os.path.exists(file):
            continue
        file_dir, file = os.path.split(file)
        if file_dir:
            os.chdir(file_dir)
        gather_includes(file, ret)

    os.chdir(original_dir)
    return list(ret.keys())

def guess_required_files(lines):
    requires = set()
    defines = set()

    REQUIRE_KEYWORDS = {
        "<iostream>" : [ "cout", "cin", "endl" ],
        "<vector>" : [ "vector" ],
        "<tuple>" : [ "tuple", "make_tuple", "tie", "std::tie"],
        "<queue>" : [ "queue" ],
        "<deque>" : [ "deque" ],
        "<map>" : ["map"],
        "<unordered_map>" : ["unordered_map"],
        "<cstdio>" : ["printf", "scanf"]
    }

    DEFINE_KEYWORDS = {
        "len(x) (int)(x).size()" : [ "len" ]
    }


    def add_requires(line_tokens, require_tokens, require):
        if not require in requires:
            for tok in require_tokens:
                if tok in line_tokens:
                    requires.add(require)


    def add_defines(line_tokens, define_tokens, word):
        if not word in defines:
            for tok in define_tokens:
                if tok in line_tokens:
                    defines.add(word)


    using_namespace_std = False
    for line in lines:
        if not using_namespace_std and line.find("using namespace std;") != -1:
            using_namespace_std = True

        tokens = smart_split(line, " :<>()")
        for require in REQUIRE_KEYWORDS:
            add_requires(tokens, REQUIRE_KEYWORDS[require], require)

        for define in DEFINE_KEYWORDS:
            add_defines(tokens, DEFINE_KEYWORDS[define], define)


    prepend = []
    for r in requires:
        prepend.append("#include %s" % r)

    included = set()
    for line in lines:
        for p in prepend:
            if line.find(p) != -1:
                included.add(p);

    prepend = list(filter(lambda w: w not in included, [ p for p in prepend]))
    prepend.sort()

    for d in defines:
        prepend.append("#define %s" % d)

    if not using_namespace_std and requires:
        prepend.append("using namespace std;");




    return prepend

