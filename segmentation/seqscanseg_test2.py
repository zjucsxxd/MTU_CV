import sys
sys.path.append("..")

import segprops.segprops as segprops

import cv2
import cv
import componentsUtils as cmpUtls
import seqscanseg
import numpy as np
import random 

def getRandomColor(srcI):
	r = srcI
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return (r, (g + 155) / 2, (b + 155) / 2)

def colorizeComponents(compMat, segProps, colors = {}):
	out = np.zeros((compMat.shape[0], compMat.shape[1], 3))
	
	for y in range(0, out.shape[0]):
		for x in range(0, out.shape[1]):
			c = compMat.item(y, x)
			if (c != 0):
				if (colors.get(c) == None):
					colors[c] = getRandomColor(segProps[c].maxI)
				out.itemset(y, x, 0, colors[c][0])
				out[y, x, 1] = colors[c][1]
				out[y, x, 2] = colors[c][2]
	return out

def createDir(name):
	import os
	if not os.path.exists(name):
		os.makedirs(name)

def main():
	src = cv2.imread("proc_src/src_47.png")
	src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	src = cv2.medianBlur(src, 3)
	(rslt, src) = cv2.threshold(src, 170, 255, cv2.THRESH_TOZERO)
	createDir("rslt_")
	a = seqscanseg.seqScanSeg(src, 30)
	a_segProps = segprops.extractSegProps(a, src)

	dst = colorizeComponents(a, a_segProps)
	cv2.imwrite("rslt_/rslt_src_6.png", dst)
	
	
	

if (__name__ == '__main__'):
	main()
