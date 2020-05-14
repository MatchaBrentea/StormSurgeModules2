import sys
from surgewarnings import*

if __name__=="__main__":
	#check for command line arguments:
	if len(sys.argv) == 1:
		print("use 'python "+sys.argv[0]+" help' for usage")
	elif len(sys.argv) == 2: 
		if sys.argv[1] == "help":
			print("usage: 'python "+sys.argv[0]+" <.shp file> <municipality filter> <fort.14 file> <maxele.63 file> <output directory> [radiusOffset]'")
		else:
			print("Unknown command: '"+sys.argv[1]+"'")
	else:
		radiusOffset = 1000 #default radius offset

		shape_file = sys.argv[1]
		filt = sys.argv[2]
		fort_14 = sys.argv[3]
		maxelev63 = sys.argv[4]	
		output_dir = sys.argv[5]			

		if len(sys.argv) > 6 : 
			try: 
				radiusOffset = int(sys.argv[6])
			except ValueError:
				print("input valid radiusOffset. Shifting to default radiusOffset 1000")


		warning = Warnings(shape_file,filt,fort_14,maxelev63,radiusOffset)
		warning.generateWarnings()
		warning.writeToFile(output_dir)
		print(datetime.datetime.now())
		