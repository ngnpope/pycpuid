#! /usr/bin/env python

# pycpuid - CPUID powered by Python
# Copyright (C) 2007  Bram de Greve <bram.degreve@bramz.net>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from distutils.core import setup, Extension
import os.path

_pycpuid = Extension('_pycpuid',
	sources = ['_pycpuid.c'])

setup (name = 'pycpuid',
	version = '0.2',
	description = 'CPUID powered by Python',
	author = 'Bram de Greve',
	author_email = 'bram.degreve@bramz.net',
	url = 'http://www.bramz.net/projects-code/pycpuid/',
	long_description = '''
pycpuid - CPUID powered by Python
Copyright (C) 2007-2009  Bram de Greve <bram.degreve@bramz.net>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
''',
	py_modules = ['pycpuid'],
	ext_modules = [_pycpuid],
	)

# EOF
