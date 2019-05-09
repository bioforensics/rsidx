#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import argparse
import rsidx
import sys


def main(args=None):
    """Entry point for the happer CLI.

    Isolated as a method so that the CLI can be called by other Python code
    (e.g. for testing), in which case the arguments are passed to the function.
    If no arguments are passed to the function, parse them from the command
    line.
    """
    if args is None:  # pragma: no cover
        if len(sys.argv) == 1:
            rsidx.cli.get_parser().parse_args(['-h'])
        args = rsidx.cli.get_parser().parse_args()

    versionmessage = '[rsidx] running version {}'.format(rsidx.__version__)
    print(versionmessage, file=sys.stderr)
    mainmethod = rsidx.cli.mains[args.subcmd]
    mainmethod(args)
