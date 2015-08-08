/*
Copyright (c) Bram de Greve <bram.degreve@bramz.net> 
Copyright (c) Flight Data Services Ltd
Copyright (c) 2015 Michael Mohr <akihana@gmail.com>
http://www.flightdataservices.com
See the file "LICENSE" for the full license governing this code.
*/

#include <Python.h>

#ifdef _MSC_VER
#include <intrin.h>
#elif defined(__i386__) || defined(__x86_64__)
#include <cpuid.h>
#endif

static PyObject *_pycpuid_cpuid(PyObject* module, PyObject* args) {
    unsigned int infotype = 0;
    unsigned int cpuinfo[4] = { 0 };

    if(!PyArg_ParseTuple(args, "I", &infotype))
        return NULL;

    #ifdef _MSC_VER
    __cpuid(cpuinfo, infotype);
    return Py_BuildValue("(IIII)", cpuinfo[0], cpuinfo[1], cpuinfo[2], cpuinfo[3]);
    #elif defined(__i386__) || defined(__x86_64__)
    if(__get_cpuid(infotype, &cpuinfo[0], &cpuinfo[1], &cpuinfo[2], &cpuinfo[3]) != 1) {
        PyErr_SetString(PyExc_RuntimeError, "Requested CPUID level not supported");
        return NULL;
    }
    return Py_BuildValue("(IIII)", cpuinfo[0], cpuinfo[1], cpuinfo[2], cpuinfo[3]);
    #else
    PyErr_SetString(PyExc_NotImplementedError, "CPUID is only supported on x86");
    return NULL;
    #endif
}

static PyMethodDef _pycpuid_methods[] = {
    { "cpuid", _pycpuid_cpuid, METH_VARARGS, "cpuid(eax) -> (eax, ebx, ecx, edx)"},
    { NULL, NULL, 0, NULL},
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_pycpuid",          /* m_name */
    "CPUID info",        /* m_doc */
    -1,                  /* m_size */
    _pycpuid_methods,    /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
};

PyMODINIT_FUNC PyInit__pycpuid(void) {
    PyObject *m;

    m = PyModule_Create(&moduledef);
    if(m == NULL)
        return NULL;
    return m;
}

#else

PyMODINIT_FUNC init_pycpuid(void) {
    (void)Py_InitModule3("_pycpuid", _pycpuid_methods, "CPUID info");
}

#endif

