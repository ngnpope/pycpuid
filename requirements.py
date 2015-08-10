#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# Requirements File Parser for Setup Tools
################################################################################
# TODO: Handle version numbers for --editable/-e lines in requirement files.
# TODO: Handle extraction and merging of multiple version constraints.
################################################################################

'''
A requirements file parser that provides a method for setuptools to use
requirements specified in external requirements files.

A base requirements file is supported, and additional suffixed files can be
used to specify requirements for tests and extras.  Dependency links are
automatically combined from all requirements files found.

Basic example usage for ``requirements*.txt`` in the same directory:

    from requirements import RequirementsParser

    requirements = RequirementsParser()

    setup(
        ...
        install_requires=requirements.install_requires,
        setup_requires=requirements.setup_requires,
        tests_require=requirements.tests_require,
        extras_require=requirements.extras_require,
        dependency_links=requirements.dependency_links,
        ...
    )

The ``RequirementsParser`` class can be instantiated with a custom path,
filename prefix and file extension if required:

    requirements = RequirementsParser(path='/', name='depends', extn='conf')

A globbing approach is used to locate additional requirements files which
contain packages for use when testing or to specify optional extra packages.

For example, a file with the name ``requirements-cython.txt`` would be added to
the extra packages dictionary with the name ``cython``.

In addition, ``requirements-tests.txt`` will also be added as the packages
required for testing as well as being added as an extra with the name
``tests``.

If a file named ``dependency_links.txt`` is found in the same path as the
requirements files, dependencies listed in the file will also be added to the
dependency links generated by the requirements parser.

Support has also been added for operating system specific packages such
packages listed in ``requirements+linux.txt`` will only be installed on Linux.
The names that can be used are anything that matches strings generated by
``__import__('platform').system().lower()``.

See more information about requirements files and integration with setup.py:

- http://www.pip-installer.org/en/latest/requirements.html
- http://cburgmer.posterous.com/pip-requirementstxt-and-setuppy
'''

################################################################################
# Imports


import os
import platform
import re
import subprocess
import sys

from collections import defaultdict
from glob import glob


################################################################################
# Exports


__all__ = ['RequirementsParser']


################################################################################
# Constants


# Regular expression for stripping out flags used in requirements files:
__fs = 'Zefir'
__fl = 'always-unzip|editable|find-links|requirement|index-url|extra-index-url'
_re_sf = re.compile(r'^(?:-[%s]|--(?:%s)) *=? *' % (__fs, __fl))

# Regular expression for splitting on versions/extras in requirements files:
_re_ps = re.compile(r'^([^<>= \[]+)(?: *([<>]=?|==) *([^\[]+))?(?: *\[([^\]]+)\])?')

# Regular expression for extracting the egg name from a URL or file path:
_re_en = re.compile(r'^.*#egg=(.*)$')


################################################################################
# Helpers


def _build_filename(path, pattern, name, extn):
    '''
    Builds filenames from separate components.

    :param path: The path in which to search for requirements files.
    :type path: string
    :param pattern: The pattern for the filename.
    :type pattern: string
    :param name: The name prefix for the requirements files.
    :type name: string
    :param extn: The extension for the requirements files.
    :type extn: string
    :returns: The full filename pattern.
    :rtype: string
    '''
    return os.path.realpath(os.path.join(path, pattern % (name, extn)))


def _strip_flags(line):
    '''
    Strips flags from the line read from a requirements file.

    :param line: The line read from a requirements file.
    :type line: string
    :returns: The line with any flags stripped.
    :rtype: string
    '''
    return re.sub(_re_sf, '', line)


def _split_package(package):
    '''
    Splits a package string into four parts: The name, comparision operator,
    version string and extras list.

    :param package: The package name to split.
    :type package: string
    :returns: A tuple of name, operator, version and extras.
    :rtype: tuple
    '''
    matches = re.match(_re_ps, package)
    if not matches:
        return None
    components = list(matches.groups())
    components = list(map(lambda x: '' if x is None else x.strip(), components))
    if components[-1]:
        components[-1] = sorted(map(str.strip, components[-1].split(',')))
    else:
        components[-1] = []
    return components


def _extract_egg_names(line):
    '''
    Extracts the python egg name from the line containing a URL or file path.

    :param package: The line to extract the egg name from.
    :type package: string
    :returns: The egg name for the package specified in the requirements file.
    :rtype: string or none
    '''
    return re.sub(_re_en, r'\1', line)


