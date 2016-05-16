
from Utility import *
#from Request import *
from Response import *
from Merge_Divide import Merge
import time
import Request
import random
import threading
import socket

## il thread download manager riesce a gestire max download paralleli
class Download_Manager(threading.Thread):
    def __init__(self, progress_bar, var_progress, num_parts, semaphore, listaPart, md5, name):
        threading.Thread.__init__(self)
        self.progress_bar = progress_bar
        self.num_parts = num_parts
        self.semaphore = semaphore
        self.listaPart = listaPart
        self.md5 = md5
        self.name = name
        self.var_progress = var_progress

    def run(self):
        # lista join thread e semaforo con coda
        threads = []

        for i in range(0, len(self.listaPart)):
            # Prendo la parte interessata ed eseguo il download
            nPeer = len(self.listaPart[i]) - 1
            down = random.randint(0, nPeer - 1)
            datiDown = self.listaPart[i][down + 1]
            datiDown = datiDown.split('-')
            parte = int(self.listaPart[i][0])

            # Chiamata al download
            try:
                self.semaphore.acquire()
                ts = Downloader(self.semaphore, self.progress_bar, self.num_parts, datiDown[0], datiDown[1], self.md5, self.name, parte)
                threads += [ts]
                ts.start()
            except Exception as e:
                self.semaphore.release()
                logging.debug("ERROR on Download " + str(e))

        for t in threads:
            t.join()

        # Verifico se sono stati scaricati tutti i file e in tal caso eseguo il merge
        # Verifico se non è presente nessun 0 nella lista delle parti
        if not ('0' in ((Utility.database.findPartForMd5(self.md5))[0][1])):
            # Ho tutte le parti ed eseguo il merge di tutte le parti di file
            # Prelevo lenFile e lenPart rispettivamente in row[0][0] e in row[0][1]
            row = Utility.database.findFile(0, self.md5, 0, 4)
            lenFile = int(row[0][0])
            lenPart = int(row[0][1])

            # nPart = len((Utility.database.findPartForMd5(md5))[0][1])
            Merge.Merger.merge(self.name, lenFile, lenPart)
            print("Merge completato")
            self.var_progress.set('Download completato')

            # Avviso il tracker di avere il file completo
            try:
                msgFile = 'ADDR' + Utility.sessionID + '{:0>10}'.format(lenFile) + '{:0>6}'.format(lenPart) + self.name.ljust(100) + self.md5
                addTracker = Request.Request.create_socket(Utility.IP_TRACKER, int(Utility.PORT_TRACKER))
                sentTracker = addTracker.send(msgFile.encode())

                # Aggiungo il file al database
                Utility.database.addFile(Utility.sessionID, self.name, self.md5, lenFile, lenPart)

                # Attendo risposta aggiunta file
                Response.add_file_ack(addTracker)
                Request.Request.close_socket(addTracker)

                # TODO pensare a come agire in caso di ADDR non inviata correttamente
                if sentTracker is None or sentTracker < len(msgFile):
                    print('ADDR non riuscita in download')
                    return

            except Exception as e:
                print(e)

class Downloader(threading.Thread):
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, semaphore, progress_bar, num_parts, ipp2p, pp2p, md5, name, part):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.semaphore = semaphore
        self.progress_bar = progress_bar
        self.num_parts = num_parts
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

        try:
            sock.connect((ind, int(pp2p)))
            mess = 'RETP' + md5 + '{:0>8}'.format(int(part))
            sent = sock.send(mess.encode())
            if sent is None or sent < len(mess):
                sock.close()
                raise Exception('recupero non effettuato')

            # ricevo i primi 10 Byte che sono "ARET" + n_chunk
            recv_mess = sock.recv(10).decode()
        except Exception as e:
            sock.close()
            raise Exception("ERRORE :" + str(e))

        if recv_mess[:4] == "AREP":
            try:
                num_chunk = int(recv_mess[4:])
                print("Download avviato")

                # Finchè i chunk non sono completi
                print("Download in corso", end='\n')
                buff = bytes()
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
                    buff += buffer

                # apro il file per la scrittura
                f = open(Utility.PATHTEMP + name.rstrip(' ') + str(int(part)), "wb")
                f.write(buff)  # Scrivo il contenuto del chunk nel file
                self.progress_bar.step(100/self.num_parts)
                f.close()
                sock.close()

                print('download parte completato')
            except Exception as e:
                raise Exception("--- ERRORE DOWNLOAD PARTE : " + e)

            try:
                # Avviso il tracker di aver completato il download della parte del file
                sockTracker = Request.Request.create_socket(Utility.IP_TRACKER, int(Utility.PORT_TRACKER))
                sentTracker = Request.Request.rpad(sockTracker, Utility.sessionID, md5, part)
                # TODO pensare a come agire in caso di RPAD non inviata correttamente
                if sentTracker is None or sentTracker < 60:
                    raise Exception('RPAD non riuscita in download')

                num_parts = Response.rpad_ack(sockTracker)
                Request.Request.close_socket(sockTracker)
                logging.debug('parti del tracker: ' + str(num_parts))

                # Aggiungo la parte alla lista delle parti nel database
                strPart = (Utility.database.findPartForMd5AndSessionId(Utility.sessionID, md5))[0][0]
                strPart = strPart[:part] + '1' + strPart[part+1:]
                Utility.database.updatePart(Utility.sessionID, md5, strPart)

            except Exception as e:
                raise Exception('-- Errore comunicazione parte scaricata RPAD: ' + e)

        self.semaphore.release()




