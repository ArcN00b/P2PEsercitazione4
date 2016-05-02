# P2PEsercitazione4

Parti parallele
Il sistema a parti parallele è analogo al meccanismo a directory centralizzata in quanto ogni peer ha la necessità di comunicare al tracker le parti che mette a disposizione, aggiornandone periodicamente lo stato. Ogni peer può mettere a disposizione nuovi file ma si vincola a mettere a disposizione tutte le parti dei file che ha richiesto. Il download avviene richiedendo più parti in parallelo da differenti peer. La scelta dei peer da utilizzare per il download è effettuata dal peer ricevente, sulla base della conoscenza aggiornata delle parti possedute da ciascun peer, con un meccanismo che privilegia le parti meno presenti e che comunque sceglie a caso tra i peer a parità di priorità. I peer forniscono al tracker un aggiornamento periodico della situazione delle proprie parti e richiedono la situazione aggiornata delle parti relative ai file di cui stanno effettuando il download.
Login
Ogni peer con indirizzo IPP2P, abile a fornire contenuti sulla porta PP2P, deve registrarsi sul tracker mediante un processo di login, indicando il proprio indirizzo e la relativa porta di comunicazione, che viene posta in ascolto. Il tracker è in ascolto all’indirizzo IPD sulla porta 3000. Il processo di login ritorna un codice di sessione SessionID di 16B, composto da una stringa di caratteri random generato da numeri e lettere maiuscole scelti casualmente. Qualora il peer sia già registrato viene ritornato il SessionID, qualora altresì vi siano problematiche per cui la registrazione risulti non possibile il codice di ritorno è “0000000000000000”, codice che si ritiene a probabilità quasi nulla come SessionID. Con il login il peer si pone in ascolto all’indirizzo IPP2P e sulla posta PP2P.

IPP2P:RND <> IPT:3000
=> “LOGI”[4B].IPP2P[55B].PP2P[5B]
<= “ALGI”[4B].SessionID[16B]

Aggiunta
Ogni peer registrato può mettere a disposizione un file in un qualsiasi momento comunicandolo al tracker. ll file è identificato da una stringa di 100B che lo descrive e sul quale è possibile effettuare una ricerca che dal relativo md5 ottenuto dal file aggiungendo in coda il proprio indirizzo IPv4+IPv6 in modo da generare un identificativo unico per ogni sorgente, correlato alle dimensioni delle parti. Ogni peer che mette a disposizione un contenuto comunica sia la dimensione complessiva del file che la dimensione della singola parte. La dimensione tipica, ma non vincolante, di una parte è 256KB=262144B. ll numero delle parti è tipicamente #part=supint[LenFile/LenPart].

IPP2P:RND <> IPT:3000
=> “ADDR”[4B].SessionID[16B].LenFile[10B].LenPart[6B].Filename[100B].Filemd5_i[32B]
<= “AADR”[4B].#part[8B]

Ricerca
La ricerca di un file è un processo che avviene in due fasi. La prima fase serve per identificare il file a cui il peer è effettivamente interessato mentre la seconda fase serve per avere la situazione delle parti su ogni peer e viene ripetuta periodicamente durante il download.

La prima fase avviene indicando una stringa di ricerca di 20B. Tale stringa viene utilizzata per effettuare una ricerca case insensive su tutti i titoli presenti, trovando ogni occorrenza della stringa stessa. Sono possibili più riscontri di differenti titoli con differente md5 relativi alla stessa stringa di ricerca. La risposta è quindi articolata nel numero complessivo di identificativi md5 #idmd5 dove per ognuno viene riportato l’identificativo md5 e il nome del file.

IPP2P:RND <> IPT:3000
=> “LOOK”[4B].SessionID[16B].Ricerca[20B]
<= “ALOO”[4B].#idmd5[3B].{Filemd5_ i[32B].Filename_i[100B].LenFile[10B].LenPart[6B]}(i=1..#idmd5)

