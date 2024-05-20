
"""

            This program is part of the Passap-MicroConsole project.
           (Passap is a brand of knitting machines.)
           This is a Python program for loading knitting patterns into PaMiCo - "Passap-MicroConsole".
           PaMiCo is a microcontroller board based device programmed using
           CUBE IDE and can perform some of the functions of the original Passap console.

            Forked from IrenePassap/Passap-E6000-hacked-and-rebuilt
            (https://github.com/IrenePassap/Passap-E6000-hacked-and-rebuilt)
 """

import time
import serial
import cv2
# import bitarray
# from bitstring import BitArray
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


# -------------------------------
def read_lines(ser):

    buffer = ser.read(300)
    time.sleep(0.05)
    print(buffer)
    buffer = ser.read(300)
    time.sleep(0.05)
    print(buffer)
    # buffer = readline(ser)
    # print(buffer)
    return buffer




def convertIntToStrSize2(numRow):
    # j = numRow  # pattern row for download
    if numRow <= 9:
        strNumRow = "0" + str(numRow)
    else:
        strNumRow = str(numRow)
    return strNumRow


def receiving():
    received = read_lines(ser)
    time.sleep(0.1)
    # print("dataFromConsole=", received, )
    print("dataFromConsole=", received.decode("utf-8"), " ! ")
    strReceived = str(received)

    time.sleep(0.1)
    findErr = strReceived.find("Err")
    print()
    if findErr != -1:
        err = (strReceived[(findErr + 3):(findErr + 5)])
    else:
        err = 0
    print(" findErr  = ", findErr, " Err  = ", err, " ")
    time.sleep(0.1)


def begin2(widthMyPatternInBytes, heightMy_, widthMy_):
    print(" l113_def_begin2(widthMyPatternInBytes)=", widthMyPatternInBytes, " ")
    numRow = 0
    # print(" NumRow  = ", numRow, ' ', " strNumRow  = ", strNumRow, ' ')
    strNumRow = convertIntToStrSize2(numRow)
    print(" NumRow  = ", numRow, ' ', " strNumRow  = ", strNumRow, ' ')
    print(" knitpatByte_black_VNB=", knitpatByte_black_VNB)
    print(" heightMy_=", heightMy_)

    for j in range(heightMy_):

        #  print(" knitpatByte_black_VNB[j]=", knitpatByte_black_VNB[j])
        ccx = ''.join('{:02X}'.format(a) for a in knitpatByte_black_VNB[j])

        jToBytesStr = (convertIntToStrSize2(j))
        # print(" jToBytesStr= ", jToBytesStr)
        newString = bytes(jToBytesStr, "ascii") + bytes(ccx, "ascii")
        # newString = bytes(ccx, "ascii")
        print(" Row ", j, ", is loading:  ")
        print("newString=", newString)
        ser.write(newString)
        time.sleep(0.01)
        print(" data were loaded: ")
        receiving()


# ------------------------------------

# Array for knit pattern

def opcv_(file_name_pat_VNB_):
    print("  ")
    print(' im = cv2.imread(file_name_pat_VNB_)')
    im = cv2.imread(file_name_pat_VNB_)
    a = np.asarray(im)
    type(a)
    sh = a.shape
    print("The shape of pattern for upload to console: ", sh)
    b, g, r = cv2.split(a)
    print("  ")
    print("--blue--")
    print(b)
    print("--green--")
    print(g)
    print("--red--")
    print(r)
    print("  ")


