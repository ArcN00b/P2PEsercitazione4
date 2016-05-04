import os

pathdir = '/home/riccardo/Scrivania/FileProgetto/'
pathtemp = '/home/riccardo/Scrivania/FileProgetto/Temp/'
nomeFComp= 'Mona.jpg'
nomeFDim= 'MonaTest.jpg'

fCompleto = open(pathdir + nomeFComp, "wb")
fCompleto.close()

lenfile=os.path.getsize(pathdir + nomeFDim)
respart=lenfile%lenpart

if(respart>0):
	numpart=int(lenfile/lenpart)+1
else:
	numpart=int(lenfile/lenpart)

for i in range (1,numpart+1):
	fParte = open(pathtemp + nomeFComp + str(i), "rb")
	buffer = fParte.read()
	with open(pathdir + nomeFComp, "ab") as myfile:
		myfile.write(buffer)
	fParte.close()



