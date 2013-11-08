#!/usr/bin/python

import sys
sys.path.append("..")

import cv2
import cv
import segmentation.seqscanseg as segalg
import segprops.segprops as segprops


def correlation(a_file, b_file):
    a = cv2.imread("proc_src/" + a_file)
    b = cv2.imread("proc_src/" + b_file)
    a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    b = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    a_segmap = segalg.seqScanSeg(a,31)
    b_segmap = segalg.seqScanSeg(b, 31)
    a_segProps = segprops.extractSegProps(a_segmap, a)
    b_segProps = segprops.extractSegProps(b_segmap, b)
    a_hist = a_segProps[1].getHist()
    b_hist = b_segProps[1].getHist()
    return cv2.compareHist(a_hist, b_hist, cv.CV_COMP_CORREL)

def main():
    print "Self correlation =",  correlation("simple.png", "simple.png")
    print "Move correlation =",  correlation("simple.png", "simple_move.png")
    print "Rotate correlation =",  correlation("simple.png", "simple_rot.png")
    print "Scale in correlation =",  correlation("simple.png", "simple_scin.png")
    print "Scale out correlation =",  correlation("simple.png", "simple_scout.png")
    print "Perspective correlation =",  correlation("simple.png", "simple_persp.png")


if (__name__ == '__main__'):
    main()
