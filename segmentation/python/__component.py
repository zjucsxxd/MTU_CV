#!/usr/bin/python

import unittest

class Component:
	id = 0
	sumI = 0
	pxls = 0
	parent = None
	def __init__(self, pxlI, id, parent = None):
		self.sumI = long(pxlI)
		self.pxls = long(1)
		self.id = id
		if (parent != None):
			parent.addPixel(pxlI)
		self.parent = parent
	def getAverangeI(self):
		root = self.getRoot()
		return root.sumI / root.pxls
	def addPixel(self, pxlI):
		root = self.getRoot()
		root.sumI += pxlI
		root.pxls += 1
	def addPixels(self, compB):
		self.sumI += compB.sumI
		self.pxls += compB.pxls
	def mergeComponents(self, compB):
		if (self.id == compB.id):
			return self
		if (self.id > compB.id):
			self.parent = compB
			self.getRoot().addPixels(self)
			return compB
		else:
			compB.parent = self
			compB.getRoot().addPixels(compB)
			return self
	def distToPixel(self, pxlI):
		return abs(pxlI - self.getAverangeI())
	def distToComponent(self, comp):
		return abs(comp.getAverangeI() - self.getAverangeI())
	def getRoot(self):
		if (self.parent == None):
			return self
		else:
			return self.parent.getRoot()
	def __repr__(self):
		return '[id = {0}, sumI = {1}, pxls = {2}, isRoot = {3}]'.format(self.id, self.sumI, self.pxls, self.parent == None)

class __Test(unittest.TestCase):
	a = Component(100, 1, None)
	b = Component(200, 2, None)
	c = Component(300, 3, None)

	def setUp(self):
		self.a = Component(100, 1, None)
		self.b = Component(200, 2, None)
		self.c = Component(300, 3, None)
	def testDistToPixel(self):
		self.assertEquals(self.a.distToPixel(200), 100)
		self.b.mergeComponents(self.a)
		self.c.mergeComponents(self.b)
		self.assertEquals(self.a.distToPixel(113), 87)
		self.assertEquals(self.b.distToPixel(113), 87)
		self.assertEquals(self.c.distToPixel(113), 87)
	def testDistToComponent(self):
		d = Component(100, 1, self.c)
		print d
		self.a.mergeComponents(self.b)
		self.assertEquals(self.a.distToComponent(d), 50)
		self.assertEquals(self.a.distToComponent(self.c), 50)
		self.assertEquals(self.b.distToComponent(d), 50)
		self.assertEquals(self.b.distToComponent(self.c), 50)
		self.assertEquals(self.a.distToComponent(self.b), 0)
	def testAddPixel(self):
		self.a = Component(100, 1, None)
		nb = Component(200, 2, self.a)
		self.assertEquals(self.a.getAverangeI(), 150)
		self.assertEquals(nb.getAverangeI(), 150)
		self.a.addPixel(600)
		self.assertEquals(self.a.getAverangeI(), 300)
		self.assertEquals(nb.getAverangeI(), 300)
		nb.addPixel(100)
		self.assertEquals(self.a.getAverangeI(), 250)
		self.assertEquals(nb.getAverangeI(), 250)
	def testMergeComps1(self):
		rslt = self.a.mergeComponents(self.b)
		self.assertEquals(rslt.id, 1)
		self.assertEquals(rslt.getAverangeI(), 150)
	def testMergeComps2(self):
		rslt = self.b.mergeComponents(self.a)
		self.assertEquals(rslt.id, 1)
		self.assertEquals(rslt.getAverangeI(), 150)
	def testMergeComps3(self):
		self.b.mergeComponents(self.a)
		self.c.mergeComponents(self.b)
		self.assertEquals(self.a.getAverangeI(), 200)
		self.assertEquals(self.b.getAverangeI(), 200)
		self.assertEquals(self.c.getAverangeI(), 200)
	def testMergeComps4(self):
		self.b.mergeComponents(self.a)
		self.c.mergeComponents(self.b)
		d = Component(400, 4, None)
		rslt = d.mergeComponents(self.a)
		self.assertEquals(rslt.id, self.a.id)
		self.assertEquals(rslt.getAverangeI(), 250)
		self.assertEquals(self.b.getAverangeI(), 250)
		self.assertEquals(self.c.getAverangeI(), 250)
		self.assertEquals(d.getAverangeI(), 250)
	def testMergeComps5(self):
		self.b.mergeComponents(self.a)
		self.c.mergeComponents(self.b)
		d = Component(400, 4, None)
		rslt = d.mergeComponents(self.b)
		self.assertEquals(rslt.id, self.b.id)
		self.assertEquals(rslt.getAverangeI(), 250)
		self.assertEquals(self.b.getAverangeI(), 250)
		self.assertEquals(self.c.getAverangeI(), 250)
		self.assertEquals(d.getAverangeI(), 250)
	def testMergeComps6(self):
		self.b.mergeComponents(self.a)
		self.c.mergeComponents(self.b)
		d = Component(400, 4, None)
		rslt = d.mergeComponents(self.c)
		self.assertEquals(rslt.id, self.c.id)
		self.assertEquals(rslt.getAverangeI(), 250)
		self.assertEquals(self.b.getAverangeI(), 250)
		self.assertEquals(self.c.getAverangeI(), 250)
		self.assertEquals(d.getAverangeI(), 250)
	def testMergeEqual(self):
		rslt = self.a.mergeComponents(self.a)
		self.assertEquals(rslt.id, self.a.id)
		self.assertEquals(rslt.getAverangeI(), 100)

if __name__ == '__main__':
	unittest.main()






