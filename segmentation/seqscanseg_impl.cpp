#include "seqscanseg.h"
#include <stdint.h>
#include <vector>

using std::vector;

inline int abs(int x) {
	return (x > 0) ? x : -x;
}

class Segment {
	uint32_t id;
	uint32_t sumI;
	uint32_t pxls;
	Segment *parent;
	double avg;
public:
	Segment(uint8_t pxlI, uint32_t id, Segment *parent = NULL) {
		this->id = id;
		this->pxls = 1;
		this->sumI = pxlI;
		this->avg = pxlI;

		if (parent != NULL) {
			parent->addPixel(pxlI);
		}
		this->parent = parent;
	}

	double getAverangeI() {
		Segment *root = getRoot();
		return root->avg;
	}

	void addPixel(int pxlI) {
		Segment *root = getRoot();
		root->sumI += pxlI;
		root->pxls += 1;
		root->avg = root->sumI / ((double)root->pxls);
	}

	void addPixels(Segment *b) {
		sumI += b->sumI;
		pxls += b->pxls;
		avg = sumI / ((double)pxls);
	}

	Segment *mergeComponents(Segment *b) {
		if (id == b->id)
			return this;
		if (id > b->id) {
			parent = b;
			getRoot()->addPixels(this);
			return b;
		} else {
			b->parent = this;
			getRoot()->addPixels(b);
			return this;
		}
	}

	int distToPixel(int pxlI) {
		return abs(pxlI - getAverangeI());
	}

	int distToSegment(Segment *b) {
		return abs(b->getAverangeI() - getAverangeI());
	}	

	uint32_t getId() {
		return id;
	}

	Segment *getRoot() {
		return (parent == NULL) ? this : parent->getRoot();
	}
};

bool isLessDistance(Segment *a, Segment *b, int delta) {
	if ((a == NULL) || (b == NULL)) {
		return false;
	} else {
		return a->distToSegment(b) < delta;
	}
}

bool isLessDistance(Segment *a, uint8_t pxlI, int delta) {
	return (a == NULL) ? false : (a->distToPixel(pxlI) < delta);
}

Segment *closerToPixel(Segment *a, Segment *b, uint8_t pxlI) {
	if (a == NULL)
		return b;
	if (b == NULL)
		return a;

	return (a->distToPixel(pxlI) < b->distToPixel(pxlI)) ? a : b;
}

uint32_t getComponentId(vector<Segment *> &segments, uint8_t srcI, uint32_t upLbl, uint32_t leftLbl, int delta) {
	if (srcI == 0) {
		return 0;
	}

	Segment *upSeg = (upLbl == 0) ? NULL : segments[upLbl - 1];
	Segment *leftSeg = (leftLbl == 0) ? NULL : segments[leftLbl - 1];
	bool isUpLessDelta = isLessDistance(upSeg, srcI, delta);
	bool isLeftLessDelta = isLessDistance(leftSeg, srcI, delta);

	if ((!isUpLessDelta) && (!isLeftLessDelta)) {
		uint32_t id = segments.size() + 1;
		segments.push_back(new Segment(srcI, id));
		return id;
	}

	if (isUpLessDelta != isLeftLessDelta) {
		if (isUpLessDelta) {
			segments[upLbl - 1]->addPixel(srcI);
			return upLbl;
		} else {
			segments[leftLbl - 1]->addPixel(srcI);
			return leftLbl;
		}
	}

	if (isLessDistance(upSeg, leftSeg, delta)) {
		return upSeg->mergeComponents(leftSeg)->getId();
	} else {
		Segment *seg = closerToPixel(upSeg, leftSeg, srcI);
		seg->addPixel(srcI);
		return seg->getId();
	}
}

void releaseSegments(const vector<Segment *> &v) {
	for(vector<Segment *>::const_iterator it = v.begin(); it != v.end(); ++it) {
		Segment *s = *it;
		delete s;
	}
}

void segmentate(uint8_t *src, int step, uint32_t *dst, int width, int height, int delta) {
	vector<Segment *> segments;
	uint32_t *curRow = dst;
	uint32_t *prevRow = dst;

	*curRow = getComponentId(segments, *src, 0, 0, delta);
	src += step;
	curRow += 1;	

	for(int j = 1; j < width; ++j) {
		*curRow = getComponentId(segments, *src, 0, *(curRow - 1), delta);
		curRow += 1;
		src += step;
	}

	for(int i = 1; i < height; ++i) {
		*curRow = getComponentId(segments, *src, *prevRow, 0, delta);
		++prevRow;
		++curRow;
		src += step;
		for (int j = 1; j < width; ++j) {
			*curRow = getComponentId(segments, *src, *prevRow, *(curRow -1), delta);
			++prevRow;
			++curRow;
			src += step;
		}
	}

	for (int i = 0; i < width; ++i) {
    	for (int j = 0; j < height; ++j) {
      		if (*dst != 0) {
          		*dst = segments[(*dst) - 1]->getRoot()->getId();
          	}
      		dst += 1;
    	}
    }

	releaseSegments(segments);	
}
