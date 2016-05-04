#!/usr/bin/python3

from Parser import *
from Utility import *
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
            command, fields = Parser.parse(data)

            if command == 'NLOG':
                n_part_down = fields[0]
                return False, n_part_down
            else:
                n_part_own = fields[0]
                return True, n_part_own

        except Exception as e:
            logging.debug("ERROR on Receive logout_ack" + str(e))

    ## metodo per ricevere la risposta dalla look
    ## quindi si riceve 'ALOO'
    @staticmethod
    def look_ack(sock_end):
        try:
            lista=[]
            data=sock_end.recv(7)
            cmd,fields=Parser.parse(data)
            numMd5=fields[0]
            for i in range(0,numMd5):
                dim=148
                d=sock_end.recv(dim)

                ## ciclo per continuare a ricevere fino ai 148 caratteri
                while len(d)<dim:
                    tmp=sock_end.recv(dim-len(d))
                    d=d+tmp

                ## estrazione delle informazioni
                md5_i=d[0:32].decode()
                name=d[32:132].decode()
                lFile=d[132:142].decode()
                lPart=d[142:148].decode()
                name=name.strip(' ')

                ## tupla contenente le informazioni
                obj= (md5_i,name,lFile,lPart)
                ## aggiornamento alla lista
                lista.append(obj)

            return lista

        except Exception as e:
            logging.debug("ERROR on Receive aloo" + str(e))

    ## metodo per la ricezione dell'aggiunta
    ## dei file da tracciare al tracker 'AADR'
    @staticmethod
    def add_file_ack(sock_end):
        try:
            data = sock_end.recv(512)
            command, fields = Parser.parse(data)
            num_parts = fields[0]
            return num_parts

        except Exception as e:
            logging.debug("ERROR on Receive aadr" + str(e))

    # Metodo per gestire la AFCH
    @staticmethod
    def afch(socket,numPart8):
        listaPeer=[] # E una lista di liste,
        data=socket.recv(7)
        cmd,fields=Parser.parse(data,None)
        numHit=fields[0]
        for i in range(0,numHit):
            dim=55+5+numPart8
            d=socket.recv(dim)
            while len(d)<dim:
                tmp=socket.recv(dim-len(d))
                d=d+tmp

            lista=[]
            ip_i=d[0:55].decode()
            port_i=d[55:60].decode()
            part=d[60:(60+numPart8)]
            strPart=Utility.toBytes(part)
            lista.append(ip_i)
            lista.append(port_i)
            lista.append(strPart)
            listaPeer.append(lista)

        return listaPeer

    ## questo metodo chiude la socket verificando se
    ## effettivamente si riesce a chiudere
    @staticmethod
    def close_socket(sock_end):
        try:
            sock_end.close()
        except Exception as e:
            logging.debug("ERROR on Close " + str(e))