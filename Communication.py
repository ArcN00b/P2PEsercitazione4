
from Utility import *
#from Request import *
from Response import *
from Merge_Divide import Merge
import time
import Request
import random
import threading
import socket

class Downloader(threading.Thread):
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, ipp2p, pp2p, md5, name, part):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.ipp2p = ipp2p
        self.pp2p = pp2p
        self.md5 = md5
        self.name = name
        self.part=part

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def run(self):
        #try:
        ipp2p = self.ipp2p
        pp2p = self.pp2p
        md5 = self.md5
        name = self.name
        part = self.part

        r = random.randrange(0,100)
        ipv4, ipv6 = Utility.getIp(ipp2p)
        if r < 50:
            ind = ipv4
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            ind = ipv6
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        sock.connect((ind, int(pp2p)))
        mess = 'RETP' + md5 + '{:0>8}'.format(int(part))
        sent = sock.send(mess.encode())
        if sent is None or sent < len(mess):
            print('recupero non effettuato')
            sock.close()
            return

        # ricevo i primi 10 Byte che sono "ARET" + n_chunk
        recv_mess = sock.recv(10).decode()
        if recv_mess[:4] == "AREP":
            num_chunk = int(recv_mess[4:])
            print("Download avviato")

            # apro il file per la scrittura
            # Apro il file rimuovendo gli spazi finali dal nome
            # Aggiungo al nome la parte del file scaricata
            f = open(Utility.PATHTEMP + name.rstrip(' ') + str(int(part)), "wb")

            # Finchè i chunk non sono completi
            print("Download in corso", end='\n')
            for count_chunk in range(0, num_chunk):
                tmp = sock.recv(5)  # leggo la lunghezza del chunk
                while len(tmp) < 5:
                    tmp += sock.recv(5 - len(tmp))
                    if len(tmp) == 0:
                        raise Exception("Socket close")

                # Eseguo controlli di coerenza su ciò che viene ricavato dal socket
                try:
                    int(tmp.decode())
                except Exception as e:
                    raise Exception("number format exception")

                chunklen = int(tmp.decode())
                buffer = sock.recv(chunklen)  # Leggo il contenuto del chunk

                # Leggo i dati del file dal socket
                while len(buffer) < chunklen:
                    tmp = sock.recv(chunklen - len(buffer))
                    buffer += tmp
                    if len(tmp) == 0:
                        raise Exception("Socket close")

                f.write(buffer)  # Scrivo il contenuto del chunk nel file

            f.close()
            print("Download completato")

            # Avviso il tracker di aver completato il download della parte del file
            msgPart = 'RPAD' + Utility.sessionID + md5 + '{:0>8}'.format(int(part))
            sockTracker = Request.Request.create_socket(Utility.IP_TRACKER, int(Utility.PORT_TRACKER))
            sentTracker = sockTracker.send(msgPart.encode())
            # TODO pensare a come agire in caso di RPAD non inviata correttamente
            if sentTracker is None or sentTracker < len(msgPart):
                print('RPAD non riuscita in download')
                return

            # TODO pensare a incongruenze aggiungendo parte al database se non viene avvisato il tracker
            # TODO inserire il codice di merge in un try catch?
            # Aggiungo la parte alla lista delle parti nel database
            strPart = (Utility.database.findPartForMd5AndSessionId(Utility.sessionID, md5))[0][0]
            strPart = strPart[:part] + '1' + strPart[part+1:]
            Utility.database.updatePart(Utility.sessionID, md5, strPart)

            # Verifico se sono stati scaricati tutti i file e in tal caso eseguo il merge
            # Verifico se non è presente nessun 0 nella lista delle parti
            if not('0' in ((Utility.database.findPartForMd5(md5))[0][1])):
                # Ho tutte le parti ed eseguo il merge di tutte le parti di file

                # Prelevo lenFile e lenPart rispettivamente in row[0][0] e in row[0][1]
                row = Utility.database.findFile(0,md5,0,4)
                lenFile = int(row[0][0])
                lenPart = int(row[0][1])

                #nPart = len((Utility.database.findPartForMd5(md5))[0][1])
                Merge.Merger.merge(name, lenFile, lenPart)

                # Avviso il tracker di avere il file completo
                msgFile = 'ADDR' + Utility.sessionID + '{:0>10}'.format(lenFile) + '{:0>6}'.format(lenPart) + name.ljust(100) + md5
                addTracker = Request.Request.create_socket(Utility.IP_TRACKER, int(Utility.PORT_TRACKER))
                sentTracker = addTracker.send(msgFile.encode())

                # Aggiungo il file al database
                Utility.database.addFile(Utility.sessionID,name,md5,lenFile,lenPart)

                # Attendo risposta aggiunta file
                Response.add_file_ack(addTracker)
                Request.Request.close_socket(addTracker)
                # TODO pensare a come agire in caso di ADDR non inviata correttamente
                if sentTracker is None or sentTracker < len(msgFile):
                    print('ADDR non riuscita in download')
                    return

        Request.Request.close_socket(sockTracker)
        Request.Request.close_socket(sock)
