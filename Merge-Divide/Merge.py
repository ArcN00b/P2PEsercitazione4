#!/usr/bin/python3
from Utility import *
import os

pathdir = '/home/riccardo/Scrivania/FileProgetto/'
pathtemp = '/home/riccardo/Scrivania/FileProgetto/Temp/'
nomeFComp = 'Mona.jpg'
nomeFDim = 'MonaTest.jpg'

fCompleto = open(pathdir + nomeFComp, "wb")
fCompleto.close()

lenfile = os.path.getsize(pathdir + nomeFDim)
respart = lenfile % Utility.LEN_PART

if respart > 0:
    numpart = int(lenfile / Utility.LEN_PART) + 1
else:
    numpart = int(lenfile / Utility.LEN_PART)

for i in range(1, numpart + 1):
    fParte = open(pathtemp + nomeFComp + str(i), "rb")
    buffer = fParte.read()
    with open(pathdir + nomeFComp, "ab") as myfile:
        myfile.write(buffer)
    fParte.close()
