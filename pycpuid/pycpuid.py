#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) Bram de Greve <bram.degreve@bramz.net>
# Copyright (c) Flight Data Services Ltd
# http://www.flightdataservices.com
# See the file "LICENSE" for the full license governing this code.

import sys
import _pycpuid
import struct as _struct

EXTENDED_OFFSET = 0x80000000


def cpuid(infotype):
    '''
    cpuid(infotype) -> (eax, ebx, ecx, edx)
    '''
    return _pycpuid.cpuid(infotype)


def vendor():
    a, b, c, d = cpuid(0)
    return _struct.pack("III", b, d, c)


def stepping_id():
    return cpuid(1)[0] & 0xf


def model():
    a = cpuid(1)[0]
    model_number = (a >> 4) & 0xf
    extended_model = (a >> 16) & 0xf
    return (extended_model << 4) + model_number


def family():
    a = cpuid(1)[0]
    family_code = (a >> 8) & 0xf
    extended_family = (a >> 20) & 0xff
    return extended_family + family_code


def processor_type():
    return (cpuid(1)[0] >> 12) & 0x3


def brand_id():
    return cpuid(1)[1] & 0xff


def brand_string():
    a = cpuid(EXTENDED_OFFSET)
    assert a >= (EXTENDED_OFFSET | 0x4), "brand string is not supported by this CPU"
    s = ''.join([_struct.pack("IIII", *cpuid(EXTENDED_OFFSET | k)) for k in 0x2, 0x3, 0x4])
    return s[:s.index('\0')]


def features():
    '''
    features() -> [str, str, ...]
    returns sequence of available features
    '''
    info = cpuid(1)
    return [key for key, reg, bit in _feat_table if info[reg] & (1 << bit)]

_feat_table = [
    ("FPU", 3, 0),
    ("VME", 3, 1),
    ("DE", 3, 2),
    ("PSE", 3, 3),
    ("TSC", 3, 4),
    ("MSR", 3, 5),
    ("PAE", 3, 6),
    ("MCE", 3, 7),
    ("CX8", 3, 8),
    ("APIC", 3, 9),
    ("SEP", 3, 11),
    ("MTRR", 3, 12),
    ("PGE", 3, 13),
    ("MCA", 3, 14),
    ("CMOV", 3, 15),
    ("PAT", 3, 16),
    ("PSE36", 3, 17),
    ("PSN", 3, 18),
    ("CLFLSH", 3, 19),
    ("DS", 3, 21),
    ("ACPI", 3, 22),
    ("MMX", 3, 23),
    ("FXSR", 3, 24),
    ("SSE", 3, 25),
    ("SSE2", 3, 26),
    ("SS", 3, 27),
    ("HTT", 3, 28),
    ("TM", 3, 29),
    ("PBE", 3, 31),
    ("SSE3", 2, 0),
    ("PCLMULDQ", 2, 1),
    ("DTES64", 2, 2),
    ("MONITOR", 2, 3),
    ("DSCPL", 2, 4),
    ("VMX", 2, 5),
    ("SMX", 2, 6),
    ("EST", 2, 7),
    ("TM2", 2, 8),
    ("SSE3", 2, 9),
    ("CNXTID", 2, 10),
    ("CX16", 2, 13),
    ("XTPR", 2, 14),
    ("PDCM", 2, 15),
    ("DCA", 2, 18),
    ("SSE4_1", 2, 19),
    ("SSE4_2", 2, 20),
    ("X2APIC", 2, 21),
    ("MOVBE", 2, 22),
    ("POPCNT", 2, 23),
    ("AES", 2, 25),
    ("XSAVE", 2, 26),
    ("OSXSAVE", 2, 27),
    ]


def _init():
    if __name__ == '__main__':
        mod = sys.modules['__main__']
    else:
        mod = sys.modules['pycpuid']
    info = cpuid(0)
    for key, reg, bit in _feat_table:
        has_feat = (info[reg] & (1 << bit)) != 0
        mod.__dict__['HAS_' + key] = has_feat

_init()

if __name__ == "__main__":
    print "Vendor:", vendor()
    print "Stepping ID:", stepping_id()
    print "Model:", hex(model())
    print "Family:", family()
    print "Processor Type:", processor_type()
    print "Brand ID:", hex(brand_id())
    print "Brand String:", brand_string()
    print "Features:", features()
