#pragma once

#include <usbd_cdc_if.h>

#define HIGH 0b0
#define LOW 0b1
#define bitRead(value, bit) (((value) >> (bit)) & 0x01)
#define bitSet(value, bit) ((value) |= (1UL << (bit)))
#define bitClear(value, bit) ((value) &= ~(1UL << (bit)))
#define bitWrite(value, bit, bitvalue) (bitvalue ? bitSet(value, bit) : bitClear(value, bit))

// GPIO Pins
#define PIN_CREF        9          // Sensor left
#define PIN_CSENSE      10         // Sensor right
#define PIN_NEEDLE_RTL  11         // Magnet: Pattern RTL (right to left)
#define PIN_NEEDLE_LTR  12         // Magnet: Pattern LTR (left to right)

// GPIO communication with Raspi, generates an interrupt on Raspi
#define PIN_RIGHT             2
#define PIN_LEFT              3
#define PIN_DIRECTIONCHANGE   4

void setupKnit();

class Iw {
	//char patternArray[25] = { 0 };
	int series_length{};
	char pat{};

	volatile bool interrupted = false;
	volatile bool* ptr_interrupted = &interrupted;

public:
	int serialData;
	void setPattArray(char[]);
	char setleftEnd(char leftEnd);
	char setRightEnd(char rightEnd);
	void knitLoop(const char patternArray[]);
};




