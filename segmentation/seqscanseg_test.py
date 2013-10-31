import cv2
import cv
import componentsUtils as cmpUtls
import seqscanseg
import numpy as np
import random 

def getRandomColor():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return ((r + 155) / 2, (g + 155) / 2, (b + 155) / 2)

def colorizeComponents(compMat, colors = {}):
	out = np.zeros((compMat.shape[0], compMat.shape[1], 3))
	
	for y in range(0, out.shape[0]):
		for x in range(0, out.shape[1]):
			c = compMat.item(y, x)
			if (c != 0):
				if (colors.get(c) == None):
					colors[c] = getRandomColor()
				out.itemset(y, x, 0, colors[c][0])
				out[y, x, 1] = colors[c][1]
				out[y, x, 2] = colors[c][2]
	return out

def createDir(name):
	import os
	if not os.path.exists(name):
		os.makedirs(name)

def main():
	#src = cv2.imread("proc_src/seqscan_test2.png")
	#src = cv2.imread("proc_src/components.png")
	src = cv2.imread("proc_src/seqscanseg_test.png")
	src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

	createDir("rslt_")
	for p in range(136, 137):
		print p
		a = seqscanseg.seqScanSeg(src, p)
		#dst = colorizeComponents(seqscanseg.seqScanSeg(src, p))
		#cv2.imwrite("rslt_/rslt" + str(p) + ".png", dst)
	
	
	

if (__name__ == '__main__'):
	main()
