
"""

                        This program is part of the Passap-MicroConsole project.
               It is intended for loading knitting patterns into PaMiCo - "Passap-MicroConsole".
               PaMiCo is a device based on a microcontroller board that is capable of performing the main
               functions of the original Passap console: storing knitting patterns in the device’s memory
               and reproducing them on knitted fabric.
               With PaMiKo you can get rid of a bulky console with a keyboard that always gets stuck,
               and by placing a tiny microcontroller board directly on the knitting lock,
               you can also get rid of the inconvenient curve cord.

                This Python program is a fork of "IrenePassap/Passap-E6000-Hacked and Rebuilt".
              (https://github.com/IrenePassap/Passap-E6000-hacked-and-rebuilt) and ported
               from Rapsberry to a regular PC.
 """

import time
import serial
import cv2
from PIL import Image
from tkinter import filedialog
import numpy as np
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,  QPushButton,
    QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
import sys
from binascii import hexlify


start = datetime.datetime.now()
print(datetime.datetime.now() - start)

ser = serial.Serial(port='com3', baudrate=115200, timeout=2)
received = []
received1 = []

ser.write(b'begin\n')
time.sleep(1)
global char1
global widthMyPatternInBytes
global widthMyPatternInPixels
file_name_pat_VNB = ""
pattern_0 = [0b0 * 23]
patternString = b'0'


def read_lines(ser):

    buffer = ser.read(300)
    time.sleep(0.05)
    print(buffer)
    buffer = ser.read(300)
    time.sleep(0.05)
    print(buffer)
    return buffer

def convertIntToStrSize2(numRow):
    # j = numRow  # pattern row for download
    if numRow <= 9:
        strNumRow = "0" + str(numRow)
    else:
        strNumRow = str(numRow)
    return strNumRow


def receiving():
    received1 = read_lines(ser)
    time.sleep(0.1)

    strReceived = str(received1)

    time.sleep(0.1)
    findErr = strReceived.find("Err")
    print()
    if findErr != -1:
        err = (strReceived[(findErr + 3):(findErr + 5)])
        print(" findErr  = ", findErr, " Err  = ", err, " ")
    else:
        err = 0

    time.sleep(0.1)


def begin2(widthMyPatternInBytes, heightMy_, widthMy_):

    numRow = 0
    strNumRow = convertIntToStrSize2(numRow)

    for j in range(heightMy_):

        ccx = ''.join('{:02X}'.format(a) for a in knitpatByte_black_VNB[j])

        jToBytesStr = (convertIntToStrSize2(j))
        # print(" jToBytesStr= ", jToBytesStr)
        newString = bytes(jToBytesStr, "ascii") + bytes(ccx, "ascii")
        # newString = bytes(ccx, "ascii")
        print(" Row ", j, ", data to load: ", newString )
        print()
        ser.write(newString)
        time.sleep(0.01)
        print(" data were loaded: ")
        receiving()

    global gray_


def opcv_(file_name_pat_VNB_):

    im = cv2.imread(file_name_pat_VNB_)
    a = np.asarray(im)
    type(a)
    sh = a.shape
    print("The shape of pattern for upload to console: ", sh)

    b_, g_, r_ = cv2.split(a)
    print("  ")
    print("--blue--")
    print(b_)
    print("--green--")
    print(g_)
    print("--red--")
    print(r_)
    print("  ")
    gray_ = (b_ + g_ + r_)/3


def get_pattern(data):

    file_name_pat_VNB_ = filedialog.askopenfilename()
    filename = Image.open(file_name_pat_VNB_)

    opcv_(file_name_pat_VNB_)

    widthMy = filename.size[0]
    global widthMyPatternInPixels
    widthMyPatternInPixels = widthMy
    heightMy = filename.size[1]
    print(widthMy, "-width of pattern, "), print(heightMy, "-height of pattern")
    listMy_black = []
    listMy_white = []


    for x in range(0, heightMy):

        row_black = []
        row_white = []

        for y in range(0, widthMy):
            pixel = (y, x)

            redMy, greenMy, blueMy = filename.getpixel(pixel)
            gray = (redMy + greenMy + blueMy)/3
            if gray < 127 :
                row_black.append(0)
                row_white.append(1)
            else:
                row_black.append(1)
                row_white.append(0)

        listMy_black.append(row_black)
        listMy_white.append(row_white)

    knitpatByte_black = []
    knitpatByte_white = []

    if (widthMy % 8) == 0:
        widthMyPatternInBytes_1 = widthMy // 8
    else:
        widthMyPatternInBytes_1 = widthMy // 8 + 1



    for i in range(0, heightMy):
        (pattern_black, widthMyPatternInBytes_1) = pattern_Array(listMy_black, i, widthMyPatternInBytes_1)
        knitpatByte_black.append(pattern_black)

    for i in range(0, widthMyPatternInBytes_1):
        (pattern_white) = pattern_Array(listMy_white, i, widthMyPatternInBytes_1)
        knitpatByte_white.append(pattern_white)

    n = 0

    return knitpatByte_black, knitpatByte_white, widthMyPatternInBytes_1, heightMy, widthMy


