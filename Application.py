#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename
from Tracker import *
from Merge_Divide import Divide
from Scaricamento import *
import logging
import shutil


class Window(Frame):
    def __init__(self, root=None):
        Frame.__init__(self, root)
        self.root = root
        self.root.title("Torrent")

        # ---- costanti controllo posizione ----
        self.larg_bottoni = 8
        self.imb_x = "3m"
        self.imb_y = "2m"
        self.imb_int_x = "3"
        self.imb_int_y = "1m"
        # ---- fine costanti di posizionamento ---

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
        menu.add_cascade(label="File", menu=file)

        ### quadro login logout
        self.quadro_login = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_login.pack(side=TOP, fill=BOTH, ipadx=self.imb_int_x, ipady=self.imb_int_y)

        ## quadro centrale della ricerca
        self.quadro_centrale_ricerca = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_centrale_ricerca.pack(side=TOP, fill=BOTH, ipadx=self.imb_int_x, ipady=self.imb_int_y)

        ## quadro centrale della ricerca
        self.quadro_centrale_file = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_centrale_file.pack(side=TOP, fill=BOTH, ipadx=self.imb_int_x, ipady=self.imb_int_y)

        ## quadro con file caricati
        self.quadro_console = Frame(self, background="white", borderwidth=5, relief=RIDGE, height=10)
        self.quadro_console.pack(side=TOP, fill=BOTH, ipadx=self.imb_int_x, ipady=self.imb_int_y)

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

        self.prog_scaricamento = Progressbar(self.quadro_sinistro_ricerca, orient='horizontal', mode='determinate')
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

            ## si rimuove la cartella temporanea, i file
            ## e le parti dal database associate
            Utility.database.removeAllFileForSessionId(Utility.sessionID)
            try:
                shutil.rmtree(Utility.PATHTEMP)
            except Exception as e:
                logging.debug('cartella non esistente')

        ## altrimenti rimane connesso
        else:
            self.stutus.set('FALLIMENTO DISCONNESSIONE - PARTI SCARICATE: ' + n_part)
            logging.debug('Disconnessione non consentita hai della parti non scaricate da altri')

    def btn_ricerca_click(self):
        logging.debug("STAI CERCANDO: "+self.en_ricerca.get())
        # Todo da testare in locale prima
        if Utility.sessionID!= '':
            # prendo il campo di ricerca
            serch=self.en_ricerca.get().strip(' ')
            # Creo la socket di connessione al tracker
            sock = Request.create_socket(Utility.IP_TRACKER, Utility.PORT_TRACKER)
            # Invio richiesta look
            Request.look(sock, Utility.sessionID, serch)
            # Azzero la ricerca precedente
            Utility.listLastSerch=[]
            # Rimuovo la lista dei file scaricati
            self.list_risultati.delete(0,END)
            # Leggo la ALOO
            # Popolo la lista globale con i risultati dell'ultima ricerca
            self.risultati,Utility.listLastSerch = Response.look_ack(sock)
            Response.close_socket(sock)

            # inserisco tutti gli elementi della lista nella lista nel form
            for value in Utility.listLastSearch:
                self.list_risultati.insert(END, value[0] + ' ' + value[1])

    def btn_scarica_click(self):
        try:
            # Todo da testare in locale prima
            # indice elemento da scaricare
            index = self.list_risultati.curselection()[0]
            logging.debug("selezionato: " + self.risultati[index])
            # prendo l'elemento da scaricare
            info = Utility.listLastSerch[index]

            #Classe che esegue il download di un file
            down=Scaricamento(info)
            down.run()
            self.prog_scaricamento.start(20)
        except Exception as e:
            logging.debug("NULLA SELEZIONATO")

    def btn_aggiungi_file_click(self):
        path_file = askopenfilename(initialdir=Utility.PATHDIR)

        if path_file != '':
            sock_end = Request.create_socket(Utility.IP_TRACKER, Utility.PORT_TRACKER)
            Request.add_file(sock_end, path_file)
            num_parts = Response.add_file_ack(sock_end)
            Response.close_socket(sock_end)

            md5_file = Utility.generateMd5(path_file)
            file_name = path_file.split('/')[-1]
            elem = (md5_file, file_name, num_parts)

            ## aggiornamento database ocn l'aggiunta del file e delle parti
            Utility.database.addFile(Utility.sessionID, file_name, md5_file, os.stat(path_file).st_size, Utility.LEN_PART)
            Utility.database.addPart(md5_file, Utility.sessionID, '1' * num_parts)

            Divide.Divider.divide(Utility.PATHDIR, Utility.PATHTEMP, file_name, Utility.LEN_PART)

            self.file_aggiunti.append(elem)
            self.list_file.insert(END, file_name)

            self.print_console('elemento aggiunto: ' + str(elem))
            logging.debug('aggiunto: ' + path_file)

    def btn_rimuovi_file_click(self):
        try:
            index = self.list_file.curselection()[0]
            del self.file_aggiunti[index]
            self.list_file.delete(index, index)
            logging.debug("rimosso: " + str(index))
        except Exception as e:
            logging.debug("NULLA SELEZIONATO")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    tracker = False

    if tracker:
        tcpServer = Tracker(Utility.database, Utility.IPv4_TRACKER + '|' + Utility.IPv6_TRACKER, Utility.PORT_TRACKER)
        tcpServer.run()

    else:
        root = Tk()
        root.geometry("800x600")
        app = Window(root=root)

        tcpServer = Tracker(Utility.database, Utility.IP_MY,  Utility.PORT_MY)
        tcpServer.start()

        root.mainloop()
