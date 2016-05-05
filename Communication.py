from builtins import print

from Utility import *
from Request import *
from Response import *
import time
import random
import threading
import socket

# questa classe non e' un thread, ma ne genera per inviare i dati
class SenderAll:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, messaggio, listaNear):
        # definizione thread del client
        self.messaggio = messaggio
        self.listaNear = listaNear

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def run(self):
        for i in range(0, len(self.listaNear)):
            messaggio = self.messaggio
            ip = self.listaNear[i][0]
            porta = self.listaNear[i][1]

            s = Sender(messaggio, ip, porta)
            s.run()

class Sender:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, messaggio, ip, port):
        # definizione thread del client
        self.messaggio = messaggio
        self.ip = ip
        self.port = port

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def run(self):
        try:
            r = random.randrange(0, 100)
            ipv4, ipv6 = Utility.getIp(self.ip)
            if r < 50:
                a = ipv4
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                a = ipv6
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

            sock.connect((a, int(self.port)))
            print('inviato a ' + a +':'+str(self.port) + ' : ' + self.messaggio)
            sock.sendall(self.messaggio.encode())
            sock.close()
        except Exception as e:
            print("Errore Peer down " + self.ip + " " + str(self.port))

class SenderAndWait:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, messaggio, ip, port):
        # definizione thread del client
        self.messaggio = messaggio
        self.ip = ip
        self.port = port
        self.sock = ''

    # Funzione che lancia il worker e controlla la chiusura improvvisa
    def run(self):
        try:
            r = random.randrange(0, 100)
            ipv4, ipv6 = Utility.getIp(self.ip)
            if r < 50:
                a = ipv4
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                a = ipv6
                self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

            self.sock.connect((a, int(self.port)))
            print('inviato a ' + a +':'+str(self.port) + ' : ' + self.messaggio)
            self.sock.send(self.messaggio.encode())
        except Exception as e:
            print("Errore Peer down " + self.ip + " " + str(self.port))

    def getSocket(self):
        return self.sock

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

## classe che dato un socket riceve tutte le informazioni
## secondo una lunghezza data di ingresso
class Receiver:

    def __init__(self, sock):
        self.sock = sock

##  metodo che ritorna le informazioni ricevute sulla lunghezza data
    def receive(self, len):
        return self.sock.recv(len)


class Downloader(threading.Thread):
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, ipp2p, pp2p, md5, name, part):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.ipp2p = ipp2p
        self.pp2p = pp2p
        self.md5 = md5
        self.name = name

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

            # Avviso il tracker di aver completato il download della parte del file
            msgPart = 'RPAD' + Utility.sessionId + md5 + '{:0>8}'.format(int(part))
            sockTracker = Request(Utility.IP_TRACKER, int(Utility.PORT_TRACKER))
            sentTracker = sockTracker.send(msgPart.encode())
            # TODO pensare a come agire in caso di RPAD non inviata correttamente
            if sentTracker is None or sentTracker < len(msgPart):
                print('RPAD non riuscita in download')
                sockTracker.close()
                return

            # TODO pensare a incongruenze aggiungendo parte al database se non viene avvisato il tracker
            # TODO inserire il codice di merge in un try catch?
            # Aggiungo la parte alla lista delle parti nel database
            strPart = Utility.database.findPartForMd5AndSessionId(Utility.sessionId, md5)
            strPart[part-1] = '1';
            Utility.database.updatePart(Utility.sessionId, md5, strPart)

            # Verifico se sono stati scaricati tutti i file e in tal caso eseguo il merge
            # Verifico se non è presente nessun 0 nella lista delle parti
            if not('0' in ((Utility.database.findPartForMd5(md5))[0][1])):
                # Ho tutte le parti ed eseguo il merge di tutte le parti di file

                # Prelevo lenFile e lenPart rispettivamente in row[0][0] e in row[0][1]
                row = Utility.database.findFile(0,md5,0,4)
                lenFile = int(row[0][0])
                lenPart = int(row[0][1])

                #nPart = len((Utility.database.findPartForMd5(md5))[0][1])

                # Calcolo il numero di parti del file: se la divisione non è esatta aggiungo una parte
                nPart = int( lenFile / lenPart )
                if( lenFile % lenPart > 0 ):
                    nPart = nPart + 1

                # Cancello il contenuto del file
                fCompleto = open(Utility.PATHDIR + name.rstrip(' '), "wb")
                fCompleto.close()

                # Raggruppo le parti in un unico file
                for i in range (1,nPart+1):

                    # Aggiungo la parte i-esima in coda al file
                    fParte = open(Utility.PATHTEMP + name.rstrip(' ') + str(i), "rb")
                    buffer = fParte.read()

                    # Scrivo all'interno del file e chiudo il file completo
                    with open(Utility.PATHDIR + name.rstrip(' '), "ab") as myfile:
                        myfile.write(buffer)

                    # Chiusura del file della parte
                    fParte.close()

                # Avviso il tracker di avere il file completo
                msgFile = 'ADDR' + Utility.sessionId + '{:0>10}'.format(lenFile) +  + '{:0>6}'.format(lenPart)
                sentTracker = sockTracker.send(msgFile.encode())
                # TODO pensare a come agire in caso di ADDR non inviata correttamente
                if sentTracker is None or sentTracker < len(msgFile):
                    print('ADDR non riuscita in download')
                    sockTracker.close()
                    return



            f.close()
            print("Download completato")

        sockTracker.shutdown()
        sockTracker.close()
        sock.shutdown()
        sock.close()



