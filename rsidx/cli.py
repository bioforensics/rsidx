#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import rsidx


def index_subparser(subparsers):
    cli = subparsers.add_parser('index')
    cli.add_argument(
        '-f', '--force', action='store_true', help='force overwrite of index '
        'file if it already exists'
    )
    cli.add_argument(
        '-c', '--cache-size', type=int, metavar='C', help='modify default '
        'sqlite3 cache size (in KiB)'
    )
    cli.add_argument(
        '-m', '--mmap-size', type=int, metavar='M', help='activate sqlite3 '
        'memory map mode and specify mmap_size (in bytes)'
    )
    cli.add_argument('vcf', help='sorted VCF file to index')
    cli.add_argument('idx', help='index file to create')


def search_subparser(subparsers):
    cli = subparsers.add_parser('search')
    cli.add_argument('--header', action='store_true', help='print VCF headers')
    cli.add_argument(
        '-o', '--out', metavar='FILE', help='write output to specified FILE; '
        'default is terminal (stdout)'
    )
    cli.add_argument('vcf', help='sorted and indexed VCF file')
    cli.add_argument('idx', help='rsidx index file')
    cli.add_argument('rsid', nargs='+', help='rsID(s) to search')


mains = {
    'index': rsidx.index.main,
    'search': rsidx.search.main,
}

subparser_funcs = {
    'index': index_subparser,
    'search': search_subparser,
}


def get_parser():
    # https://patorjk.com/software/taag/, "Standard" font
    bubbletext = r'''
≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
           _     _
  _ __ ___(_) __| |_  __
 | '__/ __| |/ _` \ \/ /
 | |  \__ \ | (_| |>  <
 |_|  |___/_|\__,_/_/\_\

≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠≠
Invoke `rsidx index --help` and `rsidx search --help` for complete
usage instructions.
'''
    subcommandstr = ', '.join(sorted(list(mains.keys())))
    parser = ArgumentParser(
        description=bubbletext,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser._positionals.title = 'Subcommands'
    parser._optionals.title = 'Global arguments'
    parser.add_argument('-v', '--version', action='version',
                        version='rsidx v{}'.format(rsidx.__version__))
    subparsers = parser.add_subparsers(dest='subcmd', metavar='subcmd',
                                       help=subcommandstr)
    for func in subparser_funcs.values():
        func(subparsers)
    return parser