def get_pattern(data):
    #  print(" def get_pattern(data): ")
    file_name_pat_VNB_ = filedialog.askopenfilename()
    #  print(" - file_name_pat_VNB= ", file_name_pat_VNB_)
    filename = Image.open(file_name_pat_VNB_)
    # filename = Image.open(data)

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

        #  print(" 204 row_black = ", row_black)
        listMy_black.append(row_black)
        listMy_white.append(row_white)

    #  print(" listMy_black = ", listMy_black)
    #  print(" listMy_white = ", listMy_white)

    knitpatByte_black = []
    knitpatByte_white = []

    if (widthMy % 8) == 0:
        widthMyPatternInBytes_1 = widthMy // 8
    else:
        widthMyPatternInBytes_1 = widthMy // 8 + 1

    print(" l215_widthMyPatternInBytes_1 = ", widthMyPatternInBytes_1)
    print(" heightMy = ", heightMy)
    for i in range(0, heightMy):
        (pattern_black, widthMyPatternInBytes_1) = pattern_Array(listMy_black, i, widthMyPatternInBytes_1)
        print(" 204 (row) pattern_black = ", pattern_black)
        knitpatByte_black.append(pattern_black)
        print(" 206 knitpatByte_black = ", knitpatByte_black)

    for i in range(0, widthMyPatternInBytes_1):
        (pattern_white) = pattern_Array(listMy_white, i, widthMyPatternInBytes_1)
        knitpatByte_white.append(pattern_white)

    print(" 212 knitpatByte_black", knitpatByte_black)
    n = 0

    return knitpatByte_black, knitpatByte_white, widthMyPatternInBytes_1, heightMy, widthMy

def pattern_Array(listMy, data, widthMyPatternInBytes):  #data - num row
    #  print(' def pattern_Array(listMy, data) ')
    print(" width My Pattern In Pixels=  ", widthMyPatternInPixels)
    print(" width My Pattern In Bytes=  ", widthMyPatternInBytes)

    if ((widthMyPatternInBytes*8) != widthMyPatternInPixels):
        print(" Error: The width of the ornament pattern must be a multiple of 8 ")
        time.sleep(1.5)
        wait = input("Press Enter to continue.")
        time.sleep(2.5)
        # exit()

    #  print("listMy= ",listMy)
    #  print(' - data= ', data, )
    pattern_data = listMy[data]
    #  print(" l244_pattern_data = ", pattern_data)

    n = 0
    m = 0

    pattern = [0b0] * widthMyPatternInBytes
    print(" pattern =  ", pattern)
    print(' data= ', data, " ")


    '''
    while m < widthMyPatternInBytes:
        while m < widthMyPatternInBytes:

            for y in range(0, 8):
                # val = pattern_data[n]  # = listMy[data]
                val = pattern_data[y]  # = listMy[data]

                n += 1
                if val == 0:
                    pattern[m] = pattern[m].__lshift__(1)
                else:
                    pattern[m] = pattern[m].__lshift__(1)
                    pattern[m] |= 1
                print( "n =  ", n, " y = ", y, "val = ", val,"m=", m, ", pattern[m] = ", pattern[m])

            print(" _m=", m, ", pattern[m] = ", pattern[m])
            m += 1
    '''

    for w in range(0, widthMyPatternInBytes):  # convert to bytes
        print("  w1=", w)
        for y in range(0, 8):
            n = (w*8) + y
            val = pattern_data[n]
            print("  w1=", w, " y1=", y, " n=", n," val=", val, " pattern[w] = ", pattern[w])
            pattern[w] = pattern[w] | val
            print(" pattern[w] = ", pattern[w])
            if y < 7 :
                pattern[w] = pattern[w] << 1
        print("  w=", w, ", pattern[w] = ", pattern[w])

    print(" 251_pattern_data = ", pattern_data)
    print(" 252_pattern = ", pattern)
    return pattern, widthMyPatternInBytes


