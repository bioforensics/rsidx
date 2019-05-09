#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2019, Battelle National Biodefense Institute.
#
# This file is part of rsidx (https://github.com/bioforensics/rsidx)
# and is licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from setuptools import setup
import versioneer


desc = 'Library for indexing VCF files for random access searches by rsID'
with open('README.md', 'r') as infile:
    longdesc = infile.read()

setup(
    name='rsidx',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=desc,
    long_description=longdesc,
    long_description_content_type='text/markdown',
    url='https://github.com/bioforensics/rsidx',
    author='Daniel Standage',
    author_email='daniel.standage@nbacc.dhs.gov',
    packages=['rsidx', 'rsidx.tests'],
    package_data={
        'rsidx': ['rsidx/tests/data/*']
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['rsidx = rsidx.__main__:main']
    },
    classifiers=[
        'Environment :: Console',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    zip_safe=True,
)
