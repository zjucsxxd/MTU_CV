#!/usr/bin/python

import sys
sys.path.append("..")

import cv2
import segmentation.seqscanseg as segalg
import segprops

def filterAndShowSegments(img, segsProps):
	for key in segsProps:
		segProps = segsProps[key]
		if (segProps.S > 500 and segProps.maxI > 190):
			print (segProps.x0, segProps.y0, segProps.x1, segProps.y1, segProps.maxI)
			cv2.rectangle(img, (segProps.x0, segProps.y0), 
							(segProps.x1, segProps.y1), (155, 155, 155))
	cv2.namedWindow("my")
	cv2.imshow("my", img)
	cv2.waitKey()

def main():
	img = cv2.imread("../segmentation/proc_src/seqscan_test3.png")
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	segmap = segalg.seqScanSeg(img, 31)
	segsProps = segprops.extractSegProps(segmap, img)
	filterAndShowSegments(img, segsProps)	

if (__name__ == '__main__'):
	main()
