#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import rsidx
import sqlite3
from subprocess import Popen, PIPE
import sys


def trim_rsid(rsid):
    rsidstr = str(rsid)
    if rsidstr.startswith('rs'):
        rsidstr = rsidstr[2:]
    return rsidstr


def filter_by_rsid(instream, rsidlist, header=False):
    for line in instream:
        if line.startswith('#'):
            yield line
            continue
        chrom, coord, rsids, *values = line.split('\t')
        for rsid in rsids.split(';'):
            if rsid[2:] in rsidlist:
                yield line
                break


def search(rsidlist, dbconn, vcffile, header=False):
    c = dbconn.cursor()
    rsids = ', '.join(map(trim_rsid, rsidlist))
    query = 'SELECT DISTINCT chrom,coord FROM rsid_to_coord WHERE rsid IN ({:s})'.format(rsids)

    def fmt(row):
        return '{chr:s}:{coord:d}-{coord:d}'.format(chr=row[0], coord=row[1])
    coords = [fmt(result) for result in c.execute(query)]
    if len(coords) == 0:
        print('[rsidx::search] WARNING: no rsID matches', file=sys.stderr)
        return
    coords.sort(
        key=lambda x: (x.split(':')[0], int(x.split(':')[1].split('-')[0]))
    )
    tabixcmd = ['tabix', vcffile]
    if header:
        tabixcmd.append('-h')
    tabixcmd.extend(coords)
    proc = Popen(tabixcmd, stdout=PIPE, universal_newlines=True)
    for line in filter_by_rsid(proc.stdout, rsids, header=header):
        yield line


def main(args):
    conn = sqlite3.connect(args.idx)
    with rsidx.open(args.out, 'w') as out:
        for line in search(args.rsid, conn, args.vcf, header=args.header):
            print(line, end='', file=out)
    conn.close()
