
#include "usbd_cdc_if.h"
#include <stdint.h>
#include "../Inc/index_tmp.hpp"

#ifdef __cplusplus
extern "C" {
#endif

	int fillBuffer(uint8_t* buf, uint16_t Len) {
		bufferFlag = 1;
		bufferLen = Len;
		for (uint16_t n = 0; n <= 63; ++n) {
			buffer[n] = '\0';
		};
		for (uint16_t n = 0; n <= Len; ++n) {
			buffer[n] = buf[n];
		};

		CDC_Transmit_FS(buffer, bufferLen);

		return 1;

	};

#ifdef __cplusplus
}
#endif




