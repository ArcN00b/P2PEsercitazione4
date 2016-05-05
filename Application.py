#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename
from Tracker import *
#from Request import *
#from Response import *
#from Utility import *
from Communication import *
import logging

class Window(Frame):
    def __init__(self, root=None):
        Frame.__init__(self, root)
        self.root = root
        self.root.title("Torrent")

        #---- costanti controllo posizione ----
        self.larg_bottoni = 8
        self.imb_x = "3m"
        self.imb_y = "2m"
        self.imb_int_x = "3"
        self.imb_int_y = "1m"
        #---- fine costanti di posizionamento ---

        self.pack(fill=BOTH, expand=1)
        self.createWidgets()
        self.file_aggiunti = []

    def createWidgets(self):

        ## creazione di un menu e sua aggiunta
        menu = Menu(self.root)
        self.root.config(menu=menu)
        ## creazione di un oggetto file
        file = Menu(menu)
        ## associazione azione all'oggetto
        file.add_command(label="Exit", command=self.client_exit)
        ## aggiunta del file al menu
        menu.add_cascade(label="File", menu = file)

        ### quadro login logout
        self.quadro_login = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_login.pack(side=TOP, fill=BOTH, ipadx = self.imb_int_x, ipady = self.imb_int_y)

        ## quadro centrale della ricerca
        self.quadro_centrale_ricerca = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_centrale_ricerca.pack(side=TOP, fill=BOTH, ipadx = self.imb_int_x, ipady = self.imb_int_y)

        ## quadro centrale della ricerca
        self.quadro_centrale_file = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_centrale_file.pack(side=TOP, fill=BOTH, ipadx=self.imb_int_x, ipady=self.imb_int_y)

        ## quadro con file caricati
        self.quadro_console = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_console.pack(side=TOP, fill=BOTH, ipadx = self.imb_int_x, ipady = self.imb_int_y)


        ## ---------------aggiunta dei pulsanti di login e logout------------
        self.btn_login = Button(self.quadro_login, command=self.btn_login_click)
        self.btn_login.configure(text="LOGIN", width=self.larg_bottoni)
        self.btn_login.pack(side=LEFT, padx=self.imb_x, pady=self.imb_y)

        self.btn_logout = Button(self.quadro_login, command=self.btn_logout_click)
        self.btn_logout.configure(text="LOGOUT", width=self.larg_bottoni)
        self.btn_logout.pack(side=LEFT, padx=self.imb_x, pady=self.imb_y)

        self.status = StringVar()
        self.lb_status = Label(self.quadro_login, textvariable=self.status, background="white")
        self.lb_status.pack(side=RIGHT, padx=self.imb_x, pady=self.imb_y)
        self.status.set("STATUS")
        ## ------------------fine parte login logout -----------------------


        ##------------ quadri di divisione della ricerca e scaricamento-------------
        self.quadro_sinistro_ricerca = Frame(self.quadro_centrale_ricerca, background="white", borderwidth=5, relief=RIDGE)
        self.quadro_sinistro_ricerca.pack(side=LEFT, fill=BOTH, expand=1, ipadx = self.imb_int_x, ipady = self.imb_int_y, padx=self.imb_x, pady=self.imb_y)

        self.quadro_destro_ricerca = Frame(self.quadro_centrale_ricerca, background="white", borderwidth=5, relief=RIDGE,)
        self.quadro_destro_ricerca.pack(side=LEFT, fill=BOTH, expand =1, ipadx=self.imb_int_x, ipady=self.imb_int_y, padx=self.imb_x, pady=self.imb_y)

        ## inserimento widget di ricerca e scaricamento
        self.en_ricerca = Entry(self.quadro_sinistro_ricerca)
        self.en_ricerca.pack(side=TOP, fill=BOTH, padx=self.imb_x, pady=self.imb_y)

        self.btn_ricerca = Button(self.quadro_sinistro_ricerca, command=self.btn_ricerca_click)
        self.btn_ricerca.configure(text="RICERCA", width=self.larg_bottoni)
        self.btn_ricerca.pack(side=TOP, padx=self.imb_x, pady=self.imb_y)

        self.lb_progresso = Label(self.quadro_sinistro_ricerca, text='Progresso Scaricamento', background="white")
        self.lb_progresso.pack(side=TOP, padx=self.imb_x, pady=self.imb_y)

        self.prog_scaricamento = Progressbar(self.quadro_sinistro_ricerca, orient='horizontal', mode='indeterminate')
        self.prog_scaricamento.pack(side=TOP, fill=BOTH, padx=self.imb_x, pady=self.imb_y)

        ## inserimento listbox dei risultati della ricerca e bottone scarica dalla selezione
        self.list_risultati = Listbox(self.quadro_destro_ricerca)
        self.list_risultati.pack(side=TOP, fill=BOTH, pady=self.imb_y)

        self.btn_scarica = Button(self.quadro_destro_ricerca, command=self.btn_scarica_click)
        self.btn_scarica.configure(text="SCARICA", width=self.larg_bottoni)
        self.btn_scarica.pack(side=TOP)
        ##--------------- fine parte della ricerca scaricamento -------------------


        ##---------------- parte di aggiunta dei file -----------------------------
        ## quadri di divisione per l'aggiunta
        self.quadro_sinistro_file = Frame(self.quadro_centrale_file, background="white", borderwidth=5, relief=RIDGE)
        self.quadro_sinistro_file.pack(side=LEFT, fill=BOTH, expand=1, ipadx=self.imb_int_x, ipady=self.imb_int_y,padx=self.imb_x, pady=self.imb_y)

        self.quadro_destro_file = Frame(self.quadro_centrale_file, background="white", borderwidth=5, relief=RIDGE)
        self.quadro_destro_file.pack(side=LEFT, fill=BOTH, expand=1, ipadx=self.imb_int_x, ipady=self.imb_int_y,padx=self.imb_x, pady=self.imb_y)

        self.lb_file = Label(self.quadro_sinistro_file, text='Gestione dei File', background="white")
        self.lb_file.pack(side=TOP, padx=self.imb_x, pady=self.imb_y)

        self.btn_aggiungi_file = Button(self.quadro_sinistro_file, command=self.btn_aggiungi_file_click)
        self.btn_aggiungi_file.configure(text="AGGIUNGI", width=self.larg_bottoni)
        self.btn_aggiungi_file.pack(side=TOP, padx=self.imb_x, pady=self.imb_y)

        self.btn_rimuovi_file = Button(self.quadro_sinistro_file, command=self.btn_rimuovi_file_click)
        self.btn_rimuovi_file.configure(text="RIMUOVI", width=self.larg_bottoni)
        self.btn_rimuovi_file.pack(side=TOP, padx=self.imb_x, pady=self.imb_y)

        self.list_file = Listbox(self.quadro_destro_file)
        self.list_file.pack(side=TOP, fill=BOTH, pady=self.imb_y)
        ##---------------- fine parte gestione dei file ---------------------------

        ##---------------- parte di console per le scritture eventuali-------------
        self.text_console = Text(self.quadro_console, state=NORMAL)
        self.text_console.pack(side=TOP, fill=BOTH)
        ##---------------- fine della parte di console ----------------------------

    def client_exit(self):
        exit()

    def print_console(self, mess):
        self.text_console.insert(END,mess+'\n')

    ## evento bottone connessione
    def btn_login_click(self):
        sock_end = Request.create_socket(Utility.IP_TRACKER, Utility.PORT_TRACKER)
        Request.login(sock_end)
        Utility.sessionID = Response.login_ack(sock_end)
        Response.close_socket(sock_end)
        self.status.set("SEI LOGGATO come " + Utility.sessionID)
        self.print_console("LOGIN")

    ## evento bottone disconnessione
    def btn_logout_click(self):
        sock_end = Request.create_socket(Utility.IP_TRACKER, Utility.PORT_TRACKER)
        Request.logout(sock_end)
        success, n_part = Response.logout_ack(sock_end)
        Response.close_socket(sock_end)

        # se si e' sconnesso
        if success:
            self.status.set('DISCONNESSO - PARTI POSSEDUTE: ' + n_part)
            logging.debug('DISCONNESSO - PARTI POSSEDUTE: ' + n_part)
        ## altrimenti rimane connesso
        else:
            self.stutus.set('FALLIMENTO DISCONNESSIONE - PARTI SCARICATE: ' + n_part)
            logging.debug('Disconnessione non consentita hai della parti non scaricate da altri')

    def btn_ricerca_click(self):
        logging.debug("STAI CERCANDO: "+self.en_ricerca.get())
        # Todo da testare in locale prima
        if Utility.SessionID!='':
            # prendo il campo di ricerca
            serch=self.en_ricerca.get().strip(' ')
            # Creo la socket di connessione al tracker
            sock = Request.create_socket(Utility.IP_TRACKER, Utility.PORT_TRACKER)
            # Invio richiesta look
            Request.look(sock,Utility.SessionID,serch)
            # Azzero la ricerca precedente
            Utility.listLastSerch=[]
            # Rimuovo la lista dei file scaricati
            self.list_risultati.delete(0,END)
            # Leggo la ALOO
            # Popolo la lista globale con i risultati dell'ultima ricerca
            self.risultati,Utility.listLastSerch = Response.look_ack(sock)
            Response.close_socket(sock)

            # inserisco tutti gli elementi della lista nella lista nel form
            for value in self.risultati:
                self.list_risultati.insert(END, value)

    def btn_scarica_click(self):
        try:
            # Todo da testare in locale prima
            #indice elemento da scaricare
            index = self.list_risultati.curselection()[0]
            logging.debug("selezionato: " + self.risultati[index])
            #prendo l'elemento da scaricare
            info=Utility.listLastSerch[index]
            '''
            info=info.split('&|&')
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

            '''

            #Classe che esegue il download di un file
            #down=Download(info)
            #down.run()
            self.prog_scaricamento.start(20)
        except Exception as e:
            logging.debug("NULLA SELEZIONATO")

    def btn_aggiungi_file_click(self):
        path_file = askopenfilename(initialdir=Utility.PATHDIR)

        if path_file != '':

            sock_end = Request.create_socket(Utility.IP_TRACKER, Utility.PORT_TRACKER)
            Request.add_file(sock_end, path_file)
            num_parts = Response.add_file_ack(sock_end)
            Response.close(sock_end)

            md5_file = Utility.generateMd5(path_file)
            file_name = path_file.split('/')[-1]
            elem = (md5_file, file_name, num_parts)
            self.file_aggiunti.append(elem)
            self.list_file.insert(END, file_name)

            self.print_console('elemento aggiunto: ' + elem)
            logging.debug('aggiunto: ' + path_file)

    def btn_rimuovi_file_click(self):
        try:
            index = self.list_file.curselection()[0]
            del self.file_aggiunti[index]
            self.list_file.delete(index,index)
            logging.debug("rimosso: " + str(index))
        except Exception as e:
            logging.debug("NULLA SELEZIONATO")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    tracker = False
    
    if tracker:
        '''Utility.database.addPeer('1'*16,Utility.IP_MY[0:54]+'1','{:0>5}'.format(Utility.PORT_MY))
        Utility.database.addPeer('2'*16,Utility.IP_MY[0:54]+'2','{:0>5}'.format(Utility.PORT_MY))
        Utility.database.addPeer('3'*16,Utility.IP_MY[0:54]+'3','{:0>5}'.format(Utility.PORT_MY))
        Utility.database.addPeer('4'*16,Utility.IP_MY[0:54]+'4','{:0>5}'.format(Utility.PORT_MY))
        Utility.database.addFile('1'*16,'pluto','A'*32,'{:0>10}'.format(Utility.LEN_PART*4),Utility.LEN_PART)
        Utility.database.addFile('2'*16,'paperino','B'*32,'{:0>10}'.format(Utility.LEN_PART*9),Utility.LEN_PART)
        Utility.database.addFile('1'*16,'pippo','C'*32,'{:0>10}'.format(Utility.LEN_PART*8),Utility.LEN_PART)
        Utility.database.addPart('A'*32,'1'*16,'11110000')
        Utility.database.addPart('B'*32,'2'*16,'1111111110000000')
        Utility.database.addPart('C'*32,'1'*16,'11111111')
        Utility.database.addPart('C'*32,'2'*16,'00011110')'''
        tcpServer = Tracker(Utility.database,Utility.IPv4_TRACKER+'|'+Utility.IPv6_TRACKER,Utility.PORT_TRACKER)
        tcpServer.run()



    
    else:
        root = Tk()
        root.geometry("800x600")
        app = Window(root=root)

        #Utility.SessionID='4'*16

        root.mainloop()
