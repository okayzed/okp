from __future__ import print_function

import sys
import os

OUTPUT_DIR=None


def get_parser():
    import argparse

    parser = argparse.ArgumentParser(description='Process .cpy files into C++')
    parser.add_argument('-ni', '--disable-implication', help='Disables variable implication', action='store_true')
    parser.add_argument('files', nargs='*', help="List of files to process and compile")
    parser.add_argument('-o', '--output', dest='exename', default="a.out")

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if not args.files:
        parser.print_help()
        return

    if args.disable_implication:
        transforms.variables.DECLARE_VARIABLES = False

    from project import compile_project
    compile_project(args.files, args.exename)

if __name__ == "__main__":
    main()
