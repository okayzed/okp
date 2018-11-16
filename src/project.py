import os
import tempfile
import shutil
import shlex
import subprocess

from pipeline import pipeline
import analysis
import sys
import util

import config

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
    util.verbose(" ".join(cmd_args))
    return subprocess.check_output(cmd_args)

def compile_project(args):
    files = args.files
    outname = args.exename or "./a.out"

    tmp_dir = tempfile.mkdtemp()
    util.verbose("working tmp dir is", tmp_dir)

    # if we have multiple files, we have to generate their headers
    use_headers = len(files) > 1
    cur_dir = os.getcwd()
    if outname[0] != '/':
        outname = os.path.join(cur_dir, outname)

    more_than_stdin = False

    ofiles = []

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

                ofiles.append(ofname)

                lines = process_file(arg)
                header = analysis.extract_header(lines)

                basedir = os.path.dirname(fname)

                try:
                    os.makedirs(basedir)
                except:
                    pass

                if use_headers:
                    lines = analysis.remove_structs(lines)
                    lines.insert(0, '#include "%s"' % os.path.basename(hfname))
                    with open(hfname, "w") as f:
                        f.write("\n".join(header))

                if (args.print_):
                    print("// %s" % arg)
                    print_lines(lines)
                    continue

                with open(fname, "w") as f:
                    f.write("\n".join(lines))


                run_cmd("g++ -c '%s' -o '%s'" % (fname, ofname))

        if not args.print_ and more_than_stdin and not args.noexe:
            os.chdir(tmp_dir)
            util.verbose("generating", outname)
            run_cmd("g++ -o '%s'" % outname, ofiles)
    finally:
        if not config.KEEP_DIR:
            util.verbose("removing", tmp_dir)
            shutil.rmtree(tmp_dir)
        else:
            util.debug("compiled into", tmp_dir)



