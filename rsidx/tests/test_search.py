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


@pytest.mark.parametrize('rsidlist', [
    ([544992196, 1335948438, 182553373, 1245348147, 1440788236]),
    (['544992196', '1335948438', '182553373', '1245348147', '1440788236']),
    (['rs544992196', 'rs1335948438', 'rs182553373', 'rs1245348147',
      'rs1440788236']),
    ([544992196, 1335948438, '182553373', 'rs1245348147', 'rs1440788236']),
])
def test_search(rsidlist):
    vcffile = data_file('chr17-sample.vcf.gz')
    idxfile = data_file('chr17-sample.rsidx')
    conn = sqlite3.connect(idxfile)
    outlines = list(rsidx.search.search(rsidlist, conn, vcffile))
    assert len(outlines) == 5
    outdata = [line.split('\t')[:5] for line in outlines]
    assert sorted(outdata) == sorted([
        ['17', '944196', 'rs182553373', 'G', 'A'],
        ['17', '611663', 'rs544992196', 'T', 'C'],
        ['17', '1946968', 'rs1245348147', 'T', 'C'],
        ['17', '567599', 'rs1335948438', 'C', 'T'],
        ['17', '374561', 'rs1440788236', 'G', 'T']
    ])
    conn.close()


def test_search_missing_rsid(capsys):
    rsidlist = [123456789]
    vcffile = data_file('chr17-sample.vcf.gz')
    idxfile = data_file('chr17-sample.rsidx')
    conn = sqlite3.connect(idxfile)
    outlines = list(rsidx.search.search(rsidlist, conn, vcffile))
    assert len(outlines) == 0
    conn.close()
    terminal = capsys.readouterr()
    assert '[rsidx::search] WARNING: no rsID matches' in terminal.err


def test_search_bad_rsids():
    rsidlist = [
        'rs538736078',  # replaced by . in VCF
        'rs547329663',  # replaced by bogus ID in VCF
        'rs1440788236',  # valid RSID not present in VCF
        'rs1234497371',  # valid RSID present in VCF
    ]
    vcffile = data_file('chr4-sample-corrupted-ids.vcf.gz')
    idxfile = data_file('chr4-sample-corrupted-ids.rsidx')
    conn = sqlite3.connect(idxfile)
    outlines = list(rsidx.search.search(rsidlist, conn, vcffile))
    assert len(outlines) == 1
    assert outlines[0].startswith('4\t218446\trs1234497371\tC\tCA,CAA')
    conn.close()


@pytest.mark.parametrize('doheader,numlines,suffix', [
    (False, 5, '.vcf'),
    (True, 62, '.vcf'),
    (False, 5, '.vcf.gz'),
    (True, 62, '.vcf.gz'),
])
def test_search_cli(doheader, numlines, suffix):
    with NamedTemporaryFile(suffix=suffix) as outfile:
        arglist = [
            'search', data_file('chr17-sample.vcf.gz'),
            data_file('chr17-sample.rsidx'), '--out', outfile.name,
            'rs1472751972', 'rs1287502205', 'rs897983471', 'rs1172219431',
            'rs189123651'
        ]
        args = rsidx.cli.get_parser().parse_args(arglist)
        args.header = doheader
        rsidx.search.main(args)
        with rsidx.open(outfile.name, 'r') as fh:
            outlines = fh.read().strip().split('\n')
            assert len(outlines) == numlines


def test_search_stdout(capsys):
    arglist = [
        'search', data_file('chr17-sample.vcf.gz'),
        data_file('chr17-sample.rsidx'), 'rs1472751972', 'rs1287502205',
        'rs897983471', 'rs1172219431', 'rs189123651'
    ]
    args = rsidx.cli.get_parser().parse_args(arglist)
    rsidx.search.main(args)
    terminal = capsys.readouterr()
    outlines = terminal.out.strip().split('\n')
    assert len(outlines) == 5
