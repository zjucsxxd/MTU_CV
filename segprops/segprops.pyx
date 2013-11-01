# distutils: language = c++

import numpy as np
cimport numpy as np
from libcpp.map cimport map
from cython.operator cimport dereference as deref, preincrement as inc

cdef struct CSegProp:
	int id
	int S
	int hist[256]
	int x0
	int y0
	int x1
	int y1
	int sumI
	int maxI
	int minI
	int xS
	int yS

cdef class SegProp:
	cdef readonly id
	cdef readonly S
	cdef int hist[256]
	cdef readonly x0
	cdef readonly y0
	cdef readonly x1
	cdef readonly y1
	cdef readonly sumI
	cdef readonly maxI
	cdef readonly minI
	cdef readonly xS
	cdef readonly yS

	def __cinit__(self, int id):
		self.id = id

	cdef set(self, CSegProp prop):
		self.S = prop.S
		for i in range(0,256):
			self.hist[i] = prop.hist[i]
		self.x0 = prop.x0
		self.y0 = prop.y0
		self.x1 = prop.x1
		self.y1 = prop.y1
		self.sumI = prop.sumI
		self.maxI = prop.maxI
		self.minI = prop.minI
		self.xS = prop.xS
		self.yS = prop.yS

	def getHist(self):
		cdef np.ndarray h = np.zeros([256], dtype = np.int)
		for i in range(0,256):
			h[i] = self.hist[i]
		return h

cdef void addPixel(CSegProp *prop, int x, int y, np.uint8_t srcI):
	if (prop.x0 > x):
		prop.x0 = x
	elif (prop.x1 < x):
		prop.x1 = x
	
	if (prop.y0 > y):
		prop.y0 = y
	elif (prop.y1 < y):
		prop.y1 = y
		
	prop.hist[srcI] += 1

	prop.S += 1
	prop.xS += x
	prop.yS += y
		
	if (prop.maxI < srcI):
		prop.maxI = srcI
	if (prop.minI > srcI):
		prop.minI = srcI

cdef CSegProp createSegProp(int id, np.uint8_t srcI, int x, int y):
	cdef CSegProp segprop
	segprop.id = id
	for i in range(0, 256):
		segprop.hist[i] = 0
	segprop.S = 1
	segprop.xS = x
	segprop.yS = y
	segprop.x0 = x
	segprop.y0 = y
	segprop.x1 = x
	segprop.y1 = y
	segprop.maxI = srcI
	segprop.minI = srcI
	return segprop

def extractSegProps(np.ndarray[np.int_t, ndim = 2] segmap, np.ndarray[np.uint8_t, ndim = 2] src):
	cdef np.int_t I
	cdef map[int, CSegProp] segsProps
	cdef CSegProp segProps
	cdef SegProp prop

	rslt = {};

	for x in range(segmap.shape[1]):
		for y in range(segmap.shape[0]):
			I = segmap[y, x]
			if (I != 0):
				if (segsProps.find(I) == segsProps.end()):
					segProps = createSegProp(I, src[y,x], x, y)
					segsProps[I] = segProps
				else:
					addPixel(&segsProps[I], x, y, src[y, x])
				
	cdef map[int, CSegProp].iterator it = segsProps.begin()
	while it != segsProps.end():
		prop = SegProp(deref(it).first)
		prop.set(deref(it).second)
		rslt[deref(it).first] = prop
		inc(it)

	return rslt
