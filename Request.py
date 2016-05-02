#!/usr/bin/python3

from Utility import *
import socket
import random
import logging


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
            logging.debug("ERROR on Send " + str(e))

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
            logging.debug("ERROR on Send " + str(e))

    ## questo metodo chiude la socket verificando se
    ## effettivamente si riesce a chiudere
    @staticmethod
    def close_socket(socket_end):
        try:
            socket_end.close()
        except Exception as e:
            logging.debug("ERROR on Close " + str(e))

