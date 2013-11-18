#!/usr/bin/python

import cv2
import segmentation.seqscanseg as segalg
import segprops.segprops as segprops

frm = 0

def filterAndShowSegments(img, segsProps):
    global frm
    for key in segsProps:
        segProps = segsProps[key]
        if (segProps.S > 50 and segProps.maxI > 190 and segProps.S < 36000):
            cv2.rectangle(img, (segProps.x0, segProps.y0), (segProps.x1, segProps.y1), (155, 155, 155))
            cv2.circle(img, (segProps.yS, segProps.xS), 10, (255, 255, 255))
            print segProps.xS / segProps.S, segProps.yS / segProps.S
        if (segProps.S == 50000):
            print segProp.S, frm

def main():
	global frm
	cap = cv2.VideoCapture("../Astrohn_auto.mp4")
	cv2.namedWindow("Window")
	
	while (cv2.waitKey(30) == -1):
		(ret, img) = cap.read()
		frm = frm + 1
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		(ret, img) = cv2.threshold(img, 150, 255, cv2.THRESH_TOZERO)
		segmap = segalg.seqScanSeg(img, 50)
		segsProps = segprops.extractSegProps(segmap, img)
		filterAndShowSegments(img, segsProps)	
		cv2.imshow("Window", img)

if (__name__ == '__main__'):
	main()
