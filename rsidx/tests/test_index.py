#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import pytest
import rsidx
from rsidx.tests import data_file
import sqlite3
from tempfile import NamedTemporaryFile


@pytest.mark.parametrize('cachesize,mmapsize', [
    (None, None),
    (4000, None),
    (None, 4000000),
    (4000, 4000000),
])
def test_index(cachesize, mmapsize):
    with NamedTemporaryFile(suffix='.sqlite3') as db:
        with sqlite3.connect(db.name) as dbconn:
            with rsidx.open(data_file('chr17-sample.vcf.gz'), 'r') as vcffh:
                rsidx.index.index(dbconn, vcffh, cache_size=cachesize,
                                  mmap_size=mmapsize, logint=10)
            c = dbconn.cursor()
            query = (
                'SELECT * FROM rsid_to_coord WHERE rsid IN '
                '(1238461543, 1472751972)'
            )
            results = list(c.execute(query))
            assert sorted(results) == sorted([
                (1238461543, '17', 624973),
                (1472751972, '17', 132359)
            ])


def test_index_bogus_rsids():
    with NamedTemporaryFile(suffix='.sqlite3') as db:
        with sqlite3.connect(db.name) as dbconn:
            vcffile = data_file('chr4-sample-corrupted-ids.vcf.gz')
            with rsidx.open(vcffile, 'r') as vcffh:
                rsidx.index.index(dbconn, vcffh)
            c = dbconn.cursor()
            query = (
                'SELECT * FROM rsid_to_coord WHERE rsid IN '
                '(538736078, 547329663, 1440788236, 1234497371)'
            )
            results = list(c.execute(query))
            assert results == [(1234497371, '4', 218446)]

def test_index_multi_rsids():
    with NamedTemporaryFile(suffix='.sqlite3') as db:
        with sqlite3.connect(db.name) as dbconn:
            vcffile = data_file('multiple_id.vcf.gz')
            with rsidx.open(vcffile, 'r') as vcffh:
                rsidx.index.index(dbconn, vcffh)
            c = dbconn.cursor()
            query = (
                'SELECT * FROM rsid_to_coord WHERE rsid IN '
                '(72634902, 145742571)'
            )
            results = list(c.execute(query))
            assert sorted(results) == sorted([
                (72634902, '1', 1900106),
                (145742571, '1', 1900106)]
            )


@pytest.mark.parametrize('mainfunc', [rsidx.index.main, rsidx.__main__.main])
def test_index_cli(mainfunc):
    with NamedTemporaryFile(suffix='.sqlite3') as db:
        arglist = ['index', data_file('chr17-sample.vcf.gz'), db.name]
        args = rsidx.cli.get_parser().parse_args(arglist)
        mainfunc(args)
        conn = sqlite3.connect(db.name)
        c = conn.cursor()
        query = (
            'SELECT * FROM rsid_to_coord WHERE rsid IN '
            '(548749810, 956322221)'
        )
        results = list(c.execute(query))
        assert sorted(results) == sorted([
            (548749810, '17', 1098730),
            (956322221, '17', 1227227)]
        )