def begin1():
    file_name_pat_VNB = filedialog.askopenfilename()

    print(file_name_pat_VNB, ' - file_name_pat_VNB')
    img = Image.open(file_name_pat_VNB)
    # pixel_ = img.getpixel((2, 3))
    # print(pixel_, ' - pixel')
    widthMy = img.size[0]
    widthMyPatternInPixels = widthMy
    heightMy = img.size[1]
    print(widthMy, " widthMy"), print(heightMy, " heightMy")

    # print('len.ba1', ba1.__len__())
    # print("array_new23 ", array_new23)
    im = cv2.imread(file_name_pat_VNB)
    aaa = np.asarray(im)
    # type(aaa)
    # print("aaa = ", aaa , ' -> aaa')
    sh = aaa.shape
    print("The shape of aaa numpy array is: ", sh)
    # for i in range(len(a)):
    #     print(a)
    List_a = np.ndarray.tolist(aaa)
    # print(" List_a = np.ndarray.tolist(aaa) ")
    # print(" List_a = " , List_a, " -  List_a")

    b, g, r = cv2.split(aaa)
    # print("b, g, r = cv2.split(aaa)")
    # print( "b = " , b)

    w, h = widthMy, heightMy
    bb_arr = [[0 for x in range(w)] for y in range(h)]
    print(bb_arr, "*----bb_arr---только создан ")
    # print("*'''''''''''''''''''''''''''''''''''''''----bb_arr---''''''''''''''''''''''''''''''''''''''' ")
    bb_arr_bool = bb_arr
    print( bb_arr_bool ,' - bb_arr_bool ')
    for i in range(h):
        for j in range(w):
            tmp = (b[i][j])
            if tmp <= 100:
                (bb_arr_bool[i][j]) = 0
            else:
                (bb_arr_bool[i][j]) = 1
    # print( bb_arr_bool, "----bb_arr---:")
    global bb_string
    global bb_list_bool
    bb_string = np.array2string(b, separator=" ")
    print(bb_string, '  -bb_string = np.array2string(b, separator=" ")- ')
    print("----bb_string----")
    print("***********************************************************************")
    bb_list = b.tolist()
    print("--bb_list-- = b.tolist() ")
    print(" bb_list = ", bb_list, " bb_list = b.tolist() ")

    bb_list_bool = bb_list
    for i in range(len(bb_list)):
        for j in range(len(bb_list[i])):
            tmp = (bb_list[i][j])
            if tmp <= 100:
                (bb_list_bool[i][j]) = 0
            else:
                (bb_list_bool[i][j]) = 1

    print(bb_list_bool, ' --(bb_list_bool)-- '), print("*----bb_list---bool -end")

    my_array = np.array(bb_list)
    print(" my_array = np.array(bb_list) ")
    print("my_array = " , my_array)
    value = tuple(b)
    print(' - value = tuple(b)')
    print(value, ' - value = tuple(List_a)')
    list_my_arr = my_array.tolist()
    print("list_my_arr = my_array.tolist()")
    print("list my arr = " , list_my_arr , " -> list my arr")
    print(type(list_my_arr)) # <class 'list'>
    # converting list to string using list comprehension


def begin():
    print(" begin() ")
    global quitButton
    global filenamePattern
    # global heightMy
    # global widthMy
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

        print(" 323 height_VNB = ", height_VNB)
        print("  knitpatByte_black_VNB = ", knitpatByte_black_VNB)
        print("  l372_widthMyPatternInBytes = ", widthMyPatternInBytes)
        print(" heightMy = ", heightMy)
        print(" widthMy = ", widthMy)
    except IOError:
        self.errorDialog("!no knitpatBytetern VNB")

    """
    # num = 


    print(" 295 knitpatByte_white_VNB")
    print(knitpatByte_white_VNB)  # printing the value
    print(" 297 knitpatByte_black_VNB")
    print(" 0," , knitpatByte_black_VNB[0])

    print(" 300 bytes(knitpatByte_black_VNB[0]) =  ")
    print(bytes(knitpatByte_black_VNB[0]))
    """

    # ser.write(bytes(knitpatByte_black_VNB[0]))
    # line = ser.readline()
    # received.append(line.decode().strip())
    print("datetime.datetime.now() - start)=")
    print(datetime.datetime.now() - start)

    begin2(widthMyPatternInBytes, heightMy, widthMy)

# -------------------------------------

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
        # newString = bytes(chr(n), "ascii")  + bytes("fgh", "ascii")
        newString = bytes(chr(n), "ascii") + bytes(chr(n), "ascii") + bytes("+", "ascii")
        ser.write(newString)
        time.sleep(0.01)
        # print(" recived=")

        '''        
        received = read_lines(ser)
        time.sleep(0.01)
        print("dataFromConsole=", received, " ! ")
        strReceived = str(received)'''

        receiving()


app = QApplication(sys.argv)


while 1 == 1:
    w = Window()
    w.show()
    app.exec()

# ----------------------------



if __name__ == '__main__':
    begin()
    # blackANDwhite()
    # app = QApplication(sys.argv)
    # ex = App()
    # sys.exit(app.exec_())
