import random
import time
import hashlib
import ManageDB
import socket
import threading

class Utility:
    IPv4_TRACKER = "172.030.007.001"
    IPv6_TRACKER = "fc00:0000:0000:0000:0000:0000:0007:0001"
    IP_TRACKER = "172.030.007.001|fc00:0000:0000:0000:0000:0000:0007:0001"

    PORT_TRACKER = 3000

    IPV4_MY = "172.030.007.003"
    IPV6_MY = "fc00:0000:0000:0000:0000:0000:0007:0003"
    IP_MY = "172.030.007.003|fc00:0000:0000:0000:0000:0000:0007:0003"

    PORT_MY = 12345
    PATHDIR = '/home/marco/seedfolder'

    ## variabili condivise in piu' parti del programma
    SessionID = ''

    @staticmethod
    def getIp(stringa):
        t = stringa.find('|')
        if t != -1:

            ''' Modifico così questa funzione poiche se usiamo una connect di un indirizzo come 127.000.000.001
                purtroppo da errore, così trasformo l'ip sopra in 127.0.0.1'''
            ipv4 = ''
            tmp = stringa[0:t].split('.')
            for grp in tmp:
                if len(grp.lstrip('0')) == 0:
                    ipv4 += '0.'
                else:
                    ipv4 += grp.lstrip('0') + '.'
            ipv4 = ipv4[0:-1]
            # estrazione ipv6
            ipv6 = ''
            tmp = stringa[t+1:].split(':')
            for grp in tmp:
                w = grp.lstrip('0')
                if len(w) != 0:
                    ipv6 += w + ':'
                else:
                    ipv6 += '0:'
            ipv6 = ipv6[0:-1]
            return ipv4, ipv6
        else:
            return '', ''

