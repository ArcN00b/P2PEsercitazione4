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
            request = request + Utility.IP_MY + '{:0>5}'.format(Utility.PORT_MY)
            sock_end.send(request.encode())
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
            sock_end.send(request.encode())
            logging.debug('inviato logo ' + Utility.SessionID)
        except Exception as e:
            logging.debug("ERROR on Send " + str(e))

    # Metodo che gestisce invia una look
    @staticmethod
    def look(socket,ssId,serch):
        try:
            serch=serch+' '*(20-len(serch))
            msg='LOOK'+ssId+serch
            socket.send(msg.encode())
            logging.debug("Inviata look")
        except Exception as e:
            logging.debug("Errore look "+str(e))

    # Metodo che invia una FCHU
    @staticmethod
    def fchu(socket,ssid,md5):
        try:
            msg="FCHU"+ssid+md5
            socket.send(msg.encode())
            logging.debug("Inviata fchu")
        except Exception as e:
            logging.debug("Errore fchu "+str(e))

    # Metodo che invia un messaggio generico
    @staticmethod
    def sendMessagge(socket,messaggio):
        try:
            socket.send(messaggio.encode())
            logging.debug("Inviato msg "+messaggio)
        except Exception as e:
            logging.debug("Errore invio messaggio "+str(e))

    ## questo metodo chiude la socket verificando se
    ## effettivamente si riesce a chiudere
    @staticmethod
    def close_socket(socket_end):
        try:
            socket_end.shutdown()
            socket_end.close()
        except Exception as e:
            logging.debug("ERROR on Close " + str(e))

