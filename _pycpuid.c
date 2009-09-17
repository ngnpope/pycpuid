/*

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
#	ifdef __PIC__
	// cpuid and PIC mode don't play nice.  Push ebx before use!
	// see http://www.technovelty.org/code/arch/pic-cas.html
	//
	__asm__ __volatile__(
		"pushl %%ebx;"
		"cpuid;"
		"movl %%ebx,%1;"
		"pop %%ebx;"
		: "=a"(cpuinfo[0]), "=m"(cpuinfo[1]), "=c"(cpuinfo[2]), "=d"(cpuinfo[3])
		: "a"(infotype));
#	else
	__asm__ __volatile__(
		"cpuid;"
		: "=a"(cpuinfo[0]), "=b"(cpuinfo[1]), "=c"(cpuinfo[2]), "=d"(cpuinfo[3])
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
