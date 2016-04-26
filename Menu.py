from Communication import *
import os
import sys
import select

class Menu:

    @staticmethod
    def function(sel):

        if Utility.stato=='start':
            sel=sel[0]
            if sel=='1':
                if not Utility.superNodo:
                    pktID=Utility.generateId(16)
                    ip=Utility.MY_IPV4+'|'+Utility.MY_IPV6
                    port='{:0>5}'.format(Utility.PORT)
                    ttl='{:0>2}'.format(4)
                    msg="SUPE"+pktID+ip+port+ttl
                    Utility.database.addPkt(pktID)
                    Utility.numFindSNode = 0
                    Utility.listFindSNode = []

                    # Invio la richiesta a tutti i Peer, cosi' reinoltrano la richiesta
                    listaP=Utility.database.listPeer(2)
                    if len(listaP)>0:
                        tP = Utility.SenderAll(msg, listaP)
                        tP.run()

                    # Invio la richiesta a tutti i SuperNodi
                    listaS=Utility.database.listSuperNode()
                    if len(listaS)>0:
                        tS = SenderAll(msg, listaS)
                        tS.run()

                    Utility.stato='conSup'
                    print("Scegli il supernodo a cui vuoi collegarti, 0 per uscire")

                else:
                    print("Errore: sei un supernodo, non puoi collegarti ad altri supernodi")
                    Menu.printMenu()

            #Aggiunta di un file
            elif sel=='2':
                #Controllo se ho un sessionId, quindi se sono loggato a un supernodo
                if Utility.sessionId!='':
                    #prendo la lista dei file
                    lst = os.listdir(Utility.PATHDIR)

                    print("Numero File     Nome File")
                    for i in range(0,len(lst)):
                        print(str(i+1)+"    "+lst[i])
                    Utility.stato='addFile'
                    print("Inserisci il numero del file da aggiungere, 0 per uscire ")
                else:
                    print("Effettuare Login")
                    Menu.printMenu()

            # Rimozione di un file
            elif sel=='3':
                #Controllo se ho un sessionId, quindi se sono loggato a un supernodo
                if Utility.sessionId!='':
                    # Ottengo la lista dei file dal database
                    lst = Utility.database.listFileForSessionId(Utility.sessionId)

                    # Visualizzo la lista dei file
                    if len(lst) > 0:
                        Utility.stato='delFile'
                        print("Scelta  MD5                                        Nome")
                        for i in range(0,len(lst)):
                            print(str(i+1) + "   " + lst[i][0] + " " + lst[i][1])

                    else:
                        print("Non ci sono file nel database")
                        Menu.printMenu()

                else:
                    print("Effettuare Login")
                    Menu.printMenu()

            #Ricerca
            elif sel=='4':
                #TODO se il tuo e presente non devi comparire nella lista dei risultati
                #TODO non scirtta xke non era chiara e da ultimare, basta importarla e creare un nuovo stato per l'input
                if Utility.sessionId != '':
                    print("IN ALLESTIMENTO")
                    Utility.stato='find'
                    print("Inserisci il file da scaricare, 0 per uscire")
                    file='Mona_Lisa.jpg'
                    md5=Utility.generateMd5(Utility.PATHDIR+'pippo/'+file)
                    name=file+' '*(100-len(file))
                    ip=Utility.MY_IPV4[0:-1]+'2|'+Utility.MY_IPV6[0:-1]+'2'
                    port='{:0>5}'.format(80)
                    t=Downloader(ip,port,md5,name)
                    t.run()
                else:
                    print("Effettuare Login")
                    Menu.printMenu()

            #logout, fuziona solo se sei un peer loggato
            elif sel=='5':
                #Controllo se ho un sessionId, quindi se sono loggato a un supernodo
                if Utility.sessionId!='':
                    if not Utility.superNodo:
                        #Resetto le variabili globali anche se effettivamente non ricevo una ALGO di risposta
                        Utility.sessionId=''
                        Utility.ipSuperNodo=''
                        Utility.portSuperNodo=''

                        # genero e invio il messaggio di logout al supernodo
                        msg='LOGO'+Utility.sessionId
                        t=Sender(msg,Utility.ipSuperNodo,int(Utility.portSuperNodo))
                        t.start()
                    else:
                        print("Sei un supernodo")
                else:
                    print("Effettuare Login")
                Menu.printMenu()

            #Visualizza file supernodo o peer
            elif sel=='6':
                #Controllo se sono supernodo, se lo sono stampo anche la colonna sessionId
                if Utility.superNodo:
                    # Ottengo la lista dei file dal database
                    lst = Utility.database.listFile()

                    # Visualizzo la lista dei file
                    if len(lst) > 0:
                        print("SessionID        MD5                                        Nome")
                        for i in range(0,len(lst)):
                            print(lst[i][0] + " " + lst[i][2]+" "+lst[i][1])

                    else:
                        print("Non ci sono file nel database")
                else:
                    # Ottengo la lista dei file dal database
                    lst = Utility.database.listFileForSessionId(Utility.sessionId)
                    # Visualizzo la lista dei file
                    if len(lst) > 0:
                        print("MD5                                        Nome")
                        for i in range(0,len(lst)):
                            print(lst[i][0] + " " + lst[i][1])
                    else:
                        print("Non ci sono file nel database")
                Menu.printMenu()

            #Aggiorna supernodi
            elif sel=='8':
                if Utility.superNodo:
                    pktID=Utility.generateId(16)
                    ip=Utility.MY_IPV4+'|'+Utility.MY_IPV6
                    port='{:0>5}'.format(Utility.PORT)
                    ttl='{:0>2}'.format(4)
                    msg="SUPE"+pktID+ip+port+ttl

                    # Aggiungo il pacchetto della richiesta SUPE
                    Utility.database.addPkt(pktID)

                    # Invio la richiesta a tutti i Peer, cosi' inoltrano la richiesta
                    listaP=Utility.database.listPeer(2)
                    if len(listaP)>0:
                        tP = SenderAll(msg, listaP)
                        tP.run()

                    # Invio la richiesta a tutti i SuperNodi
                    listaS=Utility.database.listSuperNode()
                    if len(listaS)>0:
                        tS = SenderAll(msg, listaS)
                        tS.run()
                Menu.printMenu()

            #Visualizza Peer
            elif sel=='9':
                if Utility.superNodo:
                    lst=Utility.database.listPeer(1)
                    # Visualizzo la lista dei peer collegati
                    if len(lst) > 0:
                        print("SessionID        IP                                                      Porta")
                        for i in range(0,len(lst)):
                            print(lst[i][0] + " " + lst[i][2]+" "+lst[i][1])
                    else:
                        print("Non ci peer collegati")
                Menu.printMenu()

            #Aggiungi supernodo al database
            elif sel=='7':
                Utility.stato='addSupNode'
                #todo leggi tutto insieme nel formato ip4 ip6 porta
                print("Inserisci dati del supernodo, nel formato ip4 ip6 porta")
            else:
                print("Commando Errato, attesa nuovo comando ")

        elif Utility.stato=='conSup':
            #ho ricevuto in input il supernodo a cui connettermi
            # Scelgo il supernodo a cui voglio collegarmi
            i = int(sel[0])
            if i not in range(1, Utility.numFindSNode +1):
                print("Scegli il supernodo a cui vuoi collegarti")
            elif i==0:
                Utility.stato='start'
                Menu.printMenu()
            else:
                #if Utility.numFindSNode == 0:
                #   print ("Nessun supernodo trovato")
                #TOdO controlla bene, non è cosi banale
                # Effettuo la LOGO dal precedente supernodo
                if Utility.sessionId!='':
                    #Resetto le variabili globali anche se effettivamente non ricevo una ALGO di risposta
                    Utility.sessionId=''
                    Utility.ipSuperNodo=''
                    Utility.portSuperNodo=''

                    # Invio la LOGO al supernodo a cui sono collegato
                    msg='LOGO'+Utility.sessionId
                    try:
                        tL=Sender(msg,Utility.ipSuperNodo,int(Utility.portSuperNodo))
                        tL.start()
                    except Exception as e:
                        print(e)

                # Supernodo scelto, effettuo la LOGI
                i = i - 1;
                ipDest = Utility.listFindSNode[i][1]
                portDest = Utility.listFindSNode[i][2]
                ip=Utility.MY_IPV4+'|'+Utility.MY_IPV6
                port='{:0>5}'.format(Utility.PORT)
                msg="LOGI"+ip+port
                Utility.ipSuperNodo = ipDest
                Utility.portSuperNodo = portDest

                try:
                    t1 = Sender(msg, ipDest, portDest)
                    t1.start()
                except Exception as e:
                    print(e)

                Utility.stato='start'
                Menu.printMenu()

        elif Utility.stato=='delFile':
            sel=sel[0]
            # Chiedo quale file rimuovere
            lst = Utility.database.listFileForSessionId(Utility.sessionId)
            i = int(sel)
            if i not in range(1, len(lst)+1):
                print("Scegli il file da cancellare ")
            elif i==0:
                Utility.stato='start'
                Menu.printMenu()
            else:
                Utility.stato='start'
                fileScelto=i-1
                # Elimino il file
                Utility.database.removeFile(Utility.sessionId,lst[fileScelto][0])
                #Controllo se non sono supernodo, se si devo comunicare che ho cancellato il file
                if not Utility.superNodo:
                    #genero il messaggio da mandare al supernodo con il file eliminato
                    md5=lst[fileScelto][0]
                    name=lst[fileScelto][1]
                    msg='DEFF'+Utility.sessionId+md5+name
                    t=Sender(msg,Utility.ipSuperNodo,int(Utility.portSuperNodo))
                    t.start()
                print("Operazione completata")
                Utility.stato='start'
                Menu.printMenu()

        elif Utility.stato=='addFile':
            sel=sel[0]
            i = int(sel)
            lst=os.listdir(Utility.PATHDIR)
            if i not in range(1, len(lst)+1):
                print("Inserisci il numero del file da aggiungere ")
            elif i==0:
                Utility.stato='start'
                Menu.printMenu()
            else:
                fileScelto=i-1
                #genero md5
                Utility.stato='start'
                md5=Utility.generateMd5(Utility.PATHDIR+lst[fileScelto])
                name=lst[fileScelto].ljust(100,' ')
                #Aggiungo il file al mio database
                Utility.database.addFile(Utility.sessionId,name,md5)
                #Controllo se devo inviare il messaggio di aggiunta al mio supernodo, se sono peer
                if not Utility.superNodo:
                    #Creo il messaggio da inviare al supernodo
                    msg='ADFF'+Utility.sessionId+md5+name
                    t=Sender(msg,Utility.ipSuperNodo,int(Utility.portSuperNodo))
                    t.start()
                Utility.stato='start'
                Menu.printMenu()

        elif Utility.stato=='addSupNode':
            sel=sel.split(' ')
            t=sel[0].split('.')
            ipv4=""
            ipv4=ipv4+'{:0>3}'.format(t[0])+'.'
            ipv4=ipv4+'{:0>3}'.format(t[1])+'.'
            ipv4=ipv4+'{:0>3}'.format(t[2])+'.'
            ipv4=ipv4+'{:0>3}'.format(t[3])+'|'
            t=sel[1].split(':')
            ipv6=""
            ipv6=ipv6+'{:0>4}'.format(t[0])+':'
            ipv6=ipv6+'{:0>4}'.format(t[1])+':'
            ipv6=ipv6+'{:0>4}'.format(t[2])+':'
            ipv6=ipv6+'{:0>4}'.format(t[3])+':'
            ipv6=ipv6+'{:0>4}'.format(t[4])+':'
            ipv6=ipv6+'{:0>4}'.format(t[5])+':'
            ipv6=ipv6+'{:0>4}'.format(t[6])+':'
            ipv6=ipv6+'{:0>4}'.format(t[7])
            port='{:0>5}'.format(int(sel[2]))
            ip=ipv4+ipv6
            Utility.database.addSuperNode(ip,port)
            #Ristampo il menu
            Utility.stato='start'
            Menu.printMenu()

        elif Utility.stato=='find':
            sel=sel[0]
            i=int(sel)
            if i not in range(1, len(Utility.listFindFile)+1):
               print("Inserisci il file da scaricare, 0 per uscire")
            elif i==0:
                Utility.stato='start'
                Menu.printMenu()
            else:
                fileScelto=i-1
                #TODO Avviare il download dal file scelto



    @staticmethod
    def printMenu():
        print("1. Connetti a Supernodo")
        print("2. Aggiungi File")
        print("3. Rimuovi File")
        print("4. Ricerca File")
        print("5. Logout")
        print("6. Visualizza File")
        print("7. Aggiungi Supernodo")
        if Utility.superNodo:
            print("8. Aggiorna Supernodi")
            print("9. Visualizza Peer")
        print(" ")
        print("Inserisci il numero del comando da eseguire ")