import threading
import socket
import struct
from Parser import *
from Response import *
from ManageDB import *


# Costruttore che inizializza gli attributi del Worker
class Worker(threading.Thread):
    client = 0
    database = None

    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, client, database, lock):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.client = client
        self.database = database

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def run(self):
        try:
            self.comunication()
        except Exception as e:
            print("errore: ", e)
            if self.lock.acquired():
                self.lock.release()
            self.client.shutdown()
            self.client.close()

    # Funzione che viene eseguita dal thread Worker
    def comunication(self):

        # ricezione del dato e immagazzinamento fino al max
        data = self.client.recv(2048)
        print("comando ricevuto: " + str(data))
        running = True

        # ciclo continua a ricevere i dati
        while running and len(data) > 0:

            # recupero del comando
            buffer = data.decode()
            command, fields = Parser.parse(buffer)
            # risposta da inviare in modo sincronizzato
            self.lock.acquire()
            resp = ""
            # TODO modificare che comando eseguire in che caso

            # controllo del comando effettuato
            # LOGI
            if command == "LOGI":
                # recupero ip e porta
                ipp2p = fields[0]
                pp2p = fields[1]

                # costruzione della risposta "ALGI"
                resp = Response.login(self.database, ipp2p, pp2p)
            # ADDF
            elif command == "ADDF":
                # recupero session id
                sessionID = fields[0]
                # recupero filemd5
                fileMD5 = fields[1]
                # recupero file name
                fileName = fields[2]

                # controllo se l'utente si e' precedentemente loggato
                if len(self.database.findClient(sessionID, '', '', '2')) != 0:
                    resp = Response.addFile(self.database, fileMD5, sessionID, fileName)
                else:
                    # rispondo con 000 per indicare file non aggiunto
                    resp = "AADD" + "000"
            # DELF
            elif command == "DELF":
                # recupero sessionID
                sessionID = fields[0]
                # recupero del fileMD5
                fileMD5 = fields[1]
                # controllo se l'utente si e' precedentemente loggato
                if len(self.database.findClient(sessionID, '', '', '2')) != 0:
                    resp = Response.remove(self.database, fileMD5, sessionID)
                else:
                    # rispondo con 000 per indicare file non rimosso
                    resp = "AADD" + "999"
            # FIND
            elif command == "FIND":
                # recupero sessionID
                sessionID = fields[0]
                # recupero campo di ricerca
                campo = fields[1];
                # controllo se l'utente si e' precedentemente loggato
                if len(self.database.findClient(sessionID, '', '', '2')) != 0:
                    resp = Response.search(self.database, campo)
                else:
                    # rispondo con 000 se utente non autorizzato
                    resp = "AFIN" + "000"
            # DREG
            elif command == "DREG":
                # recupero del sessionID
                sessionID = fields[0]
                # recupero fileMD5
                fileMD5 = fields[1]
                # controllo se l'utente si e' precedentemente loggato
                if len(self.database.findClient(sessionID, '', '', '2')) != 0:
                    resp = Response.download(self.database, sessionID, fileMD5)
                else:
                    # utente non presente, nessun file scaricato da aggiornare
                    resp = "ADRE" + "000"
            # LOGO
            elif command == "LOGO":
                # recupero sessionID
                sessionID = fields[0]
                # controllo se l'utente si e' precedentemente loggato
                if len(self.database.findClient(sessionID, '', '', '2')) != 0:
                    resp = Response.logout(self.database, sessionID)
                else:
                    # utente non presente nessun file da eliminare
                    resp = "ALGO" + "000"

                # termine del ciclo
                running = False
            # se non ricevo niente di valido response va a none
            else:
                resp = None
                running = False

            # invio della risposta creata controllando che sia valida
            self.lock.release()
            #print(resp+'\r\n')
            if resp is not None:
                self.client.sendall(resp.encode())
            print("comando inviato: " + resp)

            # ricezione del dato e immagazzinamento fino al max
            data = self.client.recv(2048)

        # fine del ciclo

        # chiude la connessione quando non ci sono più dati
        print("Chiusura socket di connessione")
        # chiude il client
        self.client.close()
