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
    def login_ack(sock_end):
        try:
            data = sock_end.recv(512)
            #data = data.encode()
            command, fields = Parser.parse(data)

            ## ritorno del sessionID
            return fields[0]

        except Exception as e:
            logging.debug("ERROR on Receive " + str(e))

    ## metodo che gestisce la risposta della logout
    @staticmethod
    def logout_ack(sock_end):
        try:
            data = sock_end.recv(512)
            #data = data.encode()
            command, fields = Parser.parse(data)

            if command == 'NLOG':
                n_part_down = fields[0]
                return False, n_part_down
            else:
                n_part_own = fields[0]
                return True, n_part_own

        except Exception as e:
            logging.debug("ERROR on Receive " + str(e))

    @staticmethod
    def aloo(socket):
        lista=[]
        data=socket.recv(7)
        cmd,fields=Parser.parse(data,None)
        numMd5=fields[0]
        for i in range(0,numMd5):
            dim=148
            d=socket.recv(dim)
            while len(d)<dim:
                tmp=socket.recv(dim-len(d))
                d=d+tmp

            md5_i=d[0:32].decode()
            name=d[32:132].decode()
            lFile=d[132:142].decode()
            lPart=d[142:148].decode()
            name=name.strip(' ')
            testo=md5_i+' '+name+' '+lFile+' '+lPart
            lista.append(testo)

        return lista

    ## questo metodo chiude la socket verificando se
    ## effettivamente si riesce a chiudere
    @staticmethod
    def close_socket(sock_end):
        try:
            sock_end.close()
        except Exception as e:
            logging.debug("ERROR on Close " + str(e))