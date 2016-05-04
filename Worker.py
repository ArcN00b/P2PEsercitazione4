import threading
import socket
import struct
from Parser import *
from Response import *
from ManageDB import *
from Utility import *


# Costruttore che inizializza gli attributi del Worker
class Worker(threading.Thread):
    client = 0
    database = None
    lock = None

    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, client, database):
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
            self.client.shutdown(1)
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
            buffer = data
            command, fields = Parser.parse(buffer)
            # risposta da inviare in modo sincronizzato
            resp = ""
            # TODO modificare che comando eseguire in che caso

            # controllo del comando effettuato
            # LOGI
            if command == "LOGI":
                # Todo da testare
                msgRet="ALGI"
                try:
                    ip=fields[0]
                    port=fields[1]
                    dati=self.database.findPeer(None,ip,port,1)
                    if len(dati)>0:
                        ssId=dati[0][0]
                        msgRet=msgRet+ssId
                    else:
                        ssId=Utility.generateId(16)
                        msgRet=msgRet+ssId
                except:
                    ssId='0'*16
                    msgRet=msgRet+ssId
                finally:
                    self.client.sendall(msgRet.encode())

            elif command == "ALGI":
                True
                # Todo da scrivere

            elif command == "ADDR":
                # Todo da testare
                msgRet="AADR"
                ssId=fields[0]
                lFile=fields[1]
                lPart=fields[2]
                name=fields[3]
                md5=fields[4]
                if len(self.database.findPeer(ssId,None,None,2))>0:
                    a=int(lFile)
                    b=int(lPart)
                    if a%b==0:
                        numPart=a//b
                    else:
                        numPart=(a//b)+1

                    if numPart%8==0:
                        numPart8=numPart//8
                        parte='1'*numPart
                    else:
                        numPart8=(numPart//8)+1
                        parte='0'*numPart+'0'*(8-(numPart%8))

                    Utility.database.addFile(ssId,name,md5,lFile,lPart)
                    Utility.database.addPart(md5,ssId,parte)
                    msgRet=msgRet+'{:0>8}'.format(numPart)
                    self.client.sendall(msgRet.encode())

            elif command == "AADR":
                True
                # Todo da Scrivere

            elif command == "LOOK":
                # Todo da testare
                ssId=fields[0]
                name=fields[1]
                # controllo se il sessionId è nel database
                if len(self.database.findPeer(ssId,None,None,2))>0:
                    dati=self.database.findMd5(name.strip())
                    numFileMatch=len(dati)
                    msgp=''
                    for i in range(0,len(dati)):
                        if dati[i][4]!=ssId:
                            msgp=msgp+dati[i][0] #Aggiungo l'iesimo md5
                            msgp=msgp+dati[i][1]+' '*(100-len(dati[i][1])) #Aggiungo il nome del file
                            msgp=msgp+'{:0>10}'.format(int(dati[i][2])) #Aggiungo la lunghezza del file
                            msgp=msgp+'{:0>6}'.format(int(dati[i][3])) #Aggiungo la lunghezza della parte
                        else:
                            numFileMatch=numFileMatch-1

                    msgRet="ALOO"+'{:0>3}'.format(numFileMatch)+msgp

                    self.client.sendall(msgRet.encode())

            elif command == "ALOO":
                True
                # Todo da scrivere

            elif command == "FCHU":
                # Todo da testare
                ssId=fields[0]
                md5=fields[1]
                if len(self.database.findPeer(ssId,None,None,2))>0:
                    dati=self.database.findPartForMd5(md5)
                    num=len(dati)
                    msgp=b''
                    for i in range(0,num):
                        if ssId!=dati[i][0]:
                            datiPeer=self.database.findPeer(dati[i][0],None,None,2)
                            msgp=msgp+datiPeer[0][0].encode()
                            msgp=msgp+datiPeer[0][1].encode()
                            parte=dati[i][1]+'0'*(8-(len(dati[i][1])%8))
                            tmp=Utility.toBytes(dati[i][1],0)
                            msgp=msgp+tmp
                        else:
                            num=num-1

                    msgRet="AFCH".encode()
                    msgRet=msgRet+('{:0>3}'.format(num)).encode()
                    msgRet=msgRet+msgp
                    self.client.sendall(msgRet)

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
               # TOdo da scrivere

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
        self.client.shutdown(1)
        self.client.close()
