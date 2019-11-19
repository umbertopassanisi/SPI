#
# conversion des fichiers input matrice
# naio_10_cp1750.tsv devient
# naio_10_cp1750.csv
# les codes agregats cpa_(x)10_12 deviennent cpa_(x)10_(x)12
# on rajoute la lettre sur le deuxieme code pour rester
# compatible avec la codification dans les fichiers nama
# attention dans ce fichier l'ordre les colonnes sont interverties
# on les remets comme dans naio_10_cp1700
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

fichierCSVIndus		=  dirInput		+ '\\naio_10_cp1750.tsv'
fichierOutputIndus	=  dirInput		+ '\\naio_10_cp1750.csv'

fileLog         =  open(dirLog  + '\\matrixEsa2010Naio.log', 'w')

def ajoutLetter(lstInput,separateur):
	outputLst = ''
	outputLst = lstInput[0]+separateur+lstInput[0][0]+lstInput[1]	
	return outputLst
def	traitementLigne(unit,flow,col,row,geoTime,fileOutput):
	geoTime			= re.sub(r'[a-z]', '', geoTime)
	geoTime			= re.sub(r'[:]', '0', geoTime)
	newCol			= col
	newRow			= row
	colTiret		= col.split('-')
	colUnder		= col.split('_')
	rowTiret		= row.split('-')
	rowUnder		= row.split('_')
	if	(len(colTiret) > 1) and ((colTiret[1]).isdigit()):
		newCol = ajoutLetter(colTiret,'-')
	if	(len(colUnder) > 1) and ((colUnder[1]).isdigit()):
		newCol = ajoutLetter(colUnder,'_')		
	if	(len(rowTiret) > 1) and ((rowTiret[1]).isdigit()):
		newRow = ajoutLetter(rowTiret,'-')
	if	(len(rowUnder) > 1) and ((rowUnder[1]).isdigit()):
		newRow = ajoutLetter(rowUnder,'_')
	newLine	= unit+','+flow+','+newCol+','+newRow+','+geoTime
	fileOutput.write(newLine)
def traitementFichierCSVIndus(fichierCSV,fichierOutput):
	fichierInput	= open(fichierCSV,'r')
	fileOutput		= open(fichierOutput,'w')
	recMeta			= fichierInput.readline() #1er rec avec les meta
	ligneMeta       = recMeta.split(',')
	fileOutput.write('unit,stk_flow,induse,prod_na,'+ligneMeta[4])
	#unit,stk_flow,induse,prod_na,geo\time = naio_10_cp1700
	#unit,prod_na,induse,stk_flow,geo\time = naio_10_cp1750
	for ligneCSV in fichierInput:
		ligne           = ligneCSV.split(',')       
		unit            = ligne[0].strip()
		flow            = ligne[3].strip()
		prod_na         = ligne[1].strip()
		induse          = ligne[2].strip()
		geoTime			= ligne[4]
		traitementLigne(unit,flow,induse,prod_na,geoTime,fileOutput)
	fichierInput.close()
	fileOutput.close()

traitementFichierCSVIndus(fichierCSVIndus,fichierOutputIndus)
fileLog.close()
            