def _read_requirements_file(filename, data=None):
    '''
    Reads requirements files and extracts data.

    :param filename: The name of the requirements file to read.
    :type filename: string
    :param data: The data extracted from the requirements file (for recursion).
    :type data: defaultdict(list)
    :returns: A dictionary of requirements information.
    :rtype: dict
    '''
    # Create a datastructure to store requirements information if required.
    if not data:
        data = defaultdict(list)

    # Keep track of this file so we can prevent infinite recursion:
    data['r'].append(filename)

    with open(filename, 'r') as f:

        for line in f:

            line = line.strip()

            # Ignore blank or commented lines:
            if not line or line.startswith('#'):
                continue

            # Skip over no-longer used options that may still exist in files:
            if line.startswith('-Z') or line.startswith('--always-unzip'):
                continue

            # Handle editable requirements:
            if line.startswith('-e') or line.startswith('--editable'):
                line = _strip_flags(line)
                data['e'].append(line)
                continue

            # Handle dependency links:
            if line.startswith('-f') or line.startswith('--find-links'):
                line = _strip_flags(line)
                data['f'].append(line)
                continue

            # Handle additional requirements files:
            if line.startswith('-r') or line.startswith('--requirement'):
                line = _strip_flags(line)
                filename = os.path.realpath(line)

                # Ensure that we do not have circular requirements:
                if filename in data['r']:
                    continue

                # Read in and merge the extra requirements:
                _read_requirements_file(filename, data)
                continue

            # Handle package index URL:
            if line.startswith('-i') or line.startswith('--index-url'):
                line = _strip_flags(line)
                data['i'] = [line]
                continue

            # Handle extra package index URLs:
            if line.startswith('--extra-index-url'):
                line = _strip_flags(line)
                data['i'].append(line)
                continue

            # Handle packages (removing duplicates or less specific versions):
            components = _split_package(line)
            if not components:
                # FIXME: Something went wrong, ignore for now...
                continue
            # Compare against all other packages:
            updated = False
            for package in data['_']:
                # Only act if packages have the same name:
                cached_name = package[0].lower().replace('_', '-')
                current_name = components[0].lower().replace('_', '-')
                if cached_name == current_name:  # attempt to update if names match
                    if not package[1]:  # cached package has no operator
                        if components[1]:  # have a more specific package
                            package[1:2] = components[1:2]
                    else:  # cached package has an operator
                        if not components[1]:  # have a less specific package
                            pass  # just fall through and update extras
                        elif package[1] == components[1]:  # matching operator
                            if package[2] != components[2]:  # differing versions
                                continue
                        else:  # conflicting operators... help!
                            # FIXME: Find a solution or report an error?
                            continue
                    # Update list of extras:
                    package[3] = sorted(list(set(package[3] + components[3])))
                    updated = True
                    break
            if not updated:
                # Nothing updated, so append:
                data['_'].append(components)

    # Combine package versions and names from the cache:
    packages = []
    for package in data['_']:
        if package[-1]:
            extras = ', '.join(package[-1])
            packages.append('%s%s%s [%s]' % tuple(package[:-1] + [extras]))
        else:
            packages.append('%s%s%s' % tuple(package[:-1]))
    data['p'] = sorted(packages)

    return data


################################################################################
# Parser


class RequirementsParser(object):
    '''
    Parser for requirements files providing helpful properties for populating
    the setuptools setup() function with requirements based on requirements
    files.
    '''

    def __init__(self, path='', name='requirements', extn='txt'):
        '''
        Initialise the parser and parse requirements.

        :param path: The path in which to search for requirements files.
        :type path: string
        :param name: The name prefix for the requirements files.
        :type name: string
        :param extn: The extension for the requirements files.
        :type extn: string
        '''
        self.data = {}
        self.links = []
        self.platform = platform.system().lower()

        # Handle dependency links file if available:
        filename = _build_filename(path, '%s.%s', 'dependency_links', 'txt')
        if os.path.isfile(filename):
            lines = open(filename, 'r').read().splitlines()
            self.links = list(map(str.strip, lines))

        paths = []
        paths += [_build_filename(path, '%s.%s', name, extn)]
        paths += glob(_build_filename(path, '%s[+-]*.%s', name, extn))

        for f in paths:
            if not os.path.isfile(f):
                continue

            # Extract extras name and operating system name:
            m = re.search(r'(?:-(\w+))?(?:\+(\w+))?\.%s$' % extn, f)
            if not m:
                continue
            source, system = m.groups()

            # Ensure that we don't include packages for other operating systems:
            if system and not system == self.platform:
                continue

            if not source:
                source = '*'

            # If we already have some data, pass it in to be updated:
            if source in self.data:
                self.data[source] = _read_requirements_file(f, self.data[source])
            else:
                self.data[source] = _read_requirements_file(f)

    @property
    def install_requires(self):
        '''
        Extracts requirements for installation from parsed requirements files.

        :returns: The requirements for installation from the requirements files.
        :rtype: list
        '''
        if '*' not in self.data:
            return []
        data = self.data['*']
        install_requires = []
        install_requires += data.get('p', [])
        install_requires += list(map(_extract_egg_names, data.get('e', [])))
        return sorted(list(set(install_requires)))

    @property
    def setup_requires(self):
        '''
        Extracts requirements for setup from parsed requirements files.

        :returns: The requirements for setup from the requirements files.
        :rtype: list
        '''
        if 'setup' not in self.data:
            return []
        data = self.data['setup']
        setup_requires = []
        setup_requires += data.get('p', [])
        setup_requires += list(map(_extract_egg_names, data.get('e', [])))
        return sorted(list(set(setup_requires)))

    @property
    def tests_require(self):
        '''
        Extracts requirements for tests from parsed requirements files.

        :returns: The requirements for tests from the requirements files.
        :rtype: list
        '''
        if 'tests' not in self.data:
            return []
        data = self.data['tests']
        tests_require = []
        tests_require += data.get('p', [])
        tests_require += list(map(_extract_egg_names, data.get('e', [])))
        return sorted(list(set(tests_require)))

    @property
    def extras_require(self):
        '''
        Extracts requirements for extras from parsed requirements files.

        :returns: The requirements for extras from the requirements files.
        :rtype: dict
        '''
        extras_require = {}
        for source in self.data.keys():
            data = self.data[source]
            if source == '*':
                continue
            packages = []
            packages += data.get('p')
            packages += list(map(_extract_egg_names, data.get('e', [])))
            packages = sorted(list(set(packages)))
            if packages:
                extras_require[source] = packages
        return extras_require

    @property
    def dependency_links(self):
        '''
        Extracts dependency links from parsed requirements files.

        :returns: The dependency links from the requirements files.
        :rtype: list
        '''
        dependency_links = []
        dependency_links += self.links
        for data in self.data.values():
            dependency_links += data.get('f', [])
            dependency_links += data.get('e', [])
        return sorted(list(set(dependency_links)))


################################################################################
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4
