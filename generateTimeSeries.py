#!/usr/bin/python

import sys
import datetime
# import imp
# my_module = imp.load_compiled("ADCIRC_SCRIPT_LIB", "/home/gerry/Desktop/StormSurge2019/StormSurgeApp/surgeforcast/customScripts/__pycache__/ADCIRC_SCRIPT_LIB.cpython-36.pyc")
# from ADCIRC_SCRIPT_LIB import*

def read_fort14(file):
    f = open(file, 'r')
    print('Reading fort.14 file')
    AGRID = f.readline()[:-1]
    tmp = f.readline()[:-1].split()
    NE = int(tmp[0])
    NP = int(tmp[1])
    X = [
     'X']
    Y = ['Y']
    DP = ['DP']
    ETA = ['Elevation']
    for i in range(0, NP):
        tmp = f.readline()[:-1].split()
        X.append(float(tmp[1]))
        Y.append(float(tmp[2]))
        DP.append(float(tmp[3]))

    NM = [['NM(JE,1)', 'NM(JE,2)', 'NM(JE,3)']]
    for i in range(0, NE):
        tmp = f.readline()[:-1].split()
        NM.append([int(tmp[2]), int(tmp[3]), int(tmp[4])])

    f.close()
    return (
     AGRID, NE, NP, X, Y, DP, NM)


def read_maxelev63(file):
    f = open(file, 'r')
    ETA = [
     'Elevation']
    tmp = f.readline()[:-1].split()
    RUNDES = tmp[0]
    RUNID = tmp[1]
    AGRID = tmp[2]
    tmp = f.readline()[:-1].split()
    NP = int(tmp[1])
    tmp = f.readline()[:-1].split()
    NDSETSE = int(tmp[1])
    for j in range(0, NP):
        tmp = f.readline()[:-1].split()
        ETA.append(float(tmp[1]))

    return (
     RUNDES, RUNID, AGRID, NDSETSE, ETA)

'''*************************************************
|				time in 							|
**************************************************'''
start = datetime.datetime.now()
print(start)
'''*************************************************
|				parsing fort.14						|
**************************************************'''
print(sys.argv[1])
#read fort 14
AGRID,NE,NP,X,Y,DP,NM = read_fort14(sys.argv[1])

'''*************************************************
|				parsing fort.63						|
**************************************************'''
#open maxelev.63
file=sys.argv[2]
f=open(file,'r')


tmp=(f.readline()[:-1]).split()
RUNDES=tmp[0]
RUNID=tmp[1]
AGRID=tmp[2]

tmp=(f.readline()[:-1]).split()
NDSETSE=int(tmp[0])	#number of iteration*300
NP=int(tmp[1])


print ('number of elements: ',NE, '\tnumber of Nodes: ',NP)
'''*************************************************
|ready file for parsing and converting to col file	|
**************************************************'''

typhoonName=sys.argv[3]
eventId=sys.argv[4]

print ('writing to file '+sys.argv[5]+"timeseries"+typhoonName+"_"+eventId+"_0.txt")
if typhoonName!="" or eventId!="":
	g=open(sys.argv[5]+"timeseries"+typhoonName+"_"+eventId+"_0"+"_new.txt",'w')
else:
	g=open('temp.kml','w')

print(NDSETSE,NE,NP)

for i in range(0,NDSETSE):
	if i > 0 and i%288 == 0:
		print('end of day',str(int(i/288)))
		g.close()
		print ('writing to file '+sys.argv[5]+"timeseries"+typhoonName+"_"+eventId+"_"+str(int(i/288))+".txt")
		if typhoonName!="" and eventId!="":
			g=open(sys.argv[5]+"timeseries"+typhoonName+"_"+eventId+"_"+str(int(i/288))+"_new.txt",'w')
		else:
			g=open('temp.kml','w')

	f.readline()
	ETA=['Elevation']
	for j in range(1,NP+1):
		tmp=(f.readline()[:-1]).split()
		ETA.append(float(tmp[1]))

	for k in range(1,NE+1):
		color='#00ffffff'

		ave=max(ETA[NM[k][0]],ETA[NM[k][1]],ETA[NM[k][2]])
		if ave == -99999:
			color='#00ffffff'
		elif ave < -1 and ave > -99999:
			R=49
			B=255
			G=49
			color='#a0%02x%02x%02x' % (R,G,B)
		elif ave >= -1 and ave <0:
			R=49
			B=255
			G=49 + int(((ave-(-1))/(0-(-1)))*(206))
			color='#a0%02x%02x%02x' % (R,G,B)
		elif ave >= 0 and ave <1:
			R=49
			G=255
			B= 255 - int(((ave-0)/(1-0))*(206))
			color='#a0%02x%02x%02x' % (R,G,B)
		elif ave >= 1 and ave <2:
			B=49
			G=255
			R= 49 + int(((ave-1)/(2-1))*(206))
			color='#a0%02x%02x%02x' % (R,G,B)
		elif ave >=2 and ave < 3:
			R=255
			B=49
			G= 255 - int(((ave-2)/(3-2))*(206))
			color='#a0%02x%02x%02x' % (R,G,B)
		elif ave >=3 and ave <4:
			R=255
			B=49 + int(((ave-3)/(4-3))*(206))
			G=49
			color='#a0%02x%02x%02x' % (R,G,B)
		elif ave >=4:
			R=255
			B=255
			G=0
			color='#a0%02x%02x%02x' % (R,G,B)

		g.write(str(i)+','+color+'\n')

	del ETA


'''*************************************************
|				time out 							|
**************************************************'''
end = datetime.datetime.now()
print(end)
print("duration",end-start)