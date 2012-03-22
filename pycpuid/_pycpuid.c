/*
Copyright (c) Bram de Greve <bram.degreve@bramz.net> 
Copyright (c) Flight Data Services Ltd
http://www.flightdataservices.com
See the file "LICENSE" for the full license governing this code.
*/

#include <Python.h>

#ifdef _MSC_VER
#	include <intrin.h>
#endif



static PyObject* _pycpuid_cpuid(PyObject* module, PyObject* args)
{
	unsigned cpuinfo[4] = { 0 };
	unsigned infotype;
	if (!PyArg_ParseTuple(args, "I:cpuid", &infotype))
	{
		return 0;
	}
#ifdef _MSC_VER
	__cpuid(cpuinfo, infotype);
#else
    // cpuid and PIC mode don't play nice. Push ebx before use!
    // see http://www.technovelty.org/code/arch/pic-cas.html
    
    // Flight Data Services couldn't get this to build on 64-bit.
    // See http://code.google.com/p/pycpuid/source/browse/release-0.1/cpuid/cpuid.c
#   ifdef __x86_64__
	__asm__ __volatile__(
		"cpuid;"
		: "=a"(cpuinfo[0]), "=b"(cpuinfo[1]), "=c"(cpuinfo[2]), "=d"(cpuinfo[3])
		: "a"(infotype));
#   else
	__asm__ __volatile__(
		"pushl %%ebx;"
		"cpuid;"
		"movl %%ebx,%1;"
		"pop %%ebx;"
		: "=a"(cpuinfo[0]), "=m"(cpuinfo[1]), "=c"(cpuinfo[2]), "=d"(cpuinfo[3])
		: "a"(infotype));		
#	endif
#endif
	return Py_BuildValue("IIII", cpuinfo[0], cpuinfo[1], cpuinfo[2], cpuinfo[3]);
}



static PyMethodDef _pycpuid_methods[] = 
{
	{ "cpuid", _pycpuid_cpuid, METH_VARARGS, "cpuid(eax) -> (eax, ebx, ecx, edx)"},
	{ 0, 0, 0, 0 },
};



PyMODINIT_FUNC init_pycpuid(void)
{
	Py_InitModule("_pycpuid", _pycpuid_methods);
}