class AFinder:
    # Costruttore che inizializza gli attributi del Worker
    def __init__(self, sock):
        self.sock = sock

    def run(self):
        # ricevo i primi 10 Byte che sono "AFIN" + n_chunk
        recv_mess = self.sock.recv(7).decode()
        while len(recv_mess) < 7:
            recv_mess += self.sock.recv(7 - len(recv_mess)).decode()

        if recv_mess[:4] == "AFIN":
            numMd5 = int(recv_mess[4:7])

            # Leggo MD5 NAME NUM PEER dal socket
            for i in range(0, numMd5):
                tmp = self.sock.recv(135)  # leggo la lunghezza del chunk
                while len(tmp) < 135:
                    tmp += self.sock.recv(135 - len(tmp))
                    if len(tmp) == 0:
                        raise Exception("Socket close")

                # Eseguo controlli di coerenza su ciò che viene ricavato dal socket
                try:
                    int(tmp[-3:].decode())
                except Exception as e:
                    raise Exception("number format exception")


                # Salvo cie che e stato ricavato in ListFindFile
                Utility.listFindFile.append([tmp[:32].decode(), tmp[32:-3].decode(), int(tmp[-3:].decode())])

                # Ottengo la lista dei peer che hanno lo stesso md5
                numPeer = int(tmp[-3:].decode())
                for j in range(0, numPeer):

                    # Leggo i dati di ogni peer dal socket
                    buffer = self.sock.recv(60)  # Leggo il contenuto del chunk
                    while len(buffer) < 60:
                        tmp = self.sock.recv(60 - len(buffer))
                        buffer += tmp
                        if len(tmp) == 0:
                            raise Exception("Socket close")

                    # Salvo ciò che e stato ricavato in Peer List
                    Utility.listFindPeer.append([buffer[:55].decode(), int(buffer[55:].decode())])

class Download:

    def __init__(self,dati):
        self.dati=dati

    def run(self):
        info=self.dati.split('&|&')
        md5=info[0]
        name=info[1]
        lFile=int(info[2])
        lPart=int(info[3])
        #Calcolo il numero delle parti
        if lFile%lPart==0:
            numPart=lFile//lPart
        else:
            numPart=(lFile//lPart)+1

        if numPart%8==0:
            numPart8=numPart//8
            #parte='0'*numPart
        else:
            numPart8=(numPart//8)+1
            #parte='0'*numPart+'0'*(8-(numPart%8))

        parte='0'*numPart
        # aggiungo il file al database
        Utility.database.addFile(Utility.SessionID,name,md5,lFile,lPart)
        # aggiungo al database la stringa
        Utility.database.addPart(md5,Utility.SessionID,parte)
        partiScaricate=0
        while partiScaricate!=numPart:
            sock = Request.create_socket(Utility.IP_TRACKER,Utility.PORT_TRACKER)
            # Invio messaggio FCHU
            Request.fchu(sock,Utility.SessionID,md5)
            # gestisco la risposta dei AFCH, mi ritorna la lista dei peer che hanno fatto match
            listaPeer=Response.fchu_ack(sock,numPart8,numPart)
            # Chiudo la socket,non serve tenerla aperta
            Response.close_socket(sock)
            #Prendo dal database la situazione delle parti del mio file
            myPart=Utility.database.findPartForMd5AndSessionId(Utility.SessionID,md5)
            myPart=myPart[0][0]
            # Ora seleziono ed elaboro la risposta
            listaPart=[] # E lista dove per ogni parte memorizzo i peer che ce l'hanno, lista di liste
            for i in range(0,numPart):
                if myPart[i]=='0':
                    lista=[]
                    lista.append(str(i))
                    for j in range(0,len(listaPeer)):
                        part=listaPeer[j][2]
                        if part[i]=='1':
                            lista.append(listaPeer[j][0]+'-'+listaPeer[j][1]) # salvo Ip e port separtati da -
                    listaPart.append(lista)
            # ordino la lista mettendo all'inizio le parti possedute da meno peer
            listaPart.sort(key=len)
            # Prendo i primi 10 o meno
            numDown=0
            numDownParalleli=10
            for i in  range(0,len(listaPart)):
                # Prendo la parte interessata ed eseguo il download
                nPeer=len(listaPart[i])-1
                down=random.randint(0,nPeer-1)
                datiDown=listaPart[i][down+1]
                datiDown=datiDown.split('-')
                parte=int(listaPart[i][0])
                numDown=numDown+1
                #Chiamata al download
                Request.download(datiDown[0],datiDown[1],md5,name,parte)
                #Controllo se ho gia fatto almeno 10 download
                if numDown>=numDownParalleli:
                    break

            # attendo un tempo per rifare la fchu
            a=time.strftime("%M:%S")
            a=a.split(':')
            a=int(a[0])*60+int(a[1])
            attesa=60 # Secondi di attesa
            diff=0
            while diff<attesa:
                b=time.strftime("%M:%S")
                b=b.split(':')
                b=int(b[0])*60+int(b[1])
                diff=b-a

            #conto il numero di parti scaricate, interrogando il database
            myPart=Utility.database.findPartForMd5AndSessionId(Utility.SessionID,md5)
            partiScaricate=myPart.count('1')