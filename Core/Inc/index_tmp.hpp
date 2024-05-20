
#ifndef INDEX_TMP_H
#define INDEX_TMP_H

#include <stdio.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

	extern uint8_t buffer[64];
	extern uint16_t bufferLen;
	extern uint16_t* pBufferLen;
	extern int bufferFlag;

	int fillBuffer(uint8_t* buf, uint16_t bufLen);

#ifdef __cplusplus
}
#endif

#endif //INDEX_TMP_H

