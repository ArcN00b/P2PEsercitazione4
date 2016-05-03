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

    ## variabili condivise in piu' parti del programma
    SessionID = ''
    listFindPeer = []
    listFindFile = []
    listResultFile = []
    numFindSNode=0
    listFindSNode=[]
    superNodo=False # Indica se il programma in esecuzione e' un SuperNodo o un Peer
    ipSuperNodo='' # Indica l'ip del SuperNodo a cui il Peer e' collegato
    portSuperNodo='' # Indica la porta del SuperNodo a cui il Peer e' collegato
    sessionId='' # Indica il sessionId del Peer
    database = ManageDB.ManageDB()

    # Metodo per trasformare un vettore di byte nella stringa di bit
    @staticmethod
    def toBit(stringa):
        if type(stringa) is str:
            s=bytes(stringa,'utf-8')
        else:
            s=stringa
        # converto i byte in una stringa
        tmp=''
        for i in range(0,len(s)):
            t=bin(s[i])[2:]
            t='0'*(8-len(t))+t
            t=t[::-1]
            tmp= tmp+t

        return tmp

    # Metodo per trasformare una stringa di bit in un vettore di byte
    # Prende la stringa e il numero di byte che sono presenti nella stringa
    @staticmethod
    def toBytes(stringa,num):
        if num==0:
            n=int(len(stringa)/8)
        else:
            n=num
        tmp=b''
        print(n)
        for i in range(0,n):
            s=stringa[(i*8):(i*8+8)]
            t=s[::-1]
            s=s.lstrip('0')
            s=chr(int(t,2))
            tmp=tmp+bytes(s,'utf-8')

        return tmp


    # Metodo che genera un numero random nel range [1024, 65535]
    @staticmethod
    def generatePort():
        random.seed(time.process_time())
        return random.randrange(1024, 65535)
    # Questo metodo genera un packet id randomico
    # Chiede di quanti numeri deve essere il valore generato
    @staticmethod
    def generateId(lunghezza):
        random.seed(time.process_time())
        seq = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        val = ''
        for i in range(0, lunghezza):
            val = val + random.choice(seq)
        return val

    # Metodo per generare l'md5 di un file, va passato il percorso assoluto
    @staticmethod
    def generateMd5(path):

        #path="/home/flavio/Scrivania/pippo.txt"
        # Inizializzo le variabili che utilizzerò
        f = open(path, 'rb')
        hash = hashlib.md5()

        # Per una lettura più efficiente suddivido il file in blocchi
        buf = f.read(4096)
        while len(buf) > 0:
            hash.update(buf)
            buf = f.read(4096)

        hash.update(Utility.IPV4_MY+'|'+Utility.IPV6_MY+str(Utility.PORT_MY))

        # Return del digest
        return hash.hexdigest()

        # Ritorna i due ip data la stringa generale
        # Ritorna prima ipv4 e poi ipv6

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

