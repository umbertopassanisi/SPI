#
# conversion des fichiers input matrice
# naio_10_cp1700.tsv devient
# naio_10_cp1700.csv
# les codes agregats cpa_x10_12 deviennent cpa_x10_x12
# on rajoute la lettre sur le deuxieme code pour rester
# compatible avec la codification dans les fichiers nama
#
import  sys
import  glob
import  re
from    numpy import *
from    numpy.linalg import inv

dirWork         =  sys.argv[1]

dirUse          =  dirWork

dirInput        =  dirUse           +'\\Input\\tsv\\nace2'
dirOutput       =  dirUse           +'\\Output\\matrix'
dirLog          =  dirUse           +'\\Log'

fichierCSV  	=  dirInput	+ '\\naio_10_cp1700.tsv'
fichierOutput	=  dirInput	+ '\\naio_10_cp1700.csv'

fileLog         =  open(dirLog      + '\\matrixEsa2010Naio.log', 'w')

def traitementFichierCSV():
	fichierInput	= open(fichierCSV,'r')
	fileOutput		= open(fichierOutput,'w')
	recMeta			= fichierInput.readline() #1er rec avec les meta
	fileOutput.write(recMeta)
	#unit,stk_flow,induse,prod_na,geo\time
	for ligneCSV in fichierInput:
		ligne           = ligneCSV.split(',')       
		unit            = ligne[0].strip()
		flow            = ligne[1].strip()
		col             = ligne[2].strip()
		row             = ligne[3].strip()
		geoTime			= ligne[4]
		geoTime			= re.sub(r'[a-z]', '', geoTime)
		geoTime			= re.sub(r'[:]', '0', geoTime)
		newCol			= col
		newRow			= row
		if  (col[:3] == 'CPA')and (len(col) > 8):
			newCol = col[:8] + col[4] + col[8:]
		if  (row[:3] == 'CPA')and (len(row) > 8):
			newRow = row[:8] + row[4] + row[8:]
		newLine	= unit+','+flow+','+newCol+','+newRow+','+geoTime
		fileOutput.write(newLine)
	fichierInput.close()
	fileOutput.close()

traitementFichierCSV()
fileLog.close()
            