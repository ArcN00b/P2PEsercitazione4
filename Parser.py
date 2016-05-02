import re

# Classe che implementa i metodi per eseguire controlli e suddivisioni del messaggio ricevuto
class Parser:

    # Metodo statico che si occupa di suddividere i vari campi di data in modo consono
    @staticmethod
    def parse(data,cod):

        # Inizializzo il contenitore dei vari campi
        fields = {}

        # Prendo i primi 4 caratteri maiuscoli all'interno di data e li inserisco in command
        command = data[0:4].decode()

        # Parsing LOGI
        if command == 'LOGI':
            fields[0] = data[4:59].decode()      # IPP2P[55B]
            fields[1] = data[59:64].decode()   # PP2P[5B]

        # Parsing ALGI
        elif command == 'ALGI':
            fields[0] = data[4:20].decode()      # SessionID[16B]

        # Parsing ADDR
        elif command == 'ADDR':
            fields[0] = data[4:20].decode()      # SessionID[16B]
            fields[1] = data[20:30].decode()    #LenFile[10B]
            fields[2] = data[30:36].decode()    #LenPart[6B]
            fields[3] = data[36:136].decode()    # FileName[100B]
            fields[4] = data[136:158].decode()     # MD5[32B]

        # Parsing AADR
        elif command == 'AADR':
            fields[0] = data[4:12].decode()      # Num parti[8B]

        # Parsing LOOK
        elif command == 'LOOK':
            fields[0] = data[4:20].decode()     # SessionID[16B]
            fields[1] = data[20:40].decode()    # Ricerca[20B]

        # Parsing ALOO
        elif command== 'ALOO':
            fields[0] = data[4:7].decode()      #Num MD5[3B]

        # Parsing FCHU
        elif command == 'FCHU':
            fields[0]= data[4:20].decode()      #SessionId[16B]
            fields[1]=data[20:52].decode()      # MD5[32B]

        #Parsing AFCH
        elif command == 'AFCH':
            fields[0]=data[4:7].decode()        # num hit peer[3B]

        # Parsing RETP
        elif command == 'RETP':
            fields[0]=data[4:36].decode()       # Md5_i[32B]
            fields[1]=data[36:44].decode()      # Num Part[8B]

        # Parsing AREP
        elif command == 'AREP':
            fields[0]=data[4:10].decode()       # num chunck[6B]

        # Parsing RPAD
        elif command=='RPAD':
            fields[0]=data[4:20].decode()       # SessionId[16B]
            fields[1]=data[20:52].decode()      # MD5[32B]
            fields[2]=data[52:60].decode()      # Num parte[8B]

        # Parsing APAD
        elif command=='APAD':
            fields[0]=data[4:12].decode()       #NUm part[8B]

        # Parsing LOGO
        elif command == 'LOGO':
            fields[0] = data[4:20].decode()      # SessionID[16B]

        # Parsing ALOG
        elif command == 'ALOG':
            fields[0] = data[4:14].decode()       # Num Part Down[3B]

        # Parsing NLOG
        elif command == 'NLOG':
            fields[0] = data[4:14].decode()       # Num Part Down[3B]

        # Se questo else viene eseguito significa che il comando ricevuto non e previsto
        else:
            print('Errore durante il parsing del messaggio\n')

        # Eseguo il return del comando e dei campi del messaggio
        return command, fields


'''
    # Metodo statico che controlla la corretta formattazione del parametro data
    @staticmethod
    def check(data):

        # Inizializzo la lista di comandi e un flag degli errori
        command_list = ['QUER', 'AQUE', 'NEAR', 'ANEA', 'RETR', 'ARET']
        error = False

        # Controllo che il comando sia effettivamente tra quelli riconosciuti
        command = data[0:4]
        if command not in command_list:
            error = True
            print('Errore, comando (' + command + ') non riconosciuto \n')

        # Se il comando e QUER eseguo questi controlli tramite regex
        if command == 'QUER' and not error:
            p = re.compile('[\dA-Z]{16}(\d{3}\.){3}\d{3}\|([\da-fA-F]{4}\:){7}[\da-fA-F]{4}\d{5}\d{2}[\da-zA-Z\.\ ]{20}$')
            if p.search(data) == None:
                error = True

        # Se il comando e AQUE eseguo questi controlli tramite regex
        elif command == 'AQUE' and not error:
            p = re.compile('[\dA-Z]{16}(\d{3}\.){3}\d{3}\|([\da-fA-F]{4}\:){7}[\da-fA-F]{4}\d{5}[\da-zA-Z]{32}[\da-zA-Z\.\ ]{100}$')
            if p.search(data) == None:
                error = True

        # Se il comando e NEAR eseguo questi controlli tramite regex
        elif command == 'NEAR' and not error:
            p = re.compile('[\dA-Z]{16}(\d{3}\.){3}\d{3}\|([\da-fA-F]{4}\:){7}[\da-fA-F]{4}\d{5}\d{2}$')
            if p.search(data) == None:
                error = True

        # Se il comando e ANEA eseguo questi controlli tramite regex
        elif command == 'ANEA' and not error:
            p = re.compile('[\dA-Z]{16}(\d{3}\.){3}\d{3}\|([\da-fA-F]{4}\:){7}[\da-fA-F]{4}\d{5}$')
            if p.search(data) == None:
                error = True

        # Se il comando e RETR eseguo questi controlli tramite regex
        elif command == 'RETR' and not error:
            p = re.compile('[\da-zA-Z]{32}$')
            if p.search(data) == None:
                error = True

        # Se il comando e ARET suddivido data in questo modo
        elif command == 'ARET' and not error:
            p = re.compile('\d{6}')
            if p.search(data) == None:
                error = True

        # Se questo else viene eseguito significa che il comando ricevuto non e previsto
        if not error:
            print('Il messaggio e ben formattato\n')
        else:
            print('Errore' + data + '\n')

    '''
'''
# Testing
from Parser import *

ip='127.000.000.001|fc00:0000:0000:0000:0000:0000:0007:0001'
id='1234567890123456'
port='03000'
ttl='99'
md5='00000000000000001234567890123456'
ricerca='pippo'+' '*(20-len('pippo'))
name='paperino'+' '*(100-len('paperino'))

# Check Supe
comand,campi=Parser.parse("SUPE"+id+ip+port+ttl)
#Check asup
comand,campi=Parser.parse("ASUP"+id+ip+port)
#Check logi
comand,campi=Parser.parse("LOGI"+ip+port)
#Check alog
comand,campi=Parser.parse("ALGI"+id)
#Check Adff
comand,campi=Parser.parse("ADFF"+id+md5+name)
#Check deff
comand,campi=Parser.parse("DEFF"+id+md5)
#Check LOGO
comand,campi=Parser.parse("LOGO"+id)
#check ALOG
comand,campi=Parser.parse("ALGO001")
#check QUER
comand,campi=Parser.parse("QUER"+id+ip+port+ttl+ricerca)
# check AQUE
comand,campi=Parser.parse("AQUE"+id+ip+port+md5+name)

True
True
'''
