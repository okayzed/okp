from __future__ import print_function
from future.utils import raise_


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

def print_lines(lines):
    print('\n'.join(lines))

def process_file(fname):
    basedir, name = os.path.split(fname)
    with open(fname) as f:
        lines = f.readlines()

    lines = pipeline.pipeline(lines, basedir)

    # TODO:
    # extract exports to fname.h
    # print("\n".join(exports))
    # print("/* END HEADER */")

    return lines

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
        f.write("\n".join(lines))

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
    name = arg.rstrip(".cpy")
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    return compile_cpp_file(tmp_dir, fname)

def compile_cpp_file(tmp_dir, arg):
    name = arg.rstrip(".cpp")
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    ofname = os.path.join(tmp_dir, "%s.o" % name)

    try:
        run_cmd("g++ -c '%s' -o '%s' " % (fname, ofname), COMPILE_FLAGS)
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

def process_cpp_file(tmp_dir, arg):
    name = arg.rstrip(".cpp")
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    ofname = os.path.join(tmp_dir, "%s.o" % name)
    hfname = os.path.join(tmp_dir, "%s.h" % name)

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
        f.write("\n".join(lines))

    return ofname


def process_cpy_file(args, tmp_dir, arg, use_headers=False):
    name = arg.rstrip(".cpy")
    fname = os.path.join(tmp_dir, "%s.cpp" % name)
    ofname = os.path.join(tmp_dir, "%s.o" % name)
    hfname = os.path.join(tmp_dir, "%s.h" % name)

    lines = process_file(arg)
    header = analysis.extract_header(lines)
    header = add_guards(arg, header)

    basedir = os.path.dirname(fname)

    try:
        os.makedirs(basedir)
    except:
        pass

    if use_headers:
        lines = analysis.remove_structs_and_classes(lines)
        lines.insert(0, '#include "%s"' % os.path.basename(hfname))
        with open(hfname, "w") as f:
            f.write("\n".join(header))

    if (args.print_):
        print("// %s" % arg)
        print_lines(lines)
        return

    with open(fname, "w") as f:
        f.write("\n".join(lines))



def process_files(tmp_dir, args):
    files = args.files
    # if we have multiple files, we have to generate their headers
    use_headers = len(files) > 1

    for arg in files:
        if arg == '-':
            lines = sys.stdin.readlines()
            lines = pipeline.pipeline(lines)
            print_lines(lines)
        else:
            util.verbose("processing", arg)
            if arg.endswith(".cpy"):
                process_cpy_file(args, tmp_dir, arg, use_headers)
            if arg.endswith(".cpp"):
                process_cpp_file(tmp_dir, arg)
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
            if arg.endswith(".cpy"):
                ofiles.append(compile_cpy_file(tmp_dir, arg))
            if arg.endswith(".cpp"):
                ofiles.append(compile_cpp_file(tmp_dir, arg))


    if not args.print_ and more_than_stdin and not args.noexe:
        os.chdir(tmp_dir)
        util.verbose("generating", outname)
        cmd_args = ofiles + [ "-o", outname ] + COMPILE_FLAGS
        run_cmd("g++", cmd_args)

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

    if COMPILE_FLAGS:
        util.debug("compile flags:", " ".join(COMPILE_FLAGS))

    if args.dir:
        tmp_dir = os.path.abspath(args.dir)
        os.makedirs(tmp_dir)
    else:
        tmp_dir = tempfile.mkdtemp()
    util.verbose("working tmp dir is", tmp_dir)


    try:
        process_files(tmp_dir, args)

        if not (args.print_):
            ofiles = compile_files(tmp_dir, args)
    finally:
        if not config.KEEP_DIR and not args.dir:
            util.verbose("removing", tmp_dir)
            shutil.rmtree(tmp_dir)
        else:
            util.debug("compiled into", tmp_dir)
