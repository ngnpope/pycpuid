'''
pycpuid - CPUID for Python
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


http://www.bramz.net/projects-code/pycpuid/
'''

import _pycpuid
import struct as _struct

def cpuid(infotype):
	"cpuid(infotype) -> (eax, ebx, ecx, edx)"
	return _pycpuid.cpuid(infotype)

def vendor():
	"returns vendor string"
	a, b, c, d = cpuid(0)
	return _struct.pack("III", b, d, c)

def features():
	"return tuple of available features"
	feats = cpuid(1)[3]
	return [key for key, mask in _feat_table if feats & mask]
	
_feat_table = [
	("FPU", 0x00000001),
	("VME", 0x00000002),
	("DE", 0x00000004),
	("PSE", 0x00000008),
	("TSC", 0x00000010),
	("MSR", 0x00000020),
	("PAE", 0x00000040),
	("MCE", 0x00000080),
	("CX8", 0x00000100),
	("APIC", 0x00000200),
	("SEP", 0x00000800),
	("MTRR", 0x00001000),
	("PGE", 0x00002000),
	("MCA", 0x00004000),
	("CMOV", 0x00008000),
	("PAT", 0x00010000),
	("PSE36", 0x00020000),
	("PSN", 0x00040000),
	("CLFLSH", 0x00080000),
	("DS", 0x00200000),
	("ACPI", 0x00400000),
	("MMX", 0x00800000),
	("FXSR", 0x01000000),
	("SSE", 0x02000000),
	("SSE2", 0x04000000),
	("SS", 0x08000000),
	("HTT", 0x10000000),
	("TM", 0x20000000),
	("PBE", 0x80000000)
	]
	
def _init():
	import sys
	mod = sys.modules['pycpuid']
	feats = cpuid(0)[3]
	for key, mask in _feat_table:
		has_feat = (feats & mask) != 0
		mod.__dict__['HAS_' + key] = has_feat
		
_init()