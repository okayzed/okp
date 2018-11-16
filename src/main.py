from __future__ import print_function

import sys
import os

import config

def get_parser():
    import argparse

    parser = argparse.ArgumentParser(description='Process .cpy files into C++')
    parser.add_argument('-ni', '--disable-implication', help='Disables variable implication', action='store_true')
    parser.add_argument('files', nargs='*', help="List of files to process and compile")
    parser.add_argument('-o', '--output', dest='exename', default="a.out")
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
    parser.add_argument('-p', '--print', dest='print_', action="store_true")
    parser.add_argument('-c', '-ne', '--no-exe', dest='noexe', action="store_true",
        help='Compile .o files only (no main)')

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if not args.files:
        parser.print_help()
        return

    if args.disable_implication:
        transforms.variables.DECLARE_VARIABLES = False

    config.VERBOSE = args.verbose

    from project import compile_project
    compile_project(args)

if __name__ == "__main__":
    main()
