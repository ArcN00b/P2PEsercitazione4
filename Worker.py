import threading
import socket
import struct
import os
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
    def __init__(self, client, database, lock):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.client = client
        self.database = database
        self.lock = lock

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
                        #parte='1'*numPart
                    else:
                        numPart8=(numPart//8)+1
                        #parte='0'*numPart+'0'*(8-(numPart%8))

                    parte='1'*numPart
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
                            datiPeer=self.database.findPeer(dati[i][0])
                            msgp=msgp+datiPeer[0][0].encode()
                            msgp=msgp+datiPeer[0][1].encode()
                            parte=dati[i][1]+'0'*(8-(len(dati[i][1])%8))
                            tmp=Utility.toBytes(parte,0)
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
                # Todo da testare
                # Imposto la lunghezza dei chunk e ottengo il nome del file a cui corrisponde l'md5
                chunklen = 512
                md5 = fields[0]
                partNum = fields[1]
                obj = Utility.database.findFile(Utility.sessionId, md5, None, 1)

                # Ora preparo il file per la lettura
                if len(obj) > 0:

                    # Controllo se il file è disponibile completamente o meno
                    if os.path.isfile(Utility.PATHDIR + str(obj[0][0]).strip()) > 0:
                        filename = Utility.PATHDIR + str(obj[0][0]).strip()
                        owned = True    #Se owned = true allora il file è disponibile completamente
                    else:
                        filename = Utility.PATHTEMP + str(obj[0][0]).strip() + partNum
                        owned = False

                    # Calcolo in quanti chunk devo dividere la parte
                    lenPart = int(obj([0][1]))
                    num_chunk = lenPart // chunklen
                    if lenPart % chunklen != 0:
                        num_chunk = num_chunk + 1
                    # pad con 0 davanti
                    num_chunk = str(num_chunk).zfill(6)

                    # costruzione risposta come ARET0000XX
                    msgRet = ('ARET' + num_chunk).encode()
                    self.client.sendall(msgRet)

                    # Apro il file in lettura e leggo il primo chunk della parte
                    f = open(filename, 'rb')

                    # Se il file è completo devo portare avanti l'indice di lettura
                    if owned:
                        f.seek(partNum * lenPart)

                    # Leggo la parte intera
                    r = f.read(lenPart)

                    # Finchè non completo la parte o il file non termina
                    while len(r) > 0:
                        
                        # Aggiungo la lunghezza del chunk e il chunk
                        mess = str(len(r)).zfill(5).encode()
                        if len(r) > chunklen:
                            mess += r[:chunklen]
                            r = r[chunklen:]
                        else:
                            mess += r
                            r = ''

                        # Invio effettivamente il messaggio
                        self.client.sendall(mess)

                    # Chiudo il file
                    f.close()

            elif command == "AREP":
                True
                # Todo da scrivere

            elif command == "RPAD":
                # Todo da testare

                # Assegno il contenuto di fields per comodità
                ssId = fields[0]
                md5 = fields[1]
                partNum = int(fields[2])

                # Ottengo la parte dal database modificando il valore in posizione partNum
                part = Utility.database.findPartForMd5AndSessionId(ssId, md5)
                tmp = list(part[0][0])
                tmp = tmp[partNum] = "1"
                part = "".join(tmp)

                # Conto quante parti ha attualmente il peer e aggiorno il database
                partOwn = part.coun("1")
                Utility.database.updatePart(ssId, md5, part)

                # Preparo e invio il messaggio di ritorno
                msgRet = "APAD" + str(partOwn).zfill(8)
                self.client.sendall(msgRet.encode())

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
                        listSsId = Utility.findFile(ssId, file[0][0], None, 5)
                            
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

                        # Rimuovo i file e le parti del file dal database
                        Utility.database.removeAllFileForSessionId(ssId)

                        # Preparo ora il messaggio di ritorno ALOG
                        msgRet = "ALOG" + str(partOwn).zfill(10)

                    # In caso contrario invio le parti effettivamente scaricate dagli altri peer
                    else:
                        msgRet = "NLOG" + str(partDown).zfill(10)

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
