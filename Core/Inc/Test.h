
#pragma once
#include "stm32f1xx_hal.h"
#include <usbd_cdc_if.h>
#include <vector>
#include <string>
#include <cstdint>


int testProg(std::vector<std::string>  vect);
extern int currentParameter;
extern uint8_t buffer[];
extern uint16_t bufferLen;





