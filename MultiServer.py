import select
import socket
import sys
import subprocess
from Worker import *
from ManageDB import *
from Utility import *
from Communication import *
from Menu import *
import os

# Insieme di costanti utilizzate nel progetto
#TCP_IP4 = '127.0.0.1'  # Con questo ip il bind viene effettuato su tutte le interfacce di rete
#TCP_IP6 = '::1'  # Con questo ip il bind viene effettuato su tutte le interfacce di rete

TCP_IP4 = 'localhost'
TCP_IP6 = '::1'

TCP_PORT = 3000

class MultiServer:

    database = None
    lock = None
    thread_list = {}
    server_socket4 = None
    server_socket6 = None

    def __init__(self):
        self.lock = threading.Lock()
        self.thread_list = {}

    def start(self,ipv4,ipv6):

        # Creo il socket ipv4, imposto l'eventuale riutilizzo, lo assegno all'ip e alla
        try:
            self.server_socket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket4.bind((ipv4, Utility.PORT))

        # Gestisco l'eventuale exception
        except socket.error as msg:
            print('Errore durante la creazione del socket IPv4: ' + msg[1])
            exit(0)

        # Creo il socket ipv6, imposto l'eventuale riutilizzo, lo assegno all'ip e alla porta
        try:
            self.server_socket6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket6.bind((ipv6, Utility.PORT))

        # Gestisco l'eventuale exception
        except socket.error as msg:
            print('Errore durante la creazione del socket IPv6: ' + msg[1])
            exit(0)
        # Metto il server in ascolto per eventuali richieste sui socket appena creati
        self.server_socket4.listen(5)
        self.server_socket6.listen(5)

        # Continuo ad eseguire questo codice
        while True:

            # Per non rendere accept() bloccante uso l'oggetto select con il metodo select() sui socket messi in ascolto
            print("server in ascolto")
            input_ready, read_ready, error_ready = select.select([self.server_socket4, self.server_socket6,sys.stdin], [], [])

            # Ora controllo quale dei due socket ha ricevuto una richiesta
            for s in input_ready:

                # Il client si è collegato tramite socket IPv4, accetto quindi la sua richiesta avviando il worker
                if s == self.server_socket4:
                    client_socket4, address4 = self.server_socket4.accept()
                    client_thread = Worker(client_socket4, self.lock)
                    client_thread.start()

                # Il client si è collegato tramite socket IPv6, accetto quindi la sua richiesta avviando il worker
                elif s == self.server_socket6:
                    client_socket6, address6 = self.server_socket6.accept()
                    client_thread = Worker(client_socket6,  self.lock)
                    client_thread.start()

                else:
                    sel=sys.stdin.readline()
                    Menu.function(sel)
                    #print(sys.stdin.readline() )
                    #pid=subprocess.Popen(args=["gnome-terminal","-e, python3 /home/flavio/Scrivania/ciao.py"]).pid

#Da qui si parte
#faccio scegliere all'utente se e supernodo o meno
sel=input("Sei supernodo [s/n] ? ")
while sel not in ['s', 'n']:
    sel=input("Sei supernodo [s/n] ? ")

#se sono supernodo metto porta 80 e sessionId='0000000000000000'
#altrimenti metto porta 3000
if sel=='s':
    Utility.sessionId='0'*16
    Utility.superNodo=True
    Utility.PORT=80
else:
    Utility.superNodo=False
    Utility.PORT=3000
Utility.stato='start'

#stampo il menu la prima volta
Menu.printMenu()
#Utility.database.addSuperNode("172.030.007.002|fc00:0000:0000:0000:0000:0000:0007:0002","00080")
tcpServer = MultiServer()
ipv4,ipv6=Utility.getIp(Utility.MY_IPV4+'|'+Utility.MY_IPV6)
tcpServer.start(ipv4,ipv6)