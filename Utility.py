import random
import time
import hashlib
import ManageDB
import socket
import threading

class Utility:
    IPv4_TRACKER = "172.030.007.010"
    IPv6_TRACKER = "fc00:0000:0000:0000:0000:0000:0007:0010"
    IP_TRACKER = IPv4_TRACKER+'|'+IPv6_TRACKER

    PORT_TRACKER = 3000

    IPV4_MY = "172.030.007.007"
    IPV6_MY = "fc00:0000:0000:0000:0000:0000:0007:0007"
    IP_MY = IPV4_MY+'|'+IPV6_MY

    PORT_MY = 12345
    ATTESA=60  # Attesa prima di rieseguire una FCHU
    NUMDOWNPARALLELI=20

    PATHDIR = '/home/marco/seedfolder/'
    PATHTEMP = '/home/marco/seedfolder/temp/'

    ## variabili condivise in piu' parti del programma
    LEN_PART = 262144

    sessionID = ''
    listLastSearch=[]
    blocco = threading.Lock()
    lock = False

    #semaforo=threading.Semaphore(1)

    database = ManageDB.ManageDB()

    # Metodo per trasformare un vettore di byte nella stringa di bit
    @staticmethod
    def toBit(stringa):
        s=stringa
        # converto i byte in una stringa
        tmp=''
        for i in range(0,len(s)):
            t=bin(s[i])[2:]
            t='0'*(8-len(t))+t
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
        tmp=bytes()
        print(n)
        for i in range(0,n):
            s=stringa[(i*8):(i*8+8)]
            #t=s[::-1]
            #s=s.lstrip('0')
            a=int(s,2)
            s=bytes([a])
            tmp=tmp+s

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
        # Inizializzo le variabili che utilizzerò
        f = open(path, 'rb')
        hash = hashlib.md5()

        # Per una lettura più efficiente suddivido il file in blocchi
        buf = f.read(4096)
        while len(buf) > 0:
            hash.update(buf)
            buf = f.read(4096)

        hash.update((Utility.IPV4_MY+'|'+Utility.IPV6_MY+str(Utility.PORT_MY)).encode())

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

    # Metodo che controlla che tutte le parti del file siano presenti almeno in una occorrenza della lista
    @staticmethod
    def partChecker(listParts, length):
        for j in range(0, length):

            # Controllo che sia presente almeno un 1 in posizione "j" tra tutte le righe della lista
            match = False
            for i in range(0, len(listParts)):
                if listParts[i][j] == '1':
                    match = True
                    break

            # Se non ho trovato un 1 in quella posizione allora ritorno False
            if not match:
                return False

        # Ritorno true se complessivamente tutte le parti del file sono disponibili in rete
        return True

    # Metodo che conta il numero parti con almeno un 1 all'interno della lista
    @staticmethod
    def partCounter(listParts, length):
        count = 0
        for j in range(0, len(listParts[0][0])):

            # Controllo che sia presente almeno un 1 in posizione "j" tra tutte le righe della lista
            match = False
            for i in range(0, len(listParts)):
                if listParts[i][0][j] == 1:
                    match = True
                    break

            # Se ho trovato un 1 in quella posizione allora incremento il contatore
            if match:
                count += 1

        # Ritorno il contatore
        return count