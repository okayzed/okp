from __future__ import print_function
from future.utils import raise_

import re
import os
import tempfile
import shutil
import shlex
import subprocess
import sys

from . import pipeline
from . import analysis
from . import util
from . import config
from . import single_header

CXX = os.environ.get("CXX", "g++")

def print_lines(lines):
    print('\n'.join(lines))

def extract_hidden(lines):
    scope_stack = []
    h_lines, cpp_lines = [],[]
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("class") or line.strip().startswith("namespace"):
            # "namespace Foo:" or "class Bar(Baz):"
            # namespace Foo:
            #   class Bar : public Baz:
            #     Bar() : Baz():
            #       pass
            #     def qux():
            # "Foo::Bar::qux()"
            scope = line.split(":")[0].split()[-1]
            scope_stack.append(scope)
        if line.strip() == "@hidden":
            i += 1
            line = lines[i]
            # first line after @hidden should be a method declaration
            target_indent = util.get_indent(line)
            # first token is type (int, bool, etc) or "def"
            tokens = line.lstrip().split()
            prefix = "::".join(scope_stack) + "::"
            # ex: "int Foo::Bar::qux():"
            new_line = tokens[0] +" "+ prefix + " ".join(tokens[1:]) + "\n"
            cpp_lines.append(new_line)
            i += 1
            while i < len(lines) and util.get_indent(lines[i]) >= target_indent:
                cpp_lines.append(lines[i][target_indent:])
                i += 1
        else:
            h_lines.append(line)
            i += 1
    print(cpp_lines)
    return h_lines, cpp_lines

def process_file(fname):
    basedir, name = os.path.split(fname)
    with open(fname) as f:
        lines = f.readlines()

    h_lines, cpp_lines = extract_hidden(lines)

    fname = os.path.normpath(os.path.abspath(fname))
    h_lines = pipeline.pipeline(h_lines, basedir, fname=fname)
    cpp_lines = pipeline.pipeline(cpp_lines, basedir, fname=fname)

    return h_lines, cpp_lines

def run_cmd(cmd, more_args=[], stdin=None):
    cmd_args = shlex.split(cmd)
    cmd_args.extend(more_args)
    util.debug(" ".join(cmd_args))

    if stdin:
        pipe = subprocess.Popen(cmd_args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = pipe.communicate(bytes(stdin))

        if stderr:
            print(stderr, file=sys.stderr)
        return stdout or ""

    return subprocess.check_output(cmd_args)

def process_h_file(tmp_dir, arg):
    name = arg
    fname = os.path.join(tmp_dir, arg)
    basedir = os.path.dirname(fname)

    try:
        os.makedirs(basedir)
    except:
        pass

    with open(arg) as f:
        lines = f.readlines()

    with open(fname, "w") as f:
        f.write("".join(lines))

    return

def print_file_with_line_nums(fname):
    util.debug("")
    util.debug('// ' + fname)
    with open(fname) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        util.debug(i, line.rstrip())
    util.debug("")

def compile_cpy_file(tmp_dir, arg):
    name, ext = os.path.splitext(arg)
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    return compile_cpp_file(tmp_dir, fname)

def compile_cpp_file(tmp_dir, arg):
    name, ext = os.path.splitext(arg)
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    ofname = os.path.join(tmp_dir, "%s.o" % name)

    try:
        run_cmd("%s -c '%s' -o '%s' " % (CXX, fname, ofname), COMPILE_FLAGS)
    except:
        if config.PRINT_ON_ERROR:
            print_file_with_line_nums(fname)

        e = sys.exc_info()
        print("Couldn't compile", fname, "aborting")
        sys.exit(1)
    return ofname


def add_guards(arg, lines):
    arg = arg.replace('/', '__')
    arg = arg.replace('.', '_')
    arg = arg.replace(' ', '_')
    arg = arg.upper()
    arg = "%s_H" % (arg)

    guard_line = "#ifndef %s\n#define %s" % (arg, arg)
    endif = "#endif"

    lines.insert(0, guard_line)
    lines.append(endif)


    return lines

def process_cpp_file(args, tmp_dir, arg):
    name, ext = os.path.splitext(arg)
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    ofname = os.path.join(tmp_dir, "%s.o" % name)
    hfname = os.path.join(tmp_dir, "%s.h" % name)

    args.files.append(arg)

    with open(arg) as f:
        lines = f.readlines()

    basedir = os.path.dirname(fname)

    try:
        os.makedirs(basedir)
    except:
        pass

    with open(arg) as f:
        lines = f.readlines()

    with open(fname, "w") as f:
        f.write("".join(lines))

    return ofname



def process_cpy_file(args, tmp_dir, arg, use_headers=False):
    name, ext = os.path.splitext(arg)
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    ofname = os.path.join(tmp_dir, "%s.o" % name)
    hfname = os.path.join(tmp_dir, "%s.h" % name)

    h_lines, cpp_lines = process_file(arg)
    if cpp_lines:
        cpp_lines = ['#include "{}"'.format(hfname)] + cpp_lines

    as_header = True
    if analysis.file_contains_main(h_lines):
        as_header = False
        args.files.append(fname)


    basedir = os.path.dirname(fname)

    try:
        os.makedirs(basedir)
    except:
        pass

    if (args.print_):
        print("// %s" % arg)
        print_lines(h_lines)
        print_lines(cpp_lines)
        return

    if as_header:
        header = h_lines
        header = add_guards(arg, header)

        with open(hfname, "w") as f:
            f.write("\n".join(header))
        with open(fname, "w") as f:
            f.write("\n".join(cpp_lines))
    else:
        if cpp_lines:
            with open(hfname, "w") as f:
                f.write("\n".join(h_lines))
            with open(fname, "w") as f:
                f.write("\n".join(cpp_lines))
        else:
            with open(fname, "w") as f:
                f.write("\n".join(h_lines))



def process_files(tmp_dir, args):
    args.files = analysis.gather_files(args.files)
    files = list(args.files)
    # if we have multiple files, we have to generate their headers
    use_headers = len(files) > 1
    args.files = []

    for arg in files:
        if arg == '-':
            lines = sys.stdin.readlines()
            lines = pipeline.pipeline(lines, fname="<stdin>")
            print_lines(lines)
        else:
            util.verbose("processing", arg)
            if arg.endswith(".cpy") or arg.endswith(".okp"):
                process_cpy_file(args, tmp_dir, arg, use_headers)
            if arg.endswith(".cpp") or arg.endswith(".c"):
                process_cpp_file(args, tmp_dir, arg)
            if arg.endswith(".h"):
                process_h_file(tmp_dir, arg)

def compile_files(tmp_dir, args):
    cur_dir = os.getcwd()
    outname = args.exename or "./a.out"
    if outname[0] != '/':
        outname = os.path.join(cur_dir, outname)

    files = args.files

    more_than_stdin = False
    for arg in files:
        if arg != '-':
            more_than_stdin = True

    ofiles = []
    for arg in files:
        if arg != '-':
            if arg.endswith(".cpy") or arg.endswith(".okp"):
                ofiles.append(compile_cpy_file(tmp_dir, arg))
            if arg.endswith(".cpp"):
                ofiles.append(compile_cpp_file(tmp_dir, arg))
            if arg.endswith(".c"):
                ofiles.append(compile_c_file(tmp_dir, arg))

    if args.single_header:
        os.chdir(tmp_dir)
        single_header.compile(files, outname)

    if not args.single_header and not args.print_ and more_than_stdin and not args.noexe:
        os.chdir(tmp_dir)
        util.verbose("generating", outname)
        cmd_args = ofiles + [ "-o", outname ] + COMPILE_FLAGS
        run_cmd(CXX, cmd_args)

    if config.RUN_EXE:
        if config.RUN_WITH_INPUT:
            output = run_cmd(outname, stdin=sys.stdin.read())
        else:
            output = run_cmd(outname)
        util.debug('OUTPUT:\n')
        util.debug(output.decode("utf-8"))


# we need a two pass compilation so we correctly build
# all necessary header files before compiling
COMPILE_FLAGS=""
def compile_project(args):
    global COMPILE_FLAGS
    flags = []
    files = []
    for file in args.files:
        if file[0] == '-' and file != '-':
            flags.append(file)
        else:
            files.append(file)

    COMPILE_FLAGS = flags
    COMPILE_FLAGS.extend(config.COMPILER_FLAGS)

    if COMPILE_FLAGS:
        util.debug("compile flags:", " ".join(COMPILE_FLAGS))

    if args.dir:
        tmp_dir = os.path.abspath(args.dir)
        try:
            os.makedirs(tmp_dir)
        except OSError:
            pass
    else:
        tmp_dir = tempfile.mkdtemp()
    util.verbose("working tmp dir is", tmp_dir)


    try:
        process_files(tmp_dir, args)

        if not (args.print_) and not args.transpile:
            ofiles = compile_files(tmp_dir, args)
    finally:
        if not config.KEEP_DIR and not args.dir:
            util.verbose("removing", tmp_dir)
            shutil.rmtree(tmp_dir)
        else:
            util.debug("compiled into", tmp_dir)