def pattern_Array(listMy, data, widthMyPatternInBytes_):  # data - num row

    if widthMyPatternInBytes_*8 != widthMyPatternInPixels:
        print(" Error: The width of the ornament pattern must be a multiple of 8 ")
        time.sleep(1.5)
        wait = input("Press Enter to continue.")
        time.sleep(2.5)

    n = 0

    pattern = [0b0] * widthMyPatternInBytes_  # hexadecimal string to transmit to console

    for numByteinRow in range(0, widthMyPatternInBytes_):
        for numBit in range(0, 8):
            n = (numByteinRow * 8) + numBit
            pattern[numByteinRow] = (pattern[numByteinRow] << 1) | listMy[data][n]
    return pattern, widthMyPatternInBytes_


def begin(self=None):
    global quitButton
    global filenamePattern
    global img
    global im
    global knitpatByte_black_VNB

    knitpatByte_black_VNB = []
    quitButton = 1
    np.set_printoptions(linewidth=200)
    widthMyPatternInBytes = 0
    heightMy = 0;
    widthMy = 0;

    try:
        (knitpatByte_black_VNB, knitpatByte_white_VNB, widthMyPatternInBytes, heightMy, widthMy) = get_pattern(file_name_pat_VNB)
        height_VNB = len(knitpatByte_black_VNB)
    except IOError:
        self.errorDialog("!no knitpatBytetern VNB")

    begin2(widthMyPatternInBytes, heightMy, widthMy)

class Window(QWidget):

    def __init__(self):
        super().__init__()

        v = QVBoxLayout()
        h = QHBoxLayout()
        a = 107
        button = QPushButton(str(chr(a)))
        button.pressed.connect(
            lambda val=a: self.button_pressed(val)
        )
        h.addWidget(button)

        for a in range(65, 68):
            button = QPushButton(str(chr(a)))
            button.pressed.connect(
                lambda val=a: self.button_pressed(val)
            )
            h.addWidget(button)

        for a in range(97, 100):
            button = QPushButton(str(chr(a)))
            button.pressed.connect(
                lambda val=a: self.button_pressed(val)
            )
            h.addWidget(button)

        v.addLayout(h)
        self.label = QLabel("")
        v.addWidget(self.label)
        self.setLayout(v)

        a=117  # upload pattern
        button = QPushButton(str(chr(a)))
        button.pressed.connect(
            lambda val=a: self.button_upload(val)
        )
        h.addWidget(button)

        a=110  # n, "next row" number
        button = QPushButton(str(chr(a)))
        button.pressed.connect(
            lambda val=a: self.button_pressed(val)
        )
        h.addWidget(button)

        a=116  # Test
        button = QPushButton(str(chr(a)))
        button.pressed.connect(
            lambda val=a: self.button_pressed(val)
        )
        h.addWidget(button)
        a = 120  # eXit
        button = QPushButton(str(chr(a)))
        button.pressed.connect(
            lambda val=a: self.button_exit(val)
        )
        h.addWidget(button)

    def button_upload(self, n):
        self.label.setText(str(n))
        begin()

    def button_exit(self, n):
        self.label.setText(str(n))
        sys.exit()

    def button_pressed(self, n):
        self.label.setText(str(n))
        char1 = n
        print(n)
        newString = bytes(chr(n), "ascii") + bytes(chr(n), "ascii") + bytes("+", "ascii")
        ser.write(newString)
        time.sleep(0.01)

        receiving()


app = QApplication(sys.argv)


while 1 == 1:
    w = Window()
    w.show()
    app.exec()


if __name__ == '__main__':
    begin()
    # blackANDwhite()
    # app = QApplication(sys.argv)
    # ex = App()
    # sys.exit(app.exec_())
