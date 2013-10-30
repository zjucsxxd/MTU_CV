#!/usr/bin/python

import unittest
from __ccomponent cimport Component
import numpy as np
cimport numpy as np
import cv2

ctypedef np.uint8_t DTYPE

cdef getComponentId(components, np.uint8_t srcI, int upLbl, int leftLbl, int delta):
	cdef Component upCmp
	cdef Component leftCmp
	cdef int isUpLessDelta
	cdef int isLeftLessDelta
	cdef int id

	if (srcI == 0):
		return 0
	if (upLbl == 0):
		upCmp = Component(1000000, 1000000)
		isUpLessDelta = False
	else:
		upCmp = components[upLbl - 1]
		isUpLessDelta = (upCmp.distToPixel(srcI) < delta)
	
	if (leftLbl == 0):
		leftCmp = Component(1000000, 1000000)
		isLeftLessDelta = False
	else:
		leftCmp = components[leftLbl - 1]
		isLeftLessDelta = (leftCmp.distToPixel(srcI) < delta)

	if not(isUpLessDelta) and not(isLeftLessDelta):
		id = len(components) + 1
		components.append(Component(srcI, id))
		return id

	if (isUpLessDelta != isLeftLessDelta):
		if (isUpLessDelta):
			components[upLbl - 1].addPixel(srcI)
			return upLbl
		else:
			components[leftLbl - 1].addPixel(srcI)
			return leftLbl

	if (upCmp.distToComponent(leftCmp) < delta):
		return upCmp.mergeComponents(leftCmp).id
	else:
		if (upCmp.distToPixel(srcI) < leftCmp.distToPixel(srcI)):
			upCmp.addPixel(srcI)
			return upCmp.id
		else:
			leftCmp.addPixel(srcI)
			return leftCmp.id

cimport cython
@cython.boundscheck(False)
def __labelFirstRow(components, dst, np.ndarray[DTYPE, ndim=2] src, delta):
	dst[0, 0] = getComponentId(components, src[0, 0], 0, 0, delta)
	for i in range(1, src.shape[1]):
		dst[0, i] = getComponentId(components, src[0, i], 0, dst[0, i - 1], delta)

@cython.boundscheck(False)
def seqscanseg(np.ndarray[DTYPE, ndim=2] src, delta):
	cdef np.ndarray[np.int_t, ndim=2] dst = np.ndarray(shape = (src.shape[0], src.shape[1]), dtype = int)
	components = []
	cdef int ymax = src.shape[0]
	cdef int xmax = src.shape[1]
	__labelFirstRow(components, dst, src, delta)
	
	for y in range(1, ymax):
		dst[y, 0] = getComponentId(components, src[y, 0], dst[y-1, 0], 0, delta)
		for x in range(1, xmax):
			dst[y, x] = getComponentId(components, src[y, x], dst[y-1, x], dst[y, x-1], delta)

	for y in range(0, ymax):
		for x in range(0, xmax):
			if (dst[y, x] != 0):
				dst[y, x] = components[dst[y, x] - 1].getRoot().id
	return dst

class __TestGetComponentId(unittest.TestCase):
	up = Component(100, 1)
	left = Component(200, 2)
	components = []
	def setUp(self):
		self.up = Component(100, 1)
		self.left = Component(200, 2)
		self.components = [self.up, self.left]
	def testBackgroundPixel(self):
		id = getComponentId(self.components, 0, self.up.id, self.left.id, 100)
		self.assertEquals(id, 0)
	def testUpLeftBackground(self):
		id = getComponentId(self.components, 100, 0, 0, 100)
		self.assertEquals(id, 3)
		id = getComponentId(self.components, 100, self.up.id, 0, 1000)
		self.assertEquals(id, self.up.id)
		id = getComponentId(self.components, 100, 0, self.left.id, 1000)
		self.assertEquals(id, self.left.id)
	def testUpLeftMerge(self):
		id = getComponentId(self.components, 150, self.up.id, self.left.id, 101)
		self.assertEquals(id, self.up.id)
		self.assertEquals(self.left.parent.id, self.up.id)
	def testAddToLeft(self):
		id = getComponentId(self.components, 190, self.up.id, self.left.id, 11)
		self.assertEquals(id, self.left.id)
	def testAddToUp(self):
		id = getComponentId(self.components, 110, self.up.id, self.left.id, 11)
		self.assertEquals(id, self.up.id)

class __TestSeqScanSeg(unittest.TestCase):
	def testLabelFirstRow(self):
		src = cv2.imread("proc_src/seqscanseg_test.png")
		src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
		print seqscanseg(src, 2)			


if (__name__ == '__main__'):
	unittest.main()
