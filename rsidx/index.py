#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

import os
import rsidx
import sqlite3
import sys


def parse_vcf(vcfstream, updateint=1e6):
    threshold = updateint
    for n, line in enumerate(vcfstream):
        if line.startswith('#'):
            continue
        chromstr, posstr, rsids, *values = line.split('\t')
        for rsid in rsids.split(";"):
            if not rsid.startswith('rs'):
                continue
            yield int(rsid[2:]), chromstr, int(posstr)
        if n >= threshold:
            threshold += updateint
            if threshold == updateint * 10:
                updateint = threshold
            print('[rsidx::index] processed', n, 'variants', file=sys.stderr)


def index(dbconn, vcffh, cache_size=None, mmap_size=None, logint=1e6):
    c = dbconn.cursor()
    c.execute(
        'CREATE TABLE rsid_to_coord ('
        'rsid INTEGER PRIMARY KEY, '
        'chrom TEXT NULL DEFAULT NULL, '
        'coord INTEGER NOT NULL DEFAULT 0)'
    )
    if cache_size:
        c.execute('PRAGMA cache_size = -{:d}'.format(cache_size))
    if mmap_size:
        c.execute('PRAGMA mmap_size = {:d}'.format(mmap_size))  # bytes
    dbconn.commit()

    vcfstream = parse_vcf(vcffh, updateint=logint)
    c.executemany('INSERT OR IGNORE INTO rsid_to_coord VALUES (?,?,?)', vcfstream)
    dbconn.commit()


def main(args):
    if os.path.exists(args.idx):
        message = 'WARNING: index file "{:s}" exists'.format(args.idx)
        if args.force:
            message += ', overwriting'
            try:
                os.unlink(args.idx)
            except FileNotFoundError:  # prevent exploits  # pragma: no cover
                pass
        else:
            message += ', stubbornly refusing to proceed'
        print('[rsidx]', message, file=sys.stderr)
        if not args.force:
            raise SystemExit
    with rsidx.open(args.vcf, 'r') as vcffh:
        with sqlite3.connect(args.idx) as dbconn:
            index(dbconn, vcffh, cache_size=args.cache_size,
                  mmap_size=args.mmap_size)
