#!/usr/bin/python

import unittest

cdef class Component:
	cdef public int id
	cdef int sumI
	cdef int pxls
	cdef Component parent

	cpdef double getAverangeI(self)
	cpdef addPixel(self, int pxlI)
	cpdef addPixels(self, Component compB)
	cpdef Component mergeComponents(self, Component compB)
	cpdef double distToPixel(self, int pxlI)
	cpdef double distToComponent(self, Component comp)
	cpdef Component getRoot(self)

