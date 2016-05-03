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
