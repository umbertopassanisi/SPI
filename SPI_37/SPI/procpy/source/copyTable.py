#-------------------------------------------------------------------------------------------------
# CHECK TABLE : on test la valeur de chaque meme table entre deux schema Oracle 
# par exemple entre TEST et PROD
# -----------------------------
# parametres : argv[]
# sys.argv[0] = nom du programme
# sys.argv[1] = nom du fichier input
# t (table) = nom d'une table oracle existante
# s1,s2(schema) = DEV, TEST ou PROD uniquement
# attention : les parametres sont en string, il est parfois necessaire de les convertir en integer
# r@g 19/6/2006
#-------------------------------------------------------------------------------------------------

import sys
import argparse
import time
import DBAccessCopy
#gestion des variables, elles seront recues sous options.dest (options.fileinput, options.login ...)

parser 							= argparse.ArgumentParser()
parser.add_argument("t",help	="table")
parser.add_argument("s1",help	="schema1")
parser.add_argument("s2",help	="schema2")
args 							= parser.parse_args()

def copyTable(table, schemaIn, schemaOut):
	dicTable	=	{}
	nbrRecIn	=	0
	if	table == 'matrix':
		tableOracle = 	table
	else:
		tableOracle = 	'indicators' + table
	
	#This read-write attribute specifies the size of the statement cache. 
	#This value can make a significant difference in performance (up to 100x) 
	#if you have a small number of statements that you execute repeatedly.

	connectionIn, connectionOut = DBAccessCopy.connectionDB(schemaIn, schemaOut)
	connectionOut.stmtcachesize = 200
	cursorIn 		= connectionIn.cursor()
	cursorOut 		= connectionOut.cursor()

	DBAccessCopy.truncateTable(cursorOut,tableOracle)
	timeStart=time.time()
	print 'avant lecture table', time.ctime() 
	cursorIn	=	DBAccessCopy.lectureTableOracle(cursorIn,tableOracle)
	timeRead=time.time()
	print 'apres lecture table ', time.ctime(), ' temps en sec READ = ', timeRead-timeStart
	print 'debut ecriture table', time.ctime()
	timeStartCommit =	time.time()
	timeStartT	=	time.time()
	nbrRecOut	=	0
	nbrcommit	=	0
	nbrRecOutT	=	0
	for	ligne in cursorIn.fetchall():
		nbrRecOut = DBAccessCopy.insertTable(cursorOut,connectionOut,tableOracle,ligne)
	timeWrite=time.time()
	print 'fin ecriture table', time.ctime(), ' temps en sec WRITE = ', timeWrite-timeRead
	print 'temps total en sec = ', timeWrite-timeStart
	connectionOut.commit()
	connectionOut.close()
	print 'nbr rec read', cursorIn.rowcount, ' nbr rec write ', nbrRecOut, ' for table ', tableOracle
	
def selectCopyTable(table, schema1, schema2):
	print 'COPY TABLE ', table, ' FROM ', schema1, ' TO ', schema2
	copyTable(table, schema1, schema2)
 
#-------------------------------------------------------------------------------------------------

selectCopyTable(table=args.t, schema1=args.s1, schema2=args.s2)
