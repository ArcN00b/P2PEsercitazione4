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

        # Se il comando è LOGI suddivido data in questo modo
        if command == 'LOGI':
            fields[0] = data[4:-5] #IPP2P[55B]
            fields[1] = data[-5:] #PP2P[5B]

        # Se il comando è ADDF suddivido data in questo modo
        elif command == 'ADDF':
            fields[0] = data[4:20] #SessionID[16]
            fields[1] = data[20:52] #FileMD5[32]
            fields[2] = data[-100:] #Filename[100]

        # Se il comando è DELF suddivido data in questo modo
        elif command == 'DELF':
            fields[0] = data[4:20] #SessionID[16]
            fields[1] = data[-32:] #FileMD5[32]

        # Se il comando è FIND suddivido data in questo modo
        elif command == 'FIND':
            fields[0] = data[4:20] #SessionID[16]
            fields[1] = data[-20:] #Ricerca[20]

        # Se il comando è DELF suddivido data in questo modo
        elif command == 'DREG':
            fields[0] = data[4:20] #SessionID[16]
            fields[1] = data[-32:] #FileMD5[32]

        # Se il comando è LOGO suddivido data in questo modo
        elif command == 'LOGO':
            fields[0] = data[-16:] #SessionID[16]

        # Se questo else viene eseguito significa che il comando ricevuto non è previsto
        else:
            print('Errore durante il parsing del messaggio\n')

        # Eseguo il return del comando e dei campi del messaggio
        return command, fields



    # Metodo statico che controlla la corretta formattazione del parametro data
    @staticmethod
    def check(data):

        # Inizializzo la lista di comandi e un flag degli errori
        command_list = ['LOGI', 'ADDF', 'DELF', 'FIND', 'DREG', 'LOGO']
        error = False

        # Controllo che il comando sia effettivamente tra quelli riconosciuti
        command = data[0:4]
        if command not in command_list:
            error = True
            print('Errore, comando (' + command + ') non riconosciuto \n')

        # Se il comando è LOGI eseguo questi controlli tramite regex
        if command == 'LOGI' and not error:
            p = re.compile('(\d{3}\.){3}\d{3}\|([\da-fA-F]{4}\:){7}[\da-fA-F]{4}\d{5}$')
            if p.search(data) == None:
                error = True
                print('Errore, i campi IPP2P e PP2P non sono formattati correttamente \n')

        # Se il comando è ADDF eseguo questi controlli tramite regex
        elif command == 'ADDF' and not error:
            p = re.compile('[\dA-Z]{16}[\da-zA-Z]{32}[\da-zA-Z\.\ ]{100}$')
            if p.search(data) == None:
                error = True
                print('Errore, i campi SessionID, FileMD5 e Filename non sono formattati correttamente\n')

        # Se il comando è DELF eseguo questi controlli tramite regex
        elif command == 'DELF' and not error:
            p = re.compile('[\dA-Z]{16}[\da-zA-Z]{32}$')
            if p.search(data) == None:
                error = True
                print('Errore, i campi SessionID e FileMD5 non sono formattati correttamente\n')

        # Se il comando è FIND eseguo questi controlli tramite regex
        elif command == 'FIND' and not error:
            p = re.compile('[\dA-Z]{16}[\da-zA-Z\.\ ]{20}$')
            if p.search(data) == None:
                error = True
                print('Errore, i campi SessionID e Ricerca non sono formattati correttamente\n')

        # Se il comando è DREG eseguo questi controlli tramite regex
        elif command == 'DREG' and not error:
            p = re.compile('[\dA-Z]{16}[\da-zA-Z]{32}$')
            if p.search(data) == None:
                error = True
                print('Errore, i campi SessionID e FileMD5 non sono formattati correttamente\n')

        # Se il comando è LOGO suddivido data in questo modo
        elif command == 'LOGO' and not error:
            p = re.compile('[\dA-Z]{16}$')
            if p.search(data) == None:
                error = True
                print('Errore, il campo SessionID non è formattato correttamente\n')

        # Se questo else viene eseguito significa che il comando ricevuto non è previsto
        if not error:
            print('Il messaggio è ben formattato\n')
        else:
            print(data + '\n')