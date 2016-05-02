import re

# Classe che implementa i metodi per eseguire controlli e suddivisioni del messaggio ricevuto
class Parser:

    # Metodo statico che si occupa di suddividere i vari campi di data in modo consono
    @staticmethod
    def parse(data):

        # Inizializzo il contenitore dei vari campi
        fields = {}

        # Prendo i primi 4 caratteri maiuscoli all'interno di data e li inserisco in command
        command = data[0:4]

        # Parsing LOGI
        if command == 'LOGI':
            fields[0] = data[4:59]      # IPP2P[55B]
            fields[1] = data[59:64]     # PP2P[5B]

        # Parsing ALGI
        elif command == 'ALGI':
            fields[0] = data[4:20]      # SessionID[16B]

        # Parsing LOGO
        elif command == 'LOGO':
            fields[0] = data[4:20]       # SessionID[16B]

        # Parsing ALOG
        elif command == 'ALGO':
            fields[0] = data[4:7]       # Num Delete[3B]

        elif command == 'NLOG':
            fields[0] == data[4:7]      # numero parti scaricate

        # Parsing ADFF
        elif command == 'ADFF':
            fields[0] = data[4:20]      # SessionID[16B]
            fields[1] = data[20:52]     # MD5[32B]
            fields[2] = data[52:152]    # FileName[100B]

        # Parsing DEFF
        elif command == 'DEFF':
            fields[0] = data[4:20]      # SessioID[16B]
            fields[1] = data[20:52]     # MD5[32B]

        # Parsing QUER
        elif command == 'QUER':
            fields[0] = data[4:20]      # PKTID[16B]
            fields[1] = data[20:75]     # IPP2P[55B]
            fields[2] = data[75:80]     # PP2P[5B]
            fields[3] = data[80:82]     # TTL[2B]
            fields[4] = data[82:102]    # Ricerca[20B]

        # Parsing AQUE
        elif command == 'AQUE':
            fields[0] = data[4:20]      # PKTID[16B]
            fields[1] = data[20:75]     # IPP2P[55B]
            fields[2] = data[75:80]     # PP2P[5B]
            fields[3] = data[80:112]    # MD5[32B]
            fields[4] = data[112:212]   # FileName[100B]

        elif command == 'FIND':
            fields[0] = data[4:20]      # SessioID[16B]
            fields[1] = data[-20:]      # Ricerca[20B]

        elif command == 'AFIN':
            fields[0] = data[4:7]       # Num idm5[3B]

        # Parsing RETR
        elif command == 'RETR':
            fields[0] = data[4:36]  # MD5[32B]

        # Parsing ARET
        elif command == 'ARET':
            fields[0] = data[4:10] #Num Chunk

        # Se questo else viene eseguito significa che il comando ricevuto non e previsto
        else:
            print('Errore durante il parsing del messaggio\n')

        # Eseguo il return del comando e dei campi del messaggio
        return command, fields