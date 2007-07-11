/*

PyToaster - PixelToaster powered by Python
Copyright (C) 2005  Bram de Greve <bram.degreve@gmail.com>

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

*/

#include <Python.h>

typedef struct
{
	char* name;
	unsigned mask;
} 
Feature;

#define NUM_FEATS 27
#define MAX_NAME_LEN 10
static Feature features[NUM_FEATS] = 
{
	{"X87FPU", 0x00000001},
	{"VMODEE", 0x00000002},
	{"DEBEXT", 0x00000004},
	{"PGSEXT", 0x00000008},
	{"TSCOUN", 0x00000010},
	{"XXMSRS", 0x00000020},
	{"PHAEXT", 0x00000040},
	{"MCHEXT", 0x00000080},
	{"CMPXCH", 0x00000100},
	{"APICON", 0x00000200},
	{"SYSXXX", 0x00000800},
	{"MTRREG", 0x00001000},
	{"PTEBIT", 0x00002000},
	{"MCKARC", 0x00004000},
	{"CMOVIN", 0x00008000},
	{"PGATTT", 0x00010000},
	{"PGSEX2", 0x00020000},
	{"SERNUM", 0x00040000},
	{"CFLUSH", 0x00080000},
	{"DBSTOR", 0x00200000},
	{"ACPICT", 0x00400000},
	{"MMXCMP", 0x00800000},
	{"FXXSTO", 0x01000000},
	{"SSEEXT", 0x02000000},
	{"SSE2EX", 0x04000000},
	{"SSNOOP", 0x08000000},
	{"PTHERM", 0x10000000}
};

static unsigned cpu_features()
{
	unsigned result;
#ifdef _MSC_VER
	__asm
	{
		mov eax, 1
		cpuid
		mov result, edx
	}
#else
#	error implement for your compiler
#endif
	return result;
}



PyMODINIT_FUNC initpycpuid(void)
{
	PyObject* module = NULL;
	unsigned feats;
	int i, has_feat;
	char feat_string[NUM_FEATS * (MAX_NAME_LEN + 2) + 1];
	char feat_name[MAX_NAME_LEN + 5];
	
	module = Py_InitModule("pycpuid", NULL);
	if (!module) return;
	
	feats = cpu_features();
	
	feat_string[0] = '\0';	
	for (i = 0; i < NUM_FEATS; ++i)
	{
		has_feat = (feats & features[i].mask) ? 1 : 0;
		if (has_feat)
		{
			if (feat_string[0] != '\0')
			{
				strcat(feat_string, ", ");
			}
			strncat(feat_string, features[i].name, MAX_NAME_LEN);
		}

		strcpy(feat_name, "HAS_");
		strcat(feat_name, features[i].name);
		PyModule_AddIntConstant(module, feat_name, has_feat);
	}
	
	PyModule_AddStringConstant(module, "features", feat_string);
}