import os

pathdir = '/home/riccardo/Scrivania/FileProgetto/'
pathtemp = '/home/riccardo/Scrivania/FileProgetto/Temp/'
lenpart=25000
nomeFComp= 'Mona.jpg'
numpart = 0

lenfile=os.path.getsize(pathdir + nomeFComp)
respart=lenfile%lenpart

if(respart>0):
	numpart=int(lenfile/lenpart)+1
else:
	numpart=int(lenfile/lenpart)


fcomp = open(pathdir + nomeFComp, "rb")
for i in range (1, numpart+1):
	if(i==numpart and respart>0):
		buffer = fcomp.read(respart)
	else:
		buffer = fcomp.read(lenpart)
	with open(pathtemp + nomeFComp + str(i), "ab") as myfile:
		myfile.write(buffer)

fcomp.close()







