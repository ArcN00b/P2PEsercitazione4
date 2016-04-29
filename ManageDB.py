# In questo file viene definita una classe che definisce metodi utili a gestire il database SQLite di Python
# Per creare il database, usare il comando da shell: sqlite3 data.db

import sqlite3
import sys

class ManageDB:
    # Metodo che inizializza il database
    def __init__(self):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Creo la tabella dei client e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS CLIENTS;")
            c.execute("CREATE TABLE CLIENTS (SESSIONID TEXT NOT NULL, IP TEXT NOT NULL, PORT TEXT NOT NULL);")

            # Creo la tabella dei file e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS FILES;")
            c.execute("CREATE TABLE FILES (NAME TEXT NOT NULL, MD5 TEXT NOT NULL, SESSIONID TEXT NOT NULL, NUMDOWN INTEGER DEFAULT 0);")

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 01 - initialize: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un client che ha fatto il login
    def addClient(self, sessionId, ip, port):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il client
            c.execute("INSERT INTO CLIENTS (SESSIONID, IP, PORT) VALUES (?,?,?)" , (sessionId,ip, port))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 02 - addClient: %s:" % e.args[0])
            raise Exception("Errore")

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un file aggiunto da un client
    def addFile(self, sessionId, md5, name):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Controllo se esiste il file
            c.execute("SELECT COUNT(MD5) FROM FILES WHERE MD5=:COD AND SESSIONID=:ID" , {"COD": md5 , "ID": sessionId})
            num = c.fetchall()

            # Aggiungo  il file se non e' presente
            if num[0][0] == 0:
                c.execute("INSERT INTO FILES (NAME, MD5, SESSIONID, NUMDOWN) VALUES (?,?,?,?)" , (name, md5, sessionId, 0))

            # Aggiorno il nome dei file con lo stesso MD5
            c.execute("UPDATE FILES SET NAME=:NOME WHERE MD5=:COD" , {"NOME": name, "COD": md5} )
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 03 - addFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina il client tramite indirizzo ip
    def removeClient(self, sessionId):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il client
            c.execute("DELETE FROM CLIENTS WHERE SESSIONID = ? " , (sessionId,))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 04 - removeClient: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina il file identificato da nome e md5
    def removeFile(self, md5, sessionId):

        # Il metodo non fa distinzione da chi ha caricato il file
        # Risulta raro che per errore vada a rimuovere un file caricato da piu' utenti, dato che md5 identifica il file

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo il file
            c.execute("DELETE FROM FILES WHERE SESSIONID=:ID AND MD5=:COD" , {"ID": sessionId, "COD": md5} )
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 05 - removeFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che elimina tutti i file di un client
    def removeAllFile(self, sessionId):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Rimuovo tutti i file
            c.execute("DELETE FROM FILES WHERE SESSIONID=:ID" , {"ID": sessionId} )
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            print("Codice Errore 06 - removeAllFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per ricercare il client tramite id e port, se flag settato a 1, altrimenti ricerco per id
    def findClient(self, sessionId, ip, port, flag):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il client
            if flag == '1':
                c.execute("SELECT SESSIONID FROM CLIENTS WHERE IP=:INDIP AND PORT=:PORTA", {"INDIP": ip, "PORTA": port})
            else:
                c.execute("SELECT IP, PORT FROM CLIENTS WHERE SESSIONID = ? " , (sessionId,))
            conn.commit()

            result=c.fetchall()
            return result


        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 07 - findClient: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


    # Metodo per ricercare le informazioni del file per md5
    def findFile(self,md5):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT NAME,SESSIONID FROM FILES WHERE MD5 = ? " , (md5,))
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 08 - findFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per ricercare le informazioni del file per md5
    def findMd5(self,name):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT DISTINCT MD5 FROM FILES WHERE NAME LIKE '%" + name + "%' ")
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 08 - findFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per verificare se un file esiste
    def searchIfExistFile(self,md5,sessionId):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT COUNT(MD5) FROM FILES WHERE MD5=:COD AND SESSIONID=:ID" , {"COD": md5 , "ID": sessionId})
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 09 - searchIfExistFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che ritorna il numero di file presenti con quel md5 o id
    def numOfFile(self,md5,sessionId,flag):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            if flag == '1':
                c.execute("SELECT COUNT(MD5) FROM FILES WHERE MD5 = ? " , (md5,))
            else:
                c.execute("SELECT COUNT(MD5) FROM FILES WHERE SESSIONID = ? " , (sessionId,))

            conn.commit()

            result = c.fetchone()
            return result

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 10 - numOfFile: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


    # Metodo che incrementa il numero di download di un file
    def addDownload(self,md5,sessionId,inc):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo il numero di download
            c.execute("SELECT NUMDOWN FROM FILES WHERE MD5=:COD " , {"COD": md5})
            res = c.fetchone()
            ndown = res[0] + inc

            # Aggiorno ilnumero di download
            c.execute("UPDATE FILES SET NUMDOWN=:NUM WHERE MD5=:COD" , {"NUM": ndown, "COD": md5})

            conn.commit()

            return ndown

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 11 - addDownload: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che per visualizzare la lista di utenti connessi
    def listClient(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di client connessi
            c.execute("SELECT * FROM CLIENTS")
            conn.commit()

            return c.fetchall()

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 12 - ListCLients: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che per visualizzare la lista di file registrati
    def listMD5(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di file registrati
            c.execute("SELECT MD5, SESSIONID, NUMDOWN, NAME FROM FILES")
            conn.commit()

            return c.fetchall()

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 13 - ListMD5: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che per visualizzare la lista di utenti connessi
    def topDownload(self):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Prelevo la lista di client connessi
            c.execute("SELECT DISTINCT MD5, NAME, NUMDOWN FROM FILES ORDER BY NUMDOWN")
            conn.commit()

            return c.fetchall()

        except sqlite3.Error as e:
            #In caso di errore stampo l'errore
            print ("Codice Errore 14 - mostDownloaded: %s:" % e.args[0])
            raise Exception()

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()



'''
manager = ManageDB()

# TEST FILE
manager = ManageDB()

# Aggiungo un file
manager.addFile("1","123","Test1")
num = manager.addDownload("123","1",0)
print("1) Numero download: {0}" .format(num)) #0

print("File presenti")
all_rows = manager.findFile("123")
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")

# Incremento il numero di download del file inserito
print("2) Incremento download 5")
num = manager.addDownload("123","1",5)
print("3) Numero download: {0}" .format(num)) #5

print("File presenti")
all_rows = manager.findFile("123")
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")

# Cambio il nome del file e incremento i download e incremento i download
print("4) Cambio nome file esistente da stesso client e incremento i download")
manager.addFile("1","123","Test2")
num = manager.addDownload("123","1",5)
print("5) Numero download: {0}" .format(num)) #10

print("File presenti")
all_rows = manager.findFile("123")
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")

# Un altro client inserisce lo stesso file e incremento il num di download del file di quel client
print("6) Cambio nome file esistente da altro client")
manager.addFile("2","123","Test3")
num = manager.addDownload("123","2",7)
print("7) Numero download: {0}" .format(num)) #7

print("File presenti")
all_rows = manager.findFile("123")
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
print("")

# Controllo che il numero di download del primo file inserito non sia cambiato
print("8) Controllo il numero di download del primo file")
num = manager.addDownload("123","1",0)
print("9) Numero download primo file: {0}" .format(num)) #5
num = manager.addDownload("123","2",0)
print("9) Numero download secondo file: {0}" .format(num)) #7
'''

'''
# TEST CLIENT
manager = ManageDB()
manager.addClient("1","192.168.0.2","3000")

print ("Test primo findClient: " )
all_rows = manager.findClient("1", "0", "0", "2")
for row in all_rows:
    print('ip: {0}, porta: {1}'.format(row[0], row[1]))


print ("Test seondo findClient: " )
all_rows = manager.findClient("0", "192.168.0.2", "3000", "1")
for row in all_rows:
    print('id: {0}'.format(row[0]))

print("Test removeClient")
manager.removeClient("1")
all_rows = manager.findClient("1", "0", "0", "2")
for row in all_rows:
    print('{0} : {1}'.format(row[0], row[1]))
'''



