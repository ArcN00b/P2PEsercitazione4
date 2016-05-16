
from Communication import *
from Response import *
from Request import *
from Utility import *

class Scaricamento(threading.Thread):

    def __init__(self,progress_bar, var_progress, dati):
        threading.Thread.__init__(self)
        self.dati=dati
        self.progress_bar = progress_bar
        self.var_progress = var_progress

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

        # scaricamento
        self.var_progress.set('Sto scaricando..')

        parte='0'*numPart
        # aggiungo il file al database
        Utility.database.addFile(Utility.sessionID, name, md5, lFile, lPart)
        # aggiungo al database la stringa
        Utility.database.addPart(md5, Utility.sessionID, parte)
        partiScaricate=0
        Utility.blocco.acquire()
        Utility.lock = False
        Utility.blocco.release()
        semaphore = threading.BoundedSemaphore(Utility.NUMDOWNPARALLELI)
        while partiScaricate!=numPart and not Utility.lock:
            valid_request=True
            try:
                sock = Request.create_socket(Utility.IP_TRACKER,Utility.PORT_TRACKER)
                # Invio messaggio FCHU
                Request.fchu(sock, Utility.sessionID, md5)
                # gestisco la risposta dei AFCH, mi ritorna la lista dei peer che hanno fatto match
                listaPeer=Response.fchu_ack(sock,numPart8,numPart)
                # Chiudo la socket,non serve tenerla aperta
                Response.close_socket(sock)
                #Prendo dal database la situazione delle parti del mio file
                myPart=Utility.database.findPartForMd5AndSessionId(Utility.sessionID, md5)
                myPart=myPart[0][0]
            except Exception as e:
                print("Errore Aggiornamento parti, reinvio richiesta"+str(e))
                valid_request=False

            # Da qui in avanti vi e tutta la logica di funzionamento del scaricamento
            #Controllo se ho ricevuto una richiesta corretta e non vi sono stati errori nel'invio e ricezione FCHU
            if valid_request==True:
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

                t = Download_Manager(self.progress_bar, self.var_progress, numPart, semaphore, listaPart, md5, name)
                t.start()
                # attendo un tempo per rifare la fchu
                # questo è un cilco di attesa attivo

                time.sleep(Utility.ATTESA)

                #conto il numero di parti scaricate, interrogando il database
                myPart=Utility.database.findPartForMd5AndSessionId(Utility.sessionID, md5)
                partiScaricate=(myPart[0][0]).count('1')


