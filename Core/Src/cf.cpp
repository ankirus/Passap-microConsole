
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <cstring>
#include <string.h>
//#include <string>
#include <../Inc/cf.h>

extern int currentParameter;


char sz = '`';
char fB = '`';
int (*pattptr[3])() = { A, B, C };
int (*functptr[27])() = { _, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z };


int A() {
	uint8_t TxBuffer[] = " A() ";
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);
	g_vec::vA.clear();
	return 1;
};

int B() {
	uint8_t TxBuffer[] = " B() ";
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);
	g_vec::vB.clear();
	return 1;
};

int C() {
	uint8_t TxBuffer[] = " C() ";
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);
	g_vec::vC.clear();
	return 1;
};

void call_functptr(char func, int par, char secondBy) {

	uint8_t fun = (func & 0x1F);

	(*functptr[fun])();
};

void call_pattptr(char pattern) {  

	char tmp = (pattern & 0x0F);

	(*pattptr[tmp - 1])();

};

void toArrStor(char currPatt, const  std::string& astral, size_t sz, char fB)  //for future releases
{

	switch (currPatt) {
	case 'A':
		A();
		break;
	case 'B':
		B();
		break;
	case 'C':
		C();
		break;
	};
}


inline static char chr(char h) {
	if (isdigit(h)) h -= 0x30;
	else h -= 0x37; // AtoF
	return h;
};

inline static char chr2(char h, char l) {
	return (chr(h) << 4 | chr(l));
};

void   convBufToASCIIstr(uint8_t* h, uint32_t buffLen, char currPatt) {

	uint32_t astriLen = buffLen / 2;

	std::string astri{ "" };
	for (uint32_t n1 = 0; n1 <= (buffLen - 1); n1 += 2) {
		char ab = (chr2(h[n1], h[n1 + 1]));
		astri += ' ';
		astri[n1 / 2] = ab;
	};

	uint8_t TxBuffer[] = " row( ) = ";
	TxBuffer[6] = (astriLen | 0x30);

	CDC_Transmit_FS(TxBuffer, (sizeof(TxBuffer) - 1));
	HAL_Delay(30);

	const char* c = astri.c_str();
	CDC_Transmit_FS((uint8_t*)c, astriLen);
	HAL_Delay(30);

	std::string subastri = astri.substr(1, astri.length()); //first char is row id

	if (currPatt == 'A') { g_vec::vA.push_back(subastri); return; };
	if (currPatt == 'B') { g_vec::vB.push_back(subastri); return; };
	if (currPatt == 'C') {
		g_vec::vC.push_back(subastri);
	}
	else {
		uint8_t TxBuffer3[] = " err: pattern must be specified! \r\n";
		uint8_t TxBufferLen3 = sizeof(TxBuffer3);
		HAL_Delay(30);
		CDC_Transmit_FS(TxBuffer3, TxBufferLen3);
		HAL_Delay(30);
	};
	return;
}


void peVecTr(const std::string stri) {
	uint8_t le = stri.length();
	uint8_t* c = (uint8_t*)strcpy(new char[le], stri.c_str());
	CDC_Transmit_FS(c, le);
	delete[] c;
	HAL_Delay(60);
	CDC_Transmit_FS((uint8_t*)("-"), 1);
	HAL_Delay(60);
};


int t() { 

	if (isupper(buffer[1])) {
		currentPattern = buffer[1];
		CDC_Transmit_FS((uint8_t*)(" \r\n Pattern:  \r\n  "), 16);
		HAL_Delay(60);
		CDC_Transmit_FS(&buffer[1], 1);
		HAL_Delay(60);
	};

	std::string s2{};

	switch (currentPattern) {
	case 'A': {
		s2 = (g_vec::vA[0]);
		testProg(s2);
		return 1;
	}
	case 'B': {
		s2 = (g_vec::vB[0]);
		testProg(s2);
		return 1;
	}
	case 'C': {
		s2 = (g_vec::vC[0]);
		testProg(s2);
		return 1;
	}
	default:
		CDC_Transmit_FS((uint8_t*)(" wrong pattern ID \r\n"), 20);
		HAL_Delay(50);
	};

	return 0;
};
