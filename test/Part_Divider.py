#!/usr/bin/python3

from Utility import *
import os
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':

    file_name = 'Sevendust - Walk Away.mp3'
    path_file = Utility.PATHDIR + file_name
    temp_folder = Utility.PATHDIR + 'temp/'

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    len_file = os.stat(path_file).st_size
    num_part = len_file // Utility.LEN_PART

    if len_file % Utility.LEN_PART != 0:
        num_part += 1

    print('lunghezza file in Bytes: ' + str(len_file))
    print('numero delle parti: ' + str(num_part))

    temp_file = temp_folder + file_name

    for i in range(0, num_part):
        out_file = open(temp_file + '.tmp' + str(i), 'wb')

        in_file = open(path_file, 'rb')
        bytes_readed = in_file.read(Utility.LEN_PART)

        out_file.write(bytes_readed)
        out_file.flush()
        out_file.close()

    print('diviso il file in parti nella cartella temp')


