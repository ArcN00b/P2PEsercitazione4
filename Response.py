import random

#Tutti i metodi eseguono le operazioni sul database
#Necessitano quindi che sia passato il database in ingresso
class Response:

    #Metodo per la generazione della risposta ad una richiesta di login
    #Ritorna una stringa rappresentante il messaggio da inviare
    @staticmethod
    def login(database,ip,port):
        try:
            tmp='ALGI'
            #il metodo ricerca un client per id e port e se presente ritorna il sessionID altrimenti -1
            if (len(database.findClient('',ip,port,'1')) !=0):
                #tmp=tmp+database.findClient('',ip,port,'1')[0][0];
                tmp=tmp+('0'*16)
            else:
                #creazione della stringa di sessione in maniera casuale
                s='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                val=''
                for i in range(0,16):
                    val=val+s[random.randint(0,len(s)-1)]
                #aggiungo il client al database
                database.addClient(val,ip,port)
                tmp=tmp+val
            return tmp
        except Exception:
            raise ('Error')

    #Metodo per la generazione della risposta ad una richiesta di add
    #Ritorna una stringa rappresentante la risposta
    @staticmethod
    def addFile(database,fileMd5,sessionId,fileName):
        try:
            tmp='AADD'
            #controllo se il fileName ha almeno 100 caratteri se non ne ha ne aggiungo a destra
            nome=fileName
            if (len(fileName)<100):
                nome=fileName+(' '*(100-len(fileName)))
            #metodo che aggiune un file file md5 al database, aggiorna anche gli altri nome dei file
            database.addFile(sessionId,fileMd5,nome)
            #il metodo conta il numero di file con quel Md5, si suppone che l'aggiunta sia gia stata fatta
            n=database.numOfFile(fileMd5,'','1')
            #alla risposta aggiunge il numero di file con quel Md5 nella directory
            tmp=tmp+'{:0>3}'.format(n[0])
            return tmp
        except Exception:
            raise ('Error')

    @staticmethod
    def remove(database,fileMd5,sessionId):
        try:
            tmp='ADEL'
            #metodo che ricerca la presenza di un file md5 collegato ad un determinato sessioId
            val=database.searchIfExistFile(fileMd5,sessionId)
            if (val[0][0]==0):
                n=999
                tmp=tmp+'{:0>3}'.format(n)
            else:
                #chiamo il metodo per la rimozione del file
                database.removeFile(fileMd5,sessionId)
                #metodo che conta quanti file hanno quel md5
                n=database.numOfFile(fileMd5,'','1')
                tmp=tmp+'{:0>3}'.format(n[0])
            return tmp
        except Exception:
            raise ('Error')

    @staticmethod
    def logout(database,sessionId):
        try:
            tmp='ALGO'
            #conto quanti file quel peer aveva condiviso
            n=database.numOfFile('',sessionId,'2')
            #chiamo il metodo per la rimozione di tutti i file di quel peer
            database.removeAllFile(sessionId)
            #sono stati usati due metodi perchè non si sa se il database restituisca il numero
            #di righe eliminate con una delete
            tmp=tmp+'{:0>3}'.format(n[0])
            return tmp
        except Exception:
            raise Exception('Error')

    #ricerca da sistemare per vedere reale implementazione del database
    @staticmethod
    def search(database,stringa):
        try:
            stringa=stringa.strip()
            tmp='AFIN'
            if stringa == '*':
                str=''
            else:
                str=stringa
            # Metodo che ricerca ricerca il numero distinto di Md5 sulla base della stringa di ricerca
            listMd5=database.findMd5(str)
            tmp=tmp+'{:0>3}'.format(len(listMd5))
            for i in range(0,len(listMd5)):
                # Variabile che tiene in memoria l'iesimo md5
                md5=listMd5[i][0]
                tmp=tmp+md5
                # Ritorna tutti i sessionId e fileName dato un md5
                listSessionId=database.findFile(md5)
                # Aggiungo il nome del file alla stringa di ritorno
                tmp=tmp+listSessionId[0][0]
                # Aggiungo il numero file presenti con lo stesso md5
                val=database.numOfFile(md5,'','1')
                tmp=tmp+'{:0>3}'.format(val[0])
                for j in range(0,len(listSessionId)):
                    #Metodo che ritorna ip e porta dato un sessioID
                    #val=listSessionId[j][1]
                    val=database.findClient(listSessionId[j][1],'','','2')
                    tmp=tmp+val[0][0]+val[0][1]
                tmp=tmp

            return tmp
        except Exception:
            raise Exception('Error')

    #Metodo che elabora la response in caso di download
    @staticmethod
    def download(database,sessioId,fileMd5):
        try:
            tmp='ADRE'
            #Metodo che aggiunge un numero di download per sessionId e fileMd5, prende anche il numero da aggiungere
            n=database.addDownload(fileMd5,sessioId,1)
            tmp=tmp+'{:0>3}'.format(n)
            return tmp
        except Exception:
            raise Exception('Error')


'''
# Test del codice
from Response import *
from ManageDB import *

manager=ManageDB()

val=manager.findClient('','ip','port','1')
print(val)
print(len(val))
if (len(val)!=0):
    print('e zero')
else:
    print('non e zero')
if (len(manager.findClient('','ip','port','1'))!=0):
    print('e zero')
else:
    print('non e zero')
val=Response.login(manager,'ip','port')
print(val)
'''

# Test del codice
'''
from Response import *
from ManageDB import *

manager=ManageDB()

print('connetto vari client')
s1=Response.login(manager,'ip1','port1')
print(s1)
s2=Response.login(manager,'ip2','port1')
print(s2)
s3=Response.login(manager,'ip3','port1')
print(s3)
s4=Response.login(manager,'ip4','port1')
print(s4)
print('provo a connettere un client gia connesso')
val=Response.login(manager,'ip1','port1')
print(val)

print('provo a inserire vari oggetti')
val=Response.addFile(manager,'file1',s1[4:len(s1)],'pippo')
print(val)
val=Response.addFile(manager,'file1',s2[4:len(s2)],'pippo ciao ciao')
print(val)
val=Response.addFile(manager,'file2',s4[4:len(s4)],'pluto')
print(val)
val=Response.addFile(manager,'file2',s3[4:len(s3)],'pluto cin cin')
print(val)
val=Response.addFile(manager,'file3',s4[4:len(s4)],'pippo bau bau')
print(val)

print('provo a rimuovere un file e poi a eliminarlo di nuovo')
val=Response.remove(manager,'file1','9EQA4X6X1YBLCHN0')
print(val)
val=Response.remove(manager,'file1','9EQA4X6X1YBLCHN0')
print(val)

print('provo a eseguire una ricerca prima su pippo poi su *')
print('------1------')
val=Response.search(manager,'pippo')
print(val)
print('-----2----')
val=Response.search(manager,'*')
print(val)
'''


