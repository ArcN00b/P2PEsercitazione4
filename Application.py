#!/usr/bin/python3

from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.filedialog import askopenfilename
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
        self.text_console.insert(END,mess)

    def btn_login_click(self):
        self.status.set("SEI LOGGATO")
        self.print_console("LOGIN")

    def btn_logout_click(self):
        self.status.set("DISCONNESSO")
        logging.debug("LOGOUT")

    def btn_ricerca_click(self):
        logging.debug("STAI CERCANDO: "+self.en_ricerca.get())
        self.list_risultati.delete(0,END)
        ## simulazione ciclo di ricerca
        self.risultati = []
        for i in range(0,20):
            self.risultati.append("risultato " + self.en_ricerca.get() + str(i))

        for value in self.risultati:
            self.list_risultati.insert(END, value)

    def btn_scarica_click(self):
        try:
            index = self.list_risultati.curselection()[0]
            logging.debug("selezionato: " + self.risultati[index])

            self.prog_scaricamento.start(20)
        except Exception as e:
            logging.debug("NULLA SELEZIONATO")

    def btn_aggiungi_file_click(self):
        file_path = askopenfilename(initialdir="/home/marco/seedfolder/")
        if file_path != '':
            self.file_aggiunti.append(file_path)
            list_name = file_path.split('/')
            self.list_file.insert(END, list_name[-1])

        logging.debug(file_path)

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

    root = Tk()
    root.geometry("800x600")
    app = Window(root=root)

    root.mainloop()