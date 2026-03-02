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
from importlib.resources import files
from tempfile import NamedTemporaryFile


def data_file(path):
    return str(files("rsidx") / "tests" / "data" / path)


@contextmanager
def TempFileName(*args, **kwds):
    with NamedTemporaryFile(*args, **kwds) as tf:
        os.unlink(tf.name)
        try:
            yield tf.name
        finally:
            pass
