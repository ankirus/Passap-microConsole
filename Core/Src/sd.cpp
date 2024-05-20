

//#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include <sd.h>


int getParcel(uint8_t* Buff, uint32_t buffLen) { // (uint8_t Buff[], unsigned int buffLen)
	SerD sd;
	sd.firstBy = Buff[0];
	sd.secondBy = Buff[1];

	uint32_t buffLength = buffLen;
	if (sd.firstBy == 'b' && sd.secondBy == 39) { // Python string detected
		CDC_Transmit_FS((uint8_t*)(" Py "), 4);
		HAL_Delay(50);
		for (uint32_t i = 0; i < (buffLen - 2); ++i) {
			Buff[i] = Buff[i + 2];
		};
		buffLength = buffLen - 3; // Py example: b'03474747474747' where 03 is row identifier
	};

	sd.parseParcel(Buff, buffLength);

	return 1;
};






