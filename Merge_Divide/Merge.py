#!/usr/bin/python3
from Utility import *
import os

class Merger:

    ## metodo che esegue il ricompattamento del file
    ## quando tutte le prati sono temporanee
    @staticmethod
    def merge (file_name, lenFile, lenPart):

        name = file_name

        nPart = int(lenFile / lenPart)
        if (lenFile % lenPart > 0):
            nPart = nPart + 1

        # Cancello il contenuto del file
        fCompleto = open(Utility.PATHDIR + name.rstrip(' '), "wb")
        fCompleto.close()

        # Raggruppo le parti in un unico file
        for i in range(1, nPart + 1):
            # Aggiungo la parte i-esima in coda al file
            fParte = open(Utility.PATHTEMP + name.rstrip(' ') + str(i), "rb")
            buffer = fParte.read()

            # Scrivo all'interno del file e chiudo il file completo
            with open(Utility.PATHDIR + name.rstrip(' '), "ab") as myfile:
                myfile.write(buffer)

            # Chiusura del file della parte
            fParte.close()
