

#ifndef CF_H
#define CF_H

#include <vector>
#include <string>

#include <stdint.h>

#include <usbd_cdc_if.h>
#include <Test.h>

extern class Test theTest;;
void testProg(std::string);
extern uint8_t buffer[];
extern uint16_t bufferLen;
extern char currentPattern;
extern int currentParameter;
namespace g_vec {
	static std::vector<std::string> vA;
	static std::vector<std::string> vB;
	static std::vector<std::string> vC;
};

void peVecTr(std::string stri); //print  row

static int peVec(std::vector<std::string> dq) { //print rows of current pattern
	uint8_t sz = (dq.size());

	if (sz > 0) {
		uint8_t TxBuffer[] = " total rows:  ";
		TxBuffer[11] = sz | 0X30;
		uint8_t TxBufferLen = sizeof(TxBuffer);
		CDC_Transmit_FS(TxBuffer, TxBufferLen);
		HAL_Delay(50);
	}
	else {
		CDC_Transmit_FS((uint8_t*)(" no one rows of current pattern was inserted "), 46);
		HAL_Delay(60);
		return 0;
	};

	uint8_t le = dq[0].length();
	uint8_t* c = (uint8_t*)strcpy(new char[le + 1], dq[0].c_str());
	CDC_Transmit_FS(c, le);
	delete[] c;
	HAL_Delay(60);
	CDC_Transmit_FS((uint8_t*)("|"), 1);
	HAL_Delay(60);

	for (size_t i1 = 0; i1 < sz; ++i1) {
		std::string stri = dq[i1];
		peVecTr(stri);
		/*
		   uint8_t le = dq[i1].length();
		   uint8_t* c = (uint8_t*)strcpy(new char[le], dq[i1].c_str());
		  CDC_Transmit_FS(c, le);
		  delete[] c;
		   HAL_Delay(50);
		   CDC_Transmit_FS((uint8_t*)("%"), 1);
		   HAL_Delay(50);
		   */
	}

	HAL_Delay(40);
	CDC_Transmit_FS((uint8_t*)"~", 1);
	HAL_Delay(40);
	return 1;
};


int A(void);
int B(void);
int C(void);


static int _() {
	return 1;
};

static int a() {
	currentPattern = 'A';
	uint8_t vAsize = g_vec::vA.size();
	uint8_t TxBuffer[] = " total   rows in 'A' pattern ";
	TxBuffer[7] = (vAsize | 0x30);
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);
	if (vAsize > 0) {
		peVec(g_vec::vA);
	}
	else {
		CDC_Transmit_FS((uint8_t*)(" no images were loaded in A "), 28);
		HAL_Delay(50);
	};
	return 1;
};

static int b() {
	currentPattern = 'B';
	uint8_t vBsize = g_vec::vB.size();
	uint8_t TxBuffer[] = " total   rows in 'B' pattern ";
	TxBuffer[7] = (vBsize | 0x30);
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);
	if (vBsize > 0) {
		peVec(g_vec::vB);
	}
	else {
		CDC_Transmit_FS((uint8_t*)(" no images were loaded in B "), 28);
		HAL_Delay(50);
	};
	return 1;
};

static int c() {
	currentPattern = 'C';
	uint8_t vCsize = g_vec::vC.size();
	uint8_t TxBuffer[] = " total   rows in 'C' pattern ";
	TxBuffer[7] = (vCsize | 0x30);
	uint8_t TxBufferLen = sizeof(TxBuffer);
	CDC_Transmit_FS(TxBuffer, TxBufferLen);
	HAL_Delay(50);
	if (vCsize > 0) {
		peVec(g_vec::vC);
	}
	else {
		CDC_Transmit_FS((uint8_t*)(" no images were loaded in C "), 28);
		HAL_Delay(50);
	};
	return 1;
};


static int d() {
	return 1;
};
static int e() {
	return 1;
};
static int f() {
	return 1;
};
static int g() {
	return 1;
};
static int h() {
	return 1;
};
static int i() {
	return 1;
};
static int j() {
	return 1;
};
static int k() { // command: 'kA.' set currentPattern to 'A'
	/*
	currentRow = 0;
	SerD sd;
	char c = sd.secondBy;
	switch ( c )
	{
	   case 'A':
		  currentPattern = 'A';
		  break;
	   case 'B':
		   currentPattern = 'B';
		  break;
	   case 'C':
		   currentPattern = 'C';
		  break;
	   default:
		   currentPattern = 'A';
	};

	currentRow = currentParameter;
*/

	return 1;
};

static int l() {
	return 1;
};
static int m() {
	return 1;
};
static int n() {
	return 1;
};
static int o() {  //

	return 1;
};
static int p() {

	return 1;
};
static int q() {
	return 1;
};
static int r() {
	//rr.loopR();
	return 1;
};
static int s() {
	return 1;
};

int t();

static int u() {
	return 1;
};
static int v() {

	return 1;
};
static int w() {

	return 1;
};
static int x() {
	return 1;
};
static int y() {
	return 1;
};
static int z() {
	return 1;
};

inline   char numbOfLetters(char d = {}) {  //return number of letter
	//Serial << " numbOfLetters d = " << d;
	char i2 = (d & 0x0F);
	//Serial << " (d & 0x0F)= " << i << " ";
	return i2;
}

void call_functptr(char func, int par, char secondBy); // command function

void call_pattptr(char pattern); // pattern

void toArrStor(char currPatt, const  std::string& astral, size_t sz, char fB);


// convert hex char string to ASCII char string for storage (reduce memory usage)
// void convHexStrToASCIIone(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, unsigned int, char, char);

#endif  //CF_H
