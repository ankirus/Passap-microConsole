#pragma once

#ifndef SD_H
#define SD_H

#include <stdlib.h> 
#include <cstdio>
#include <cctype>
#include <string.h>
#include <vector>
#include <string>

#include "usbd_cdc_if.h"

extern int A();
extern int B();
extern int C();
extern void call_functptr(char, int, char);
extern void convBufToASCIIstr(uint8_t* Buff, uint32_t buffLen, char currentPattern);

extern char currentPattern;
extern int currentParameter;

int getParcel(uint8_t* Buff, uint32_t buffLen);

class SerD {

	size_t currentLen = 0;

public:
	char firstBy = 0b0;
	char secondBy = 0b0;
	SerD() {

	};
	~SerD() {};


	uint8_t numRowInData{ 0 }; //for future release to make possible to change separate pattern rows and for test purpose


	char isNumRow(char c1, char c2) {

		return c1 * 10 + c2;
	};

	int extractCommandParameter(uint8_t* Buf, uint32_t sdLen) {

		CDC_Transmit_FS((uint8_t*)(" command parameter: "), 21);
		HAL_Delay(50);
		if (sdLen > 6) {
			CDC_Transmit_FS((uint8_t*)(" length err: "), 14);
			HAL_Delay(50);
			isErr('l');
			return 0;
		};

		if ((Buf[2] != '-') && (isdigit(Buf[2]) == 0)) {
			CDC_Transmit_FS((uint8_t*)(" err: only numbers and the sign '-' ! "), 38);
			HAL_Delay(50);
			isErr('n');
		};

		for (uint32_t i = 3; i < sdLen; ++i) {
			if (isdigit(Buf[2]) == 0) {
				CDC_Transmit_FS((uint8_t*)(" err: only numbers and the sign '-' . "), 38);
				HAL_Delay(50);
				isErr('n');
				return 0;
			};
		};

		char bufCmdPar[sdLen - 2]{}; // bufCmdPar - buffer for command parameter: (first two chars is for commands; third etc. - is parameter)

		for (long unsigned int i = 0; i < (sdLen - 2); ++i) {
			bufCmdPar[i] = Buf[i + 2];
		};

		int   intCmdPar{}; // same in integer
		sscanf((char*)bufCmdPar, "%d", &intCmdPar);

		char bufTmp[5];
		int charNumber = sprintf(bufTmp, " %d\n ", intCmdPar);

		CDC_Transmit_FS((uint8_t*)&bufTmp, 5);

		return intCmdPar;

	};

	int parseParcel(uint8_t* Buf, uint32_t sdLen) {


		if (isdigit(firstBy) && isdigit(secondBy)) {  //is pattern data if first and second chars is digits in decimal = pattern row (max 99 rows in this release)
			//CDC_Transmit_FS((uint8_t*)(" is_pattern "), 11);
			 //HAL_Delay(50);
			numRowInData = (firstBy & 0x0F) * 10 + (secondBy & 0x0F);
			convBufToASCIIstr(Buf, sdLen, currentPattern); // ...at this time currentPattern is global

		}
		else if (islower(firstBy) || isupper(firstBy)) {  //is command
			//CDC_Transmit_FS((uint8_t*)(" is_command "), 11);
			// HAL_Delay(50);
			int commandParam = -999;
			if (isdigit(Buf[2]) || ('-' == Buf[2])) {
				commandParam = extractCommandParameter(Buf, sdLen);
				currentParameter = commandParam;
			};

			if (islower(firstBy)) {
				// CDC_Transmit_FS((uint8_t*)(" is_lower "), 9);
				// HAL_Delay(50);
				call_functptr(firstBy, commandParam, secondBy); //call console commands
			};

			if (isupper(firstBy)) {  //set pattern ID A, B or C


				if (firstBy == 'A') {
					CDC_Transmit_FS((uint8_t*)(" _A_ "), 5);
					A();
				}
				else
					if (firstBy == 'B') {
						CDC_Transmit_FS((uint8_t*)(" _B_ "), 5);
						B();
					}
					else
						if (firstBy == 'C') {
							CDC_Transmit_FS((uint8_t*)(" _C_  "), 5);
							C();
						}
						else { isErr('P'); return 0; };

				currentPattern = firstBy;
			}

		}
		else {
			CDC_Transmit_FS((uint8_t*)(" wrong message, err: "), 22);
			isErr('f'); // wrong First symbol of message
		};
		HAL_Delay(50);
		return 1;
	} // end of deqToStr()

	char isErr(char u) {
		CDC_Transmit_FS((uint8_t*)(" err: "), 6);
		HAL_Delay(40);
		CDC_Transmit_FS((uint8_t*)&u, 1);
		HAL_Delay(40);
		return u;
	}


}; // class SerD {



#endif //  SD_H
