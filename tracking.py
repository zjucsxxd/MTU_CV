#!/usr/bin/python

import cv2
import cv
import segmentation.seqscanseg as segalg
import segprops.segprops as segprops

BACKGROUND_THRESHOLD = 150
SEGMENT_THRESHOLD = 50
SEGMENT_MINS = 100
SEGMENT_MAXI = 200

class TrackSegment:
#    histo
#    motion
#    timeOfLife
#    timeOfEps
    def __init__(self, histo, cX, cY, S):
        self.histo = histo
        self.motion = [(cX / S, cY / S)]
        self.timeOfLife = 1
        self.timeOfEps = -1
        self.isShown = True
    def checkDist(self, hist):
        return cv2.compareHist(self.histo, hist, cv.CV_COMP_CORREL)
    def add(self, histo, cX, cY, S):
        self.timeOfEps = -1
        self.histo = histo
        self.motion.append((cX / S, cY / S))
        self.isShown = True

def filterSegment(segment):
    return (segment.S > SEGMENT_MINS and 
            segment.maxI > SEGMENT_MAXI)

def extractSegments(src):
    segmap = segalg.seqScanSeg(src, SEGMENT_THRESHOLD)
    segsProps = segprops.extractSegProps(segmap, src)
    return dict((k, v) for k, v in segsProps.iteritems() if filterSegment(v))

def showSegments(segsProps, dst):
    for key in segsProps:
        segProps = segsProps[key]
        cv2.rectangle(dst, (segProps.x0, segProps.y0),
                            (segProps.x1, segProps.y1), (0, 155, 0))

def findMaxPSegment(motionTable, seg):
    maxP = 0.0
    maxPSeg = None
    for trkSeg in motionTable:
        P = trkSeg.checkDist(seg.getHist())
        if (maxP < P):
            maxP = P
            maxPSeg = trkSeg
    return (maxP, maxPSeg)


def fillMotionTable(motionTable, segsProps):
    for trkSeg in motionTable:
        trkSeg.isShown = False

    for k, v in segsProps.iteritems():
        (maxP, segment) = findMaxPSegment(motionTable, v)
        if (maxP < 0.85):
            motionTable.append(TrackSegment(v.getHist(), v.xS, v.yS, v.S))
        else:
            segment.add(v.getHist(), v.xS, v.yS, v.S)

    for trkSeg in list(motionTable):
        if (trkSeg.isShown == False):
            trkSeg.timeOfEps += 1
            if (trkSeg.timeOfEps > 100):
                motionTable.remove(trkSeg)
        else:
            trkSeg.timeOfEps = 0

def showMotion(motionTable, dst):
    for trkSeg in motionTable:
        if (len(trkSeg.motion) > 1):
            for i in xrange(1, len(trkSeg.motion)):
                    cv2.line(dst, trkSeg.motion[i-1], trkSeg.motion[i],
                                    (155, 0, 0))



def main():
    cap = cv2.VideoCapture("../Astrohn_auto.mp4")
    cv2.namedWindow("Window")
    motionTable = []

    while (cv2.waitKey(30) == -1):
        (ret, img) = cap.read()
        img_proc = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, dstCn = 1)
        (ret, img_proc) = cv2.threshold(img_proc, BACKGROUND_THRESHOLD, 
                                        255, cv2.THRESH_TOZERO)
        segsProps = extractSegments(img_proc)
        fillMotionTable(motionTable, segsProps)
        showSegments(segsProps, img)
        showMotion(motionTable, img)
        cv2.imshow("Window", img)



    return


if (__name__ == '__main__'):
    main()
