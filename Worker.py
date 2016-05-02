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
                True
                # TODO da scrivere

            elif command == "ALGI":
                True
                # Todo da scrivere

            elif command == "ADDR":
                True
                # TOdo da scrivere

            elif command == "AADR":
                True
                # Todo da Scrivere

            elif command == "LOOK":
                msgRet=""
                self.database


            elif command == "ALOO":
                True
                # Todo da scrivere

            elif command == "FCHU":
                True
                # Todo da scrivere

            elif command == "AFCH":
                True
                # Todo da scrivere

            elif command == "RETP":
                True
                # Todo da scrivere

            elif command == "AREP":
                True
                # Todo da scrivere

            elif command == "RPAD":
                True
                # Todo da scrivere

            elif command == "APAD":
                True
                # TOdo da scrivere

            elif command == "LOGO":
                True
                # Todo da scrivere

            elif command == "NLOG":
                True
                # Todo da scrivere

            elif command == "ALOG":
                True
                # Todo da scrivere

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
        self.client.shutdown()
        self.client.close()
