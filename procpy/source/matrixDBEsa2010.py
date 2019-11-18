#-------------------------------------------------------------------------------------------------
# SPI
# upload matrix 
# r@g 01/07/2016
#-------------------------------------------------------------------------------------------------

import sys
import ameco
import glob
import cx_Oracle
import DBConnect
from   DBAccess import lectureInfo

# variables globales recues en parametre
# fichier = fichier input a traiter = resultat de readExcelNRR.PY

#fichier = sys.argv[1]


dirWork 		= sys.argv[1]
dirUse          = dirWork 

dirInput        = dirUse           +'\\Output'
dirLog          = dirUse           +'\\Log'
fileLog         = open(dirLog      + '\\matrixDBEsa2010.log', 'w')

#selection des fichiers products by products
filesInput		= glob.glob(dirInput+'\\matrix\\matrixDB*Esa2010.csv')
#selection des fichiers industries by industries
filesInputIndus	= glob.glob(dirInput+'\\matrix\\matrixDB*Esa2010I.csv')

cursor         = DBConnect.connection.cursor()

def openDbTable():
	# Table Oracle, on ouvre et on vide la table    
	truncateTable		=		"truncate table matrix"        
	cursor.execute(truncateTable)
       
def majDB(cursor,indicator,country,yyyy,codeprod,vector):                 
	insertTable	= "insert into matrix (indicator,country,yyyy,codeprod,vector) values\
	('"+indicator+"','"+country+"',"+yyyy+",'"+codeprod+"','"+vector+"')"
	try:
		#print insertTable
		cursor.execute(insertTable)
	except DBConnect.cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
        
def closeDbTable():
	DBConnect.connection.commit()
	DBConnect.connection.close()  
                      
def lectureInput(fichier):
	fileLog.write('updated product file'+str(fichier)+'\n')
	fileInput       = open(fichier,'r') 
	rec             = []
	serie           = {} 
	#Cet ordre est garanti par le programme de creation des matrices
	#des fichiers csv 
	#exemple pour matrixInpsh.py
	#New;Cost structure of industries for;inpsh;AT;2008
	#Code;CPA_A01,CPA_A02,CPA_A03,CPA_B,CPA_C10-C12,CPA_C13-C15,...,CPA_TOTAL
	#B1G;42.6263748665,45.5799972058,32.2608949985,51.4321167338,24.8088352118,...,46.6250766661
	for	l in fileInput: 
		rec             = l.split(';')
		codeprod        = rec[0].strip()
		if	codeprod   == 'New':
			indicator  =  rec[2].strip() 
			country    =  rec[3].strip()
			yyyy       =  rec[4].strip()
			continue
		if	codeprod   == 'Code':
			vector     =  rec[1].strip().replace('CPA_','')
		else:
			vector     =  rec[1].strip()                  
		majDB(cursor,indicator,country,yyyy,codeprod,vector)
		 
	fileInput.close()       
#-------------------------------------------------------------------------------------------------
# traitement Industries by Industries
# on traite uniquement la Finlande et le Nederlands
def lectureInputIndus(fichier):
	fileLog.write('updated industry file'+str(fichier)+'\n')
	fileInput       = open(fichier,'r') 
	rec             = []
	serie           = {} 
	for	l in fileInput: 
		rec             = l.split(';')
		codeprod        = rec[0].strip()
		if	codeprod   == 'New':
			indicator  =  rec[2].strip() 
			country    =  rec[3].strip()
			yyyy       =  rec[4].strip()
			continue
		if	codeprod   == 'Code':
			vector     =  rec[1].strip().replace('CPA_','')
		else:
			vector          =  rec[1].strip()
		if	country == 'FI' or country == 'NL':
			majDB(cursor,indicator,country,yyyy,codeprod,vector) 
	fileInput.close()       
#-------------------------------------------------------------------------------------------------

openDbTable()
for	fichier in filesInput :
	lectureInput(fichier)
for	fichier in filesInputIndus :
	lectureInputIndus(fichier) 
closeDbTable()     
fileLog.close()