#!/usr/bin/python

import sys
import shapefile
import matplotlib.path as mpltPath
from ADCIRC_SCRIPT_LIB import*

'''*************************************************
|				parsing fort.14						|
**************************************************'''
print(sys.argv[1])
#read fort 14
AGRID,NE,NP,X,Y,DP,NM = read_fort14(sys.argv[1])

'''*************************************************
|				parsing maxele.64					|
**************************************************'''
#read for 63
RUNDES,RUNID,AGRID,NDSETSE,ETA = read_maxelev63(sys.argv[2])
print(ETA[1])

print ('number of elements: ',NE, '\tnumber of Nodes: ',NP)


'''*************************************************
|				load shapefile						|
**************************************************'''
sf =  shapefile.Reader(sys.argv[6])
fields = sf.fields[1:] 
field_names = [field[0] for field in fields]

for r in sf.shapeRecords():
	atr = dict(zip(field_names,r.record))
	geom = r.shape.points
	parts = r.shape.parts		

	if atr['NAME_1'] == sys.argv[7]: 
		paths=[]
		insides=[]
		for i in range(0,len(parts)):
			if(i < len(parts) - 1):
				path = mpltPath.Path(geom[parts[i]:parts[i+1]])		
				inside=path.contains_points([(X[j],Y[j]) for j in range(1,len(X))])
				paths.append(path)
				insides.append(inside)
			else:
				path = mpltPath.Path(geom[parts[i]:len(geom)])		
				inside=path.contains_points([(X[j],Y[j]) for j in range(1,len(X))])				
				paths.append(path)
				insides.append(inside)

		'''*************************************************
		|		ready file for converting to kml file		|
		**************************************************'''

		typhoonName=sys.argv[3]
		eventId=sys.argv[4]

		print ('writing to file '+sys.argv[5]+"maxelev_"+typhoonName+"_"+eventId+".kml")
		if typhoonName!="" or eventId!="":
			g=open(sys.argv[5]+"maxelev_"+typhoonName+"_"+eventId+".kml",'w')
		else:
			g=open('temp.kml','w')


		g.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		g.write('<kml xmlns="http://earth.google.com/kml/2.0"> <Document>\n')
		for k in range(1,NE+1):
			print(NM[k][0],NM[k][1],NM[k][2])

			for inside in insides:

				if (inside[NM[k][0]-1]==True or inside[NM[k][1]-1]==True or inside[NM[k][2]-1]==True):
					color='#00ffffff'
					ave=max(ETA[NM[k][0]],ETA[NM[k][1]],ETA[NM[k][2]])
					
					if ave < -1 and ave != -99999:
						R=49
						B=255
						G=49
						color='#a0%02x%02x%02x' % (B,G,R)	
					elif ave >= -1 and ave <0:
						R=49
						B=255
						G=49 + int(((ave-(-1))/(0-(-1)))*(206))
						color='#a0%02x%02x%02x' % (B,G,R)
					elif ave >= 0 and ave <1:
						R=49
						G=255
						B= 255 - int(((ave-0)/(1-0))*(206))
						color='#a0%02x%02x%02x' % (B,G,R)			
					elif ave >= 1 and ave <2:
						B=49
						G=255
						R= 49 + int(((ave-1)/(2-1))*(206))
						color='#a0%02x%02x%02x' % (B,G,R)
					elif ave >=2 and ave < 3:
						R=255
						B=49
						G= 255 - int(((ave-2)/(3-2))*(206))
						color='#a0%02x%02x%02x' % (B,G,R)
					elif ave >=3 and ave <4:
						R=255
						B=49 + int(((ave-3)/(4-3))*(206))
						G=49
						color='#a0%02x%02x%02x' % (B,G,R)				
					elif ave >=4:
						R=255
						B=255
						G=0
						color='#a0%02x%02x%02x' % (B,G,R)
					g.write('<Placemark>\n')
					g.write(' <Polygon> <outerBoundaryIs>  <LinearRing>  \n')
					g.write('  <coordinates>\n')
					g.write('     '+str(X[NM[k][0]])+','+str(Y[NM[k][0]])+'\n')	
					g.write('     '+str(X[NM[k][1]])+','+str(Y[NM[k][1]])+'\n')	
					g.write('     '+str(X[NM[k][2]])+','+str(Y[NM[k][2]])+'\n')	
					g.write('  </coordinates>\n')				
					g.write(' </LinearRing> </outerBoundaryIs> </Polygon>\n')
					g.write(' <Style>\n')
					g.write('  <PolyStyle>\n')
					g.write('   <color>'+color+'</color>\n')
					g.write('  <outline>0</outline>\n')
					g.write('  </PolyStyle>\n')
					g.write(' </Style>\n')
					g.write('</Placemark>\n')

		del ETA
		g.write('</Document> </kml>')
		g.close()