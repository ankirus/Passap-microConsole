#pragma once
#ifndef MP_H_
#define MP_H_

#include <string>
#include <stdint.h>
#include <usbd_cdc_if.h>
#include "cf.h"
#include "Iw.h"

extern char currernPattern;
extern int currernParameter;
//extern int currRow;
class Mp  //multiply pattern
{

	void fill_knitBitArr(uint8_t currRow) {

		if (currernParameter < 0 || currernParameter > 180) { // here currernParameter is pattern width
			CDC_Transmit_FS((uint8_t*)(" err: wrong patt width "), 24);
			HAL_Delay(50);
		};

		if (currernPattern == 'A') {
			for (int i = 0; sizeof(str_180) <= 23; ++i) str_180 += g_vec::vA.at(currRow);
		}
		else 	if (currernPattern == 'B') {
			for (int i = 0; sizeof(str_180) <= 23; ++i) str_180 += g_vec::vB.at(currRow);
		}
		else 	if (currernPattern == 'C') {
			for (int i = 0; sizeof(str_180) <= 23; ++i) str_180 += g_vec::vC.at(currRow);
		}
		else {
			CDC_Transmit_FS((uint8_t*)(" err: fill_knitBitArr() "), 25);
			HAL_Delay(50);
			return;
		};
		CDC_Transmit_FS((uint8_t*)(" knit row: "), 23);
		HAL_Delay(50);
		CDC_Transmit_FS((uint8_t*)&str_180, 23);
		HAL_Delay(50);
		return;
	};

public:
	std::string str_180;
	Mp(uint8_t knitRow) {
		fill_knitBitArr(knitRow);
		Iw iw;
		char* c = &str_180[0];
		iw.knitLoop(c);
	};
	~Mp();

};

#endif