La seconda fase avviene periodicamente ed ha lo scopo di indicare l’attuale situazione di ogni parte per un dato file identificato dal proprio md5 su ogni peer che ne ha effettuato il download o che lo ha immesso nel sistema. Complessivamente il numero dei peer che hanno interesse al file in questione sono #hitpeer. Sebbene le ottimizzazioni non siano un elemento affrontato in questo contesto, la lista delle parti disponibili può risultare particolarmente lunga ed onerosa da trasferire periodicamente, per cui PartList viene rappresentata direttamente in binario, dove 0 implica assenza di parte e 1 invece presenza. Considerando una rappresentazione a 8 bit, il vettore di byte che rappresenta la PartList ha dimensione #part8=supint[#part/8] e le informazioni di presenza o assenza sono rappresentate al Byte B=infint[part/8] e al bit b=part mod 8 (dove il b=0 è LSB cioè quello più a sinistra e b=7 è MSB cioè quello più a destra). Il peer interessato ad un download deve aggiornare periodicamente la propria conoscenza dello stato, mediante una esplicita richiesta al tracker, e assumiamo che tale aggiornamento avvenga ogni 60s.

IPP2P:RND <> IPT:3000
=> “FCHU”[4B].SessionID[16B].Filemd5_i[32B]
<= “AFCH”[4B].#hitpeer[3B].{IPP2P_ i[55B].PP2P_ i[5B].PartList_ i[8bitB][#part8]}(i=1..#hitpeer)

Download
Il peer interessato ad effettuare il download di un file ha identificato il file di interesse e conosce la situazione delle parti in ogni peer presente nella rete, identificato opportunamente dalla conoscenza di IPP2P e di PP2P ove i peer sono all’ascolto dall’atto del login. Sulla base della seconda fase della ricerca il peer è in grado di compilare una tabella in cui sono presenti le occorrenze delle parti. Il peer procede a: identificare le occorrenze di ogni parte, scartare le occorrenze delle parti che già possiede, ordinare le occorrenze in modo crescente, selezionare le parti con minore occorrenza, tra le parti selezionate con uguale occorrenza selezionare una parte casualmente, effettuare il download della parte selezionata da uno dei peer che la rende disponibile scelto a caso, aggiornare il tracker. Il sistema deve consentire il download parallelo di più parti in parallelo, specificando esplicitamente il numero delle parti parallelle trattabili.

Relativamente alla singola parte, questa viene suddivisa in chunk, e il download dal peer selezionato prevede l’indicazione del file mediante il proprio identificativo random univoco e l’indicazione della parte di interesse. Il numero dei chunk #chunk di cui è composta ogni singola parte è costante, con possibile e probabile eccezione dell’ultima. Al termine del download di una parte il peer comunica al tracker la nuova parte di cui è venuto in possesso e il tracker gli ritorna il numero delle parti di quel file che gli risultano il peer complessivamente possegga.

IPP2P:RND <> IPP2P:PP2P
=> “RETP”[4B].Filemd5_i[32B].PartNum[8B]
<= “AREP”[4B].#chunk[6B].{Lenchunk_i[5B].data[LB]}(i=1..#chunk)
 
IPP2P:RND <> IPT:3000
=> “RPAD”[4B].SessionID[16B].Filemd5_i[32B].PartNum[8B]
<= “APAD”[4B].#Part[8B]
Logout
Supponiamo che un peer che mette a disposizione un nuovo file rimanga presente nel sistema almeno fino a quando ogni sua parte sia stata copiata in almeno un altro peer. Con tale definizione non si considera una procedura di rimozione dei file messi in condivisione, che una volta aggiunti nel sistema vengono considerati patrimonio comune non rimovibile. Un peer può effettuare il logout e due sono le possibilità: non viene consentito con una risposta “NLOG” dal tracker in quanto i file messi a disposizione come sorgente non sono ancora divenuti patrimonio del sistema e nella risposta del tracker viene riportato il numero complessivo di parti già scaricate almeno una volta da altri peer della rete relativi ai file di cui il peer in logout è sorgente #partdown; viene consentito con risposta “ALOG” del tracker non rendendo più disponibili tutte le parti possedute dei vari file, ritornando il numero complessivo di parti #partown che sono in possesso del peer in logout su ogni file di cui è sorgente o che ha scaricato. Con il logout il peer smette di ascoltare sull’IP e la porta specificata per le azioni di P2P.

IPP2P:RND <> IPT:3000
=> “LOGO”[4B].SessionID[16B]
1<= “NLOG”[4B].#partdown[10B]
2<= “ALOG”[4B].#partown[10B]
