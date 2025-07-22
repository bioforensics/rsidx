#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import builtins
from contextlib import contextmanager
from gzip import open as gzopen
import sys

from rsidx import index
from rsidx import search
from rsidx import __main__
from rsidx import cli

from . import _version
__version__ = _version.get_versions()['version']


@contextmanager
def open(filename, mode):
    if mode not in ('r', 'w'):
        raise ValueError('invalid mode "{}"'.format(mode))
    if filename in ['-', None]:
        filehandle = sys.stdin if mode == 'r' else sys.stdout
        yield filehandle
    else:
        openfunc = builtins.open
        if filename.endswith('.gz'):
            openfunc = gzopen
            mode += 't'
        with openfunc(filename, mode) as filehandle:
            yield filehandle
