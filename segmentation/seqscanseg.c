#ifdef __cplusplus
extern "C" {
#endif

#include <Python.h>
#include <stdint.h>
#include <numpy/arrayobject.h>

static PyObject *seqscanseg(PyObject *, PyObject *);

static PyMethodDef SeqScanSegMethods[] = {
	{"seqScanSeg", seqscanseg, METH_VARARGS, "Sequence scanline segmentation"},
	{NULL, NULL, NULL, 0, NULL}
}

PyMODINIT_FUNC
initseqscanseg(void) {
	(void) Py_InitModule("seqscanseg", SeqScanSegMethods);
	import_array();
}

static void segmentate(PyArrayObject *src, PyArrayObject *dst) {
	
}

static PyObject* seqscanseg(PyObject *self, PyObject *args) {
	PyArrayObject *ptr;
	PyObject *rslt;

	if (!PyArg_ParseTuple(args, "O", &ptr)) {
		return NULL;
	}
 
 	if (!(rslt = PyArray_SimpleNew(2, PyArray_DIMS(ptr), NPY_INT32))) {
    	return NULL;
  	}

	markComponents(ptr, rslt);
	return rslt;
}

#ifdef __cplusplus
}
#endif