#!/usr/bin/python3

from Parser import *
import random
import logging

#Tutti i metodi eseguono le operazioni sul database
#Necessitano quindi che sia passato il database in ingresso
class Response:

    #Metodo per la generazione della risposta ad una richiesta di login
    #Ritorna una stringa rappresentante il messaggio da inviare
    @staticmethod
    def login_ack(socket_end):
        try:
            data = socket_end.recv(512)
            data = data.encode()
            command, fields = Parser.parse(data)

            ## ritorno del sessionID
            return fields[0]

        except Exception as e:
            logging.debug("ERROR on Receive " + str(e))


    ## questo metodo chiude la socket verificando se
    ## effettivamente si riesce a chiudere
    @staticmethod
    def close_socket(socket_end):
        try:
            socket_end.close()
        except Exception as e:
            logging.debug("ERROR on Close " + str(e))