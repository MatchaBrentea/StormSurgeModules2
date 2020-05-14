import sys
sys.path.append(r"C:\Users\adminalpha\Desktop\UPStuff\Acads\1920A\ThesisRelated\StormSurge2019\Modules\surgewarnings")
from surgewarnings import*
from textwrap import dedent


if __name__=="__main__":

	programInfo= ''' 
					This program generates storm warnings for towns affected in a given province.
					It also generates notifications for towns beside affected towns (towns with storm surge warnings).
					Moroever, it also takes note of the earliest storm surge happened on those affacted towns.
					Three different shapefiles would be needed for this program. This are the administrative boundaries
					of different barangays, towns or cities and the administrative boundaries for each provinces.
					Another argument would also be passed, this would be the name of the province. 
					This would filter and narrow down all the boundaries and scopes that would be of interest to the user. 
					Different adcirc files are also required: 
					fort.14 (grid and boundary information file; this would be used to define the domain of the area/places of interest),
					maxele.63(the maximum elevations at each grid points in fort.14; this would be used for storm-surge prediction), 
					fort.15 (model parameter and boundary condition file; this file would be used for determining the reference time) 
					and fort.63 (elevation time series at all nodes; used for determining the earliest surges);
					output directory would also be required.
					Two files would be generated <province filter>.warnings and <province filter>.notifications. 
				'''

	#check for command line arguments:
	if len(sys.argv) == 1:
		print(dedent(programInfo))
		print("use 'python "+sys.argv[0]+" help' for usage")
	elif len(sys.argv) == 2: 
		if sys.argv[1] == "help":
			print("usage: 'python "+sys.argv[0]+" <.shp file for Munipalities/Cities> <.shp file for Barangay> <.shp file for Province> <province filter> <fort.14 file> <fort.15 file> <maxele.63 file> <fort.63 file> <neighborfiles directory> <output directory> [radiusOffset]'")
		else:
			print("Unknown command: '"+sys.argv[1]+"'")
	else:
		radiusOffset = 1000 #default radius offset

		shape_file = sys.argv[1]
		shape2_file = sys.argv[2]
		shape3_file = sys.argv[3]
		filt = sys.argv[4]
		fort_14 = sys.argv[5]
		fort_15 = sys.argv[6]
		maxelev63 = sys.argv[7]	
		fort_63 = sys.argv[8]	
		neighborfiles_dir = sys.argv[9]	
		output_dir = sys.argv[10]	
	

		#earliestSurge=EarliestSurgeLocator(fort_14,fort_15,fort_63,shape2_file,[filt])
		#earliestSurge.getEarliestSurge()
		#earliestSurge.getBarangayOfEarliestSurge(shape_file,output_dir)

		if len(sys.argv) > 11 : 
			try: 
				radiusOffset = int(sys.argv[11])
			except ValueError:
				print("input valid radiusOffset. Shifting to default radiusOffset 1000")


		warning = Warnings(shape_file,shape2_file,shape3_file,filt,fort_14,fort_15,maxelev63,fort_63,radiusOffset,neighborfiles_dir)
		warning.getEarliestSurge()
		warning.generateWarnings()
		warning.getBarangayOfEarliestSurge(output_dir)
		warning.writeToFile(output_dir)
		#print(warning.warnings)
		warning.writeToFile(output_dir)
		print(datetime.datetime.now())	