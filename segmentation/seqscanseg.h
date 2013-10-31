#ifndef __SEQSCANSEG_H
#define __SEQSCANSEG_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void segmentate(uint8_t *src, int step, uint32_t *dst, int width, int height, int delta);

#ifdef __cplusplus
}
#endif

#endif
