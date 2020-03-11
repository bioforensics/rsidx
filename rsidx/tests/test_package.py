#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import rsidx
import pytest
from tempfile import NamedTemporaryFile


def test_open():
    with NamedTemporaryFile() as tf:
        with pytest.raises(ValueError, match=r'invalid mode "rwx"'):
            with rsidx.open(tf.name, 'rwx') as fh:
                pass
