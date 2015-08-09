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
#include <stdio.h>
#include <sched.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <cpuid.h>
#endif

static PyObject *_pycpuid_cpuid(PyObject* module, PyObject* args) {
    #if defined(__i386__) || defined(__x86_64__)
    pid_t pid;
    cpu_set_t saved, target;
    #endif
    int cpu_num = 0;
    unsigned int level = 0;
    unsigned int info[4] = { 0 };

    if(!PyArg_ParseTuple(args, "I|i", &level, &cpu_num))
        return NULL;

    #ifdef _MSC_VER

    /* Handling CPU affinity on Windows is not supported.  Patches welcome. */
    __cpuid(info, level);
    return Py_BuildValue("(IIII)", info[0], info[1], info[2], info[3]);

    #elif defined(__i386__) || defined(__x86_64__)

    pid = syscall(__NR_gettid);
    if(sched_getaffinity(pid, sizeof(cpu_set_t), &saved) != 0) {
        PyErr_SetString(PyExc_RuntimeError, "Unable to get CPU affinity");
        return NULL;
    }

    CPU_ZERO(&target);
    CPU_SET(cpu_num, &target);
    if(sched_setaffinity(pid, sizeof(cpu_set_t), &target) != 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    if(__get_cpuid(level, &info[0], &info[1], &info[2], &info[3]) != 1) {
        PyErr_SetString(PyExc_RuntimeError, "CPUID level not supported");
        return NULL;
    }

    if(sched_setaffinity(pid, sizeof(cpu_set_t), &saved) != 0) {
        PyErr_SetFromErrno(PyExc_OSError);
        return NULL;
    }

    return Py_BuildValue("(IIII)", info[0], info[1], info[2], info[3]);
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

