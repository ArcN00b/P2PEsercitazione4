# PEERS:        SESSIONID   IP          PORT
# FILES:        SESSIONID   NAME        MD5    LENFILE    LENPART
# PARTS:        MD5         SESSIONID   PART

import sqlite3
import time

# TODO testare i metodi del database
class ManageDB:

    # Metodo che inizializza il database
    def __init__(self):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Creo la tabella dei peer e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS PEERS")
            c.execute("CREATE TABLE PEERS (SESSIONID TEXT NOT NULL, IP TEXT NOT NULL, PORT TEXT NOT NULL)")

            # Creo la tabella dei file e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS FILES")
            c.execute("CREATE TABLE FILES (SESSIONID TEXT NOT NULL, NAME TEXT NOT NULL, MD5 TEXT NOT NULL, LENFILE TEXT NOT NULL, LENPART TEXT NOT NULL)")

            # Creo la tabella dei packetId e la cancello se esiste
            c.execute("DROP TABLE IF EXISTS PARTS")
            c.execute("CREATE TABLE PARTS (MD5 TEXT NOT NULL, SESSIONID TEXT NOT NULL,PART TEXT NOT NULL)")

            # Imposto il tempo di cancellazione dei packets
            self.deleteTime = 10

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - init: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che aggiunge un peer
    def addPeer(self, sessionId, ip, port):

        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il peer se non e' presente
            c.execute("SELECT COUNT(IP) FROM PEERS WHERE IP=:INDIP AND PORT=:PORTA", {"INDIP": ip, "PORTA": port})
            count = c.fetchall()

            if(count[0][0] == 0):
                c.execute("INSERT INTO PEERS (SESSIONID, IP, PORT) VALUES (?,?,?)" , (sessionId, ip, port))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - addPeer: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    #Metodo che rimuove un peer dato un sessionId
    def removePeer(self,sessionId):
        try:
            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT COUNT(SESSIONID) FROM PEERS WHERE SESSIONID=:SID", {"SID": sessionId})
            count = c.fetchall()

            if count[0][0]!=0:
                c.execute("DELETE FROM PEERS WHERE SESSIONID=:SID", {"SID": sessionId})
                conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removePeer: %s:" % e.args[0])

        finally:
            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che ritorna la lista dei peer
    def listPeer(self,flag):
        count=None
        try:
            # Connessione
            conn=sqlite3.connect("data.db")
            c=conn.cursor()

            if flag==1:
                c.execute("SELECT * FROM PEERS")
                count=c.fetchall()
            elif flag==2:
                c.execute("SELECT IP,PORT FROM PEERS")
                count=c.fetchall()

            conn.commit()

        except sqlite3.Error as e:
            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - listPeer: %s:" % e.args[0])
        finally:
            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo per trovare un peer
    def findPeer(self,sessionId,ip,port,flag):
        count=None
        try:
            # Connessione
            conn=sqlite3.connect("data.db")
            c=conn.cursor()

            if flag==1:
                c.execute("SELECT SESSIONID FROM PEERS WHERE IP=:INDIP AND PORT=:PORTA", {"INDIP": ip, "PORTA": port})
                count = c.fetchall()
            elif flag==2:
                c.execute("SELECT IP,PORT FROM PEERS WHERE SESSIONID=:SID", {"SID": sessionId})
                count = c.fetchall()

            conn.commit()

        except sqlite3.Error as e:
            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - findPeer: %s:" % e.args[0])
        finally:
            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo che aggiunge un file
    def addFile(self,sessionId,fileName,Md5,lenFile,lenPart):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il file se non e' presente
            c.execute("SELECT * FROM FILES WHERE NAME=:FNAME AND MD5=:M AND SESSIONID=:SID", {"FNAME": fileName, "M": Md5, "SID":sessionId})
            count = c.fetchall()

            if(len(count)==0):
                #c.execute("UPDATE FILES SET NAME=:NOME WHERE MD5=:COD" , {"NOME": fileName, "COD": Md5})
                #conn.commit()
                c.execute("INSERT INTO FILES (SESSIONID, NAME, MD5,LENFILE,LENPART) VALUES (?,?,?,?,?)" , (sessionId, fileName, Md5,lenFile,lenPart))
                conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - addFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che rimuove un file
    def removeFile(self,sessionId,Md5):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT COUNT(SESSIONID) FROM FILES WHERE SESSIONID=:SID AND MD5=:M", {"SID": sessionId, "M": Md5})
            count = c.fetchall()

            if count[0][0]!=0:
                c.execute("DELETE FROM FILES WHERE SESSIONID=:SID AND MD5=:M", {"SID": sessionId, "M": Md5})
                conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removeFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo che rimuove tutti i file di un sessionId
    def removeAllFileForSessionId(self,sessionId):
        count=None
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT COUNT(MD5) FROM FILES WHERE SESSIONID=:SID", {"SID": sessionId})
            count = c.fetchall()

            if (count[0][0]>0):
                c.execute("DELETE FROM FILES WHERE SESSIONID=:SID", {"SID": sessionId})
                conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removeAllFileForSessionId: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count[0][0]

    # Metodo per avere la lista di file per un sessionID
    def listFileForSessionId(self,sessionId):
        count=None
        try:
            # Connessione
            conn=sqlite3.connect("data.db")
            c=conn.cursor()

            c.execute("SELECT MD5,NAME,LENFILE,LENPART FROM FILES WHERE SESSIONID=:SID",{"SID":sessionId})
            count=c.fetchall()

            conn.commit()

        except sqlite3.Error as e:
            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - listFileForSessionId: %s:" % e.args[0])
        finally:
            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo ritorna tutta la tabella files
    def listFile(self):
        count=None
        try:
            # Connessione
            conn=sqlite3.connect("data.db")
            c=conn.cursor()

            c.execute("SELECT * FROM FILES")
            count=c.fetchall()

            conn.commit()

        except sqlite3.Error as e:
            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - listFile: %s:" % e.args[0])
        finally:
            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo per ricerca nome file da sessionId e Md5
    def findFile(self,sessionId,Md5,name,flag):
        count=None
        try:
            # Connessione
            conn=sqlite3.connect("data.db")
            c=conn.cursor()

            if flag == 1:
                c.execute("SELECT NAME FROM FILES WHERE SESSIONID=:SID AND MD5=:M",{"SID":sessionId,"M":Md5})
                count=c.fetchall()
            elif flag == 2:
                c.execute("SELECT SESSIONID,NAME FROM FILES WHERE MD5=:M",{"M":Md5})
                count=c.fetchall()
            elif flag == 3:
                c.execute("SELECT * FROM FILES WHERE NAME LIKE '%" + name + "%' ")
                count = c.fetchall()
            elif flag == 4:
                c.execute("SELECT SESSIONID FROM FILES WHERE SESSIONID!=SID MD5=:M",{"SID":sessionId,"M": Md5})
                count = c.fetchall()

            conn.commit()

        except sqlite3.Error as e:
            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - listFileForSessionId: %s:" % e.args[0])
        finally:
            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo per ricercare l'md5 del file da stringa di ricerca
    def findMd5(self, name):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Cerca il file
            c.execute("SELECT MD5,NAME,LENFILE,LENPART FROM FILES WHERE NAME LIKE '%" + name + "%' ")
            conn.commit()

            result = c.fetchall()
            return result

        except sqlite3.Error as e:

            raise Exception("Errore - findFile: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per aggiungere un file delle parti alla tabella
    def addPart(self,Md5,sessionId,parte):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            # Aggiungo il peer se non e' presente
            c.execute("SELECT * FROM PARTS WHERE MD5=:M AND SESSIONID=:SSID", {"M": Md5, "SSID": sessionId})
            count = c.fetchall()

            if(len(count)>0):
                c.execute("INSERT INTO PARTS (MD5, SESSIONID, PART) VALUES (?,?,?)" , (Md5,sessionId, parte))
            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - addPart: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per rimuovere tutti le parti da sessionId
    def removePart(self,sessionId):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT * FROM PARTS WHERE SESSIONID=:SID AND MD5=:M", {"SID": sessionId})
            count = c.fetchall()

            if len(count)>0:
                c.execute("DELETE FROM PARTS WHERE SESSIONID=:SID", {"SID": sessionId})
                conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - removeParts: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()

    # Metodo per cercare la parte dato un sessionID
    def findPartForSessionID(self,sessionId):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT MD5,PART FROM PARTS WHERE SESSIONID=:SID", {"SID": sessionId})
            count = c.fetchall()

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - findPartForSessionID: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo per cercare una parte dato un md5
    def findPartForMd5(self,Md5):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT SESSIONID,PART FROM PARTS WHERE MD5=:M", {"M": Md5})
            count = c.fetchall()

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - findPartForMd5: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Ritorna la parte dato un md5 e un sessionId
    def findPartForMd5AndSessionId(self,SessionId,Md5):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("SELECT PART FROM PARTS WHERE MD5=:M AND SESSIONID=SSID", {"M": Md5,"SSID":SessionId})
            count = c.fetchall()

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - findPartForMd5AndSessionId: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()
            if count is not None:
                return count

    # Metodo per aggiornare la parte dati sessionId e Md5
    def updatePart(self,sessionId,md5,part):
        try:

            # Creo la connessione al database e creo un cursore ad esso
            conn = sqlite3.connect("data.db")
            c = conn.cursor()

            c.execute("UPDATE PARTS SET PART=:P WHERE MD5=:M AND SESSIONID=SSID" , {"P": part, "M": md5,"SSID":sessionId} )

            conn.commit()

        except sqlite3.Error as e:

            # Gestisco l'eccezione
            if conn:
                conn.rollback()

            raise Exception("Errore - updatePart: %s:" % e.args[0])

        finally:

            # Chiudo la connessione
            if conn:
                conn.close()


# SUPERNODES:   IP          PORT
# PEERS:        SESSIONID   IP      PORT
# FILES:        SESSIONID   NAME    MD5
# PACKETS:      ID      DATE
'''
manager = ManageDB()

print("Aggiungo Peer")
manager.addPeer("123", "1.1.1.1", "3000")
manager.addPeer("456", "1.1.1.2", "3000")
manager.addPeer("789", "1.1.1.3", "3000")
print("Lista Peer")
all_rows = manager.listPeer()
for row in all_rows:
    print('{0} {1} {2}'.format(row[0],row[1],row[2]))
print("")


print("Aggiungo SuperNodo")
manager.addSuperNode("10.10.10.10", "80")
manager.addSuperNode("20.20.20.20", "80")
print("Lista SuperNodi")
all_rows = manager.listSuperNode()
for row in all_rows:
    print('{0} {1}'.format(row[0],row[1]))
print("")


print("Metodo findPeer flag 1")
all_rows = manager.findPeer(0,"1.1.1.3","3000",1)
for row in all_rows:
    print('{0}'.format(row[0]))
print("")


print("Metodo findPeer flag 2")
all_rows = manager.findPeer("123",0,0,2)
for row in all_rows:
    print('{0} {1}'.format(row[0],row[1]))
print("")


print("Aggiungo File")
manager.addFile("123","pippo","1111")
manager.addFile("123","pluto","2222")
manager.addFile("456","pluto2","2222")
manager.addFile("456","paperino","3333")
print("Lista File")
all_rows = manager.listFile()
for row in all_rows:
    print('{0} {1} {2}'.format(row[0],row[1],row[2]))
print("")


print("Rimuovo File")
manager.removeFile("123","2222")
print("Lista File")
all_rows = manager.listFile()
for row in all_rows:
    print('{0} {1} {2}'.format(row[0],row[1],row[2]))
print("")


print("Lista File da SessionID")
all_rows = manager.listFileForSessionId("456")
for row in all_rows:
    print('{0} {1}'.format(row[0],row[1]))
print("")


print("Rimuovo tutti File da SessionID")
manager.removeAllFileForSessionId("456")
print("Lista File")
all_rows = manager.listFile()
for row in all_rows:
    print('{0} {1} {2}'.format(row[0],row[1],row[2]))
print("")
'''

