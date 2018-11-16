import os
import tempfile
import shutil
import shlex
import subprocess
import glob

from pipeline import pipeline
import analysis
import sys
import util

VERBOSE = False
def print_lines(lines):
    print('\n'.join(lines))

def process_file(fname):
    basedir, name = os.path.split(fname)
    with open(fname) as f:
        lines = f.readlines()

    lines = pipeline(lines, basedir)


    # TODO:
    # extract exports to fname.h
    # print("\n".join(exports))
    # print("/* END HEADER */")

    return lines

def run_cmd(cmd, more_args=[]):
    cmd_args = shlex.split(cmd)
    cmd_args.extend(more_args)
    if VERBOSE:
        util.debug(" ".join(cmd_args))
    return subprocess.check_output(cmd_args)

def compile_project(args):
    global VERBOSE

    VERBOSE = args.verbose

    files = args.files
    outname = args.exename or "./a.out"

    tmp_dir = tempfile.mkdtemp()

    # if we have multiple files, we have to generate their headers
    use_headers = len(files) > 1
    cur_dir = os.getcwd()
    if outname[0] != '/':
        outname = os.path.join(cur_dir, outname)

    more_than_stdin = False
    try:
        for arg in files:
            if arg == '-':
                lines = sys.stdin.readlines()
                lines = pipeline(lines)
                print_lines(lines)
            else:
                more_than_stdin = True

                name = arg.strip(".cpy")
                fname = os.path.join(tmp_dir, "%s.cpp" % name)
                ofname = os.path.join(tmp_dir, "%s.o" % name)
                hfname = os.path.join(tmp_dir, "%s.h" % name)

                lines = process_file(arg)
                header = analysis.extract_header(lines)

                if use_headers:
                    lines = analysis.remove_structs(lines)
                    lines.insert(0, '#include "%s"' % os.path.basename(hfname))

                if (args.print_):
                    print("// %s" % arg)
                    print_lines(lines)
                    continue

                with open(fname, "w") as f:
                    f.write("\n".join(lines))

                with open(hfname, "w") as f:
                    f.write("\n".join(header))

                run_cmd("g++ -c '%s' -o '%s'" % (fname, ofname))

        if not args.print_ and more_than_stdin and not args.noexe:
            os.chdir(tmp_dir)
            args = glob.glob("%s/*.o" % tmp_dir)
            run_cmd("g++ -o '%s'" % outname, args)
    finally:
        pass
        shutil.rmtree(tmp_dir)



