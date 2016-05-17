import threading
import socket
import struct
import time
import select
from Utility import *
from Worker import *

class Tracker(threading.Thread):
#class Tracker():

    def __init__(self, database,ip,porta):
        # definizione thread del client
        threading.Thread.__init__(self)
        self.database=database
        self.ipv4,self.ipv6=Utility.getIp(ip)
        self.port=porta
        self.running = True

    def run(self):
        # Creo il socket ipv4, imposto l'eventuale riutilizzo, lo assegno all'ip e alla
        try:
            self.server_socket4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket4.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket4.bind((self.ipv4, self.port))

        # Gestisco l'eventuale exception
        except socket.error as msg:
            print('Errore durante la creazione del socket IPv4: ' + msg[1])
            exit(0)

        # Creo il socket ipv6, imposto l'eventuale riutilizzo, lo assegno all'ip e alla porta
        try:
            self.server_socket6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            self.server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket6.bind((self.ipv6, self.port))

        # Gestisco l'eventuale exception
        except socket.error as msg:
            print('Errore durante la creazione del socket IPv6: ' + msg[1])
            exit(0)
        # Metto il server in ascolto per eventuali richieste sui socket appena creati
        self.server_socket4.listen(50)
        self.server_socket6.listen(50)

        #Ciclo continuo
        while self.running:
            # Per non rendere accept() bloccante uso l'oggetto select con il metodo select() sui socket messi in ascolto
            print("server in ascolto")
            input_ready, read_ready, error_ready = select.select([self.server_socket4, self.server_socket6], [], [])

            # Ora controllo quale dei due socket ha ricevuto una richiesta
            for s in input_ready:

                # Il client si è collegato tramite socket IPv4, accetto quindi la sua richiesta avviando il worker
                if s == self.server_socket4:
                    client_socket4, address4 = self.server_socket4.accept()
                    client_thread = Worker(client_socket4, self.database)
                    client_thread.run()

                # Il client si è collegato tramite socket IPv6, accetto quindi la sua richiesta avviando il worker
                elif s == self.server_socket6:
                    client_socket6, address6 = self.server_socket6.accept()
                    client_thread = Worker(client_socket6, self.database)
                    client_thread.run()

    # Idealmente questo dovrebbe fermare il cliclo while sopra
    #TODO da testare
    def stop(self):
        self.running = False
        self.server_socket4.shutdown()
        self.server_socket6.shutdown()
        self.server_socket4.close()
        self.server_socket6.close()