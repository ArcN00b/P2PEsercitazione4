#!/usr/bin/python3
from Utility import *
import os

class Divider:

    ## metodo che esegue la divisione del file in parti
    @staticmethod
    def divide (path_dir, path_temp, file_name, len_part):

        pathdir = path_dir
        pathtemp = path_temp
        lenpart = Utility.LEN_PART
        nomeFComp = file_name
        numpart = 0

        lenfile = os.path.getsize(pathdir + nomeFComp)
        respart = lenfile % lenpart

        if respart > 0:
            numpart = int(lenfile / lenpart) + 1
        else:
            numpart = int(lenfile / lenpart)

        fcomp = open(pathdir + nomeFComp, "rb")
        for i in range(0, numpart):
            if i == numpart and respart > 0:
                buffer = fcomp.read(respart)
            else:
                buffer = fcomp.read(lenpart)
            with open(pathtemp + nomeFComp + str(i), "wb") as myfile:
                myfile.write(buffer)

        fcomp.close()
