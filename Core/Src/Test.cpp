
#include "Test.h"
#include <cstring>


int test1(std::string s1) {
	CDC_Transmit_FS((uint8_t*)" \r\n Test(): ", 13);
	HAL_Delay(40);
	std::string t{ "" };
	uint8_t onechar[1];

	do { t += s1; } while (t.size() < 23);

	for (uint8_t patternPos = 0; patternPos <= 179; patternPos = patternPos + 1) {
		onechar[0] = ((t[patternPos / 8]) >> (patternPos % 8)) & 0b1 ? '1' : '0';
		CDC_Transmit_FS(onechar, 1);
		HAL_Delay(60);
		if (onechar[0] == '1')
		{
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
		}
		else
		{
			HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
		};
		/*
		if(patternPos >= 180){
		  CDC_Transmit_FS((uint8_t *)" /r/n ", 6);
		  HAL_Delay(40);
		  return 0
		};
		*/
	};
	return 1;
};


void testProg(std::string stri) {
	test1(stri);
	return;
};
