import threading
import socket
import struct
from Parser import *
from ManageDB import *
from Utility import *


# Costruttore che inizializza gli attributi del Worker
class Worker(threading.Thread):

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
            buffer = data
            command, fields = Parser.parse(buffer)
            # risposta da inviare in modo sincronizzato
            self.lock.acquire()
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
                        parte='0'*numPart
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
                msgRet="ALOO"
                ssId=fields[0]
                name=fields[1]
                # controllo se il sessionId è nel database
                if len(self.database.findPeer(ssId,None,None,2))>0:
                    dati=self.database.findMd5(name.strip())
                    msgRet=msgRet+'{:0>3}'.format(len(dati))
                    for i in range(0,len(dati)):
                        msgRet=msgRet+dati[i][0] #Aggiungo l'iesimo md5
                        msgRet=msgRet+dati[i][1]+' '*(100-len(dati[i][1])) #Aggiungo il nome del file
                        msgRet=msgRet+'{:0>10}'.format(int(dati[i][2])) #Aggiungo la lunghezza del file
                        msgRet=msgRet+'{:0>6}'.format(int(dati[i][3])) #Aggiungo la lunghezza della parte

                    self.client.sendall(msgRet.encode())

            elif command == "ALOO":
                True
                # Todo da scrivere

            elif command == "FCHU":
                # Todo da testare
                msgRet="AFCH".encode()
                ssId=fields[0]
                md5=fields[1]
                if len(self.database.findPeer(ssId,None,None,2))>0:
                    dati=self.database.findPartForMd5(md5)
                    num=len(dati)
                    msgRet=msgRet+('{:0>3}'.format(num)).encode()
                    for i in range(0,num):
                        datiPeer=self.database.findPeer(dati[i][0])
                        msgRet=msgRet+datiPeer[0][0].encode()
                        msgRet=msgRet+datiPeer[0][1].encode()
                        tmp=Utility.toBytes(dati[i][1],0)
                        msgRet=msgRet+tmp

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
                # Todo da scrivere

            elif command == "LOGO":
                # Todo da testare

                # Ricavo la lista dei file inerenti al sessionID di chi richiede il logout
                ssId = fields[0]
                listFile = Utility.database.listFileForSessionId(ssId) #MD5,NAME,LENFILE,LENPART

                # Se il peer non ha aggiunto file allora posso effettuare logout
                if(len(listFile) == 0):
                    msgRet = "ALOG" + '0'.zfill(10)
                else:
                    
                    # Per ciascun file devo controllare che ci siano altri peer che l'hanno scaricato (almeno in parte)
                    canLogout = True
                    partDown = 0
                    for file in listFile:
                        listSsId = Utility.findFile(ssId, file[0][0], None, 4)
                            
                        # Se nessun altro peer ha lo stesso file non posso effettuare il logout
                        if len(listSsId) == 0:
                            canLogout = False

                        # Per ciascun peer devo ottenere l'elenco delle parti che possiedono
                        else:
                            listParts = []
                            for peer in listSsId:
                                tmp = Utility.database.findPartForMd5AndSessionId(peer, file[0][0])
                                listParts.append(tmp)
                                        
                            # Ricavo ora il numero delle parti del file per effettuare il controllo successivo
                            nParts = file[0][2]//file[0][3]     #file[0][2] = LENFILE
                            if file[0][2] % file[0][3] != 0:    #file[0][3] = LENPART
                                nParts += 1

                            # Conto quante parti sono state scaricate almeno una volta (caso NLOG) mi è comodo farlo qui
                            partDown += Utility.partCounter(listParts, nParts)

                            # Ora devo controllare che tra tutti i peer, il file possa essere disponibile completamente
                            if not Utility.partChecker(listParts, nParts):
                                canLogout = False
                    
                    # Se si può effettuare il logout allora preparo il messaggio con le parti dei file in possesso
                    if canLogout:
                        partOwn = 0
                        for file in listFile:
                            tmp = Utility.database.findPartForMd5AndSessionId(peer, file[0][0])
                            partOwn += tmp.count("1")

                        # Preparo ora il messaggio di ritorno ALOG
                        msgRet = "ALOG" + partOwn.zfill(10)

                        #TODO rimuovere dalla tabella PARTS tutte le occorrenze dove SessionID = ssId
                    else:
                        msgRet = "NLOG" + partDown.zfill(10)

                # Invio il messaggio di ritorno
                self.client.sendall(msgRet.encode())

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
