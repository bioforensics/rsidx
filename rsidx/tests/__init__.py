#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from contextlib import contextmanager
import os
from pkg_resources import resource_filename
from tempfile import NamedTemporaryFile


def data_file(path):
    pathparts = path.split('/')
    relpath = os.path.join('tests', 'data', *pathparts)
    return resource_filename('rsidx', relpath)


@contextmanager
def TempFileName(*args, **kwds):
    with NamedTemporaryFile(*args, **kwds) as tf:
        os.unlink(tf.name)
        try:
            yield tf.name
        finally:
            pass
