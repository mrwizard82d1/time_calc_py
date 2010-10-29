#!/usr/bin/env python

"""Summarizes the time on activities completed each day."""


from __future__ import print_function
import sys

from argparse import ArgumentParser


def summarize_time(args):
    """Summarize daily time by task."""
    infile = args.infile
    outfile = args.outfile

    task_starts = infile.readlines()
    task_ends = task_starts[1:]
    print(task_starts, file=outfile)
    print(task_ends, file=outfile)


if __name__ == '__main__':
    parser = ArgumentParser(description='Summarize daily time by task.')
    parser.add_argument('-i', '--infile', default=sys.stdin,
                        type=open,
                        help='Specify input file (default=STDIN).')
    parser.add_argument('-o', '--outfile', default=sys.stdout,
                        type=open,
                        help='Specify output file (default=STDOUT).')
    args = parser.parse_args()

    summarize_time(args)

    
