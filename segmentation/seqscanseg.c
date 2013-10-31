#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>
#include <stdint.h>
#include <numpy/arrayobject.h>
#include "seqscanseg.h"

static PyObject *seqscanseg(PyObject *, PyObject *);

static PyMethodDef SeqScanSegMethods[] = {
	{"seqScanSeg", seqscanseg, METH_VARARGS, "Sequence scanline segmentation"},
	{NULL, NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initseqscanseg(void) {
	(void) Py_InitModule("seqscanseg", SeqScanSegMethods);
	import_array();
}

typedef struct _Segment {
	unsigned int id;
	unsigned long sumI;
	unsigned int pxls;
} Segment;

static void segmentateDecorator(PyArrayObject *src, PyArrayObject *dst, int delta) {
	int nd = PyArray_NDIM(src);
	npy_intp *dims = PyArray_DIMS(src);
	int step = (nd == 3) ? dims[2] : 1;
	uint32_t *dstData = PyArray_BYTES(dst);
	uint8_t *srcData = PyArray_BYTES(src);

	segmentate(srcData, step, dstData, dims[1], dims[0], delta);	
}

static PyObject* seqscanseg(PyObject *self, PyObject *args) {
	PyArrayObject *ptr;
	PyObject *rslt;
	unsigned int delta;
	
	if (!PyArg_ParseTuple(args, "OI", &ptr, &delta)) {
		return NULL;
	}
 
 	if (!(rslt = PyArray_SimpleNew(2, PyArray_DIMS(ptr), NPY_INT32))) {
    	return NULL;
  	}

  	segmentateDecorator(ptr, rslt, (delta));
	return rslt;
}

#ifdef __cplusplus
}
#endif
