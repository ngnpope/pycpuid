#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) Bram de Greve <bram.degreve@bramz.net>
# Copyright (c) Flight Data Services Ltd
# http://www.flightdataservices.com
# See the file "LICENSE" for the full license governing this code.

# Ensure PyCPUID 0.3 and later has the same namespace as previous version while
# allowing setup.py and Sphinx to get at the meta data prior to the C extension
# being built.
try:
    from pycpuid import *
except ImportError:
    pass

__packagename__ = 'PyCPUID'
__version__ = '0.4'
__author__ = 'Bram de Greve'
__author_email__ = 'bram.degreve@bramz.net'
__maintainer__ = 'Flight Data Services Ltd'
__maintainer_email__ = 'developers@flightdataservices.com'
__url__ = 'http://pypi.python.org/pypi/PyCPUID'
__description__ = 'CPUID powered by Python.'
__download_url__ = 'https://github.com/FlightDataServices/PyCPUID'
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    ]
__platforms__ = ['OS Independent']
__license__ = 'GNU Library or Lesser General Public License (LGPL)'
__keywords__ = ['cpuid']

################################################################################
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
