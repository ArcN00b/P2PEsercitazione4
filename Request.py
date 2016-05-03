#!/usr/bin/python3

from Utility import *
import socket
import random
import logging
import os

class Request:

##  metodo che effettua la richiesta di una login
##  il metodo apre una socket su un indirizzo e porta del tracker
##  per poi inviare le informazioni
    @staticmethod
    def create_socket(ip_tracker, port_tracker):
        try:
            r = random.randrange(0, 100)
            ipv4, ipv6 = Utility.getIp(ip_tracker)
            if r < 50:
                a = ipv4
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                a = ipv6
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

            ## connessione al terminale
            sock.connect((a, int(port_tracker)))
            logging.debug('connesso a ' + a + ':' + str(port_tracker))

            ## ritorno della socket al chiamante
            return sock
        except Exception as e:
            print("Errore Peer down " + ip_tracker + " " + port_tracker)

    ## questo metodo che riceve una socket scrive la login su tale
    ## backend verificando l'invio
    @staticmethod
    def login(sock_end):
        try:
            request = "LOGI"
            request = request + Utility.IP_MY + Utility.PORT_MY
            sock_end.send(request)
            logging.debug("inviato logi")
        except Exception as e:
            logging.debug("ERROR on Send login" + str(e))

    ## metodo che data una socket di ingresso invia al
    ## terminale le informazioni per il logout
    @staticmethod
    def logout(sock_end):
        try:
            request = 'LOGO'
            request = request + Utility.SessionID
            sock_end.send(request)
            logging.debug('inviato logo ' + Utility.SessionID)
        except Exception as e:
            logging.debug("ERROR on Send logout" + str(e))

    ## metodo che ricevendo un valore di ricerca
    ## e un socket invia una richiesta di ricerca
    @staticmethod
    def look(sock_end, search):
        try:
            search = search.ljust(20)
            request = 'LOOK' + Utility.SessionID + search
            sock_end.send(request)
            logging.debug("Inviata look")
        except Exception as e:
            logging.debug("Errore look "+str(e))

    ## metodo che ricevendo il percorso di un file
    ## estrae la lunghezza e il numero di parti
    @staticmethod
    def add_file(sock_end, path_file):
        try:
            md5_file = Utility.generateMd5(path_file)
            file_name = path_file.split('/')[-1]
            len_file = os.stat(path_file).st_size
            request='ADDR' + Utility.SessionID
            request = request + len_file.zfill(10) + Utility.LEN_PART.zfill(6)
            reqeust = request.ljust(100) + md5_file
            sock_end.send(request)

        except Exception as e:
            logging.debug("Error on Send add_file " + str(e))


    ## questo metodo chiude la socket verificando se
    ## effettivamente si riesce a chiudere
    @staticmethod
    def close_socket(socket_end):
        try:
            socket_end.shutdown()
            socket_end.close()
        except Exception as e:
            logging.debug("ERROR on Close " + str(e))

