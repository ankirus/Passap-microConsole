#ifndef INDEX_H
#define INDEX_H

/*
 *
 *
 * This version of the program is not intended for connection to a knitting machine,
 * it illustrates the device control algorithm
 *
 *
*/

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <usbd_cdc_if.h>

#include "sd.h" //**************

extern int  getParcel(uint8_t* Buff, uint32_t buffLen);

bool parameterExist{ false };
uint8_t buffer[64];
uint16_t bufferLen = 0;
uint16_t* pBufferLen = &bufferLen;
int bufferFlag = 0;
int currentParameter{}; //left and right knitting ends; pattern width; set knit row; etc.
int currentRow{}; //knot row = vector[element]
char currentPattern = { 'A' }; // currentPattern = vector

int main_index(void);

#ifdef __cplusplus
extern "C" {
#endif

	int receivedMessageFS(uint8_t* buf, uint16_t Len);

#ifdef __cplusplus
}
#endif


int main_index() {
	for (;;) {
		if (bufferFlag) {
			bufferFlag = 0;
			CDC_Transmit_FS(buffer, bufferLen);
			HAL_Delay(50);
			getParcel(buffer, bufferLen);
		};
	};
	return 1;
}


int receivedMessageFS(uint8_t* buf, uint16_t Len) {
	uint8_t TxBuffer[] = " receive: ";
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);

	CDC_Transmit_FS(buf, Len);
	HAL_Delay(50);
	uint8_t TxBuffer2[] = " ";
	CDC_Transmit_FS(TxBuffer2, 1);

	return 1;
};


#endif
