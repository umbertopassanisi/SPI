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
import cx_Oracle
import argparse
import DBConnectCheck


#gestion des variables, elles seront recues sous options.dest (options.fileinput, options.login ...)

parser 							= argparse.ArgumentParser()
parser.add_argument("t",help	="table")
parser.add_argument("db1",help	="db(oracle/Mysql)1")
parser.add_argument("s1",help	="schema1")
parser.add_argument("db2",help	="db(oracle/Mysql)2")
parser.add_argument("s2",help	="schema2")
args 							= parser.parse_args()

def lectureTableMatrix(start, cursor, table):
	dicTable	=	{}
	nbrRec		=	0
	try:
			cursor.execute("select * from "+table)
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		indicator			=	ligne[start+0].strip()  #
		country				=	ligne[start+1].strip()  #
		yyyy				=	str(ligne[start+2])     #
		codeprod			=	ligne[start+3].strip()  #
		vector				=	ligne[start+4].strip()  #
		cle					=	indicator+'#'+country+'#'+yyyy+'#'+codeprod
		if	dicTable.has_key(cle):
			print 'table ', table, ' doublon : ', cle, ' vector = ',dicTable[cle]
			print 'table ', table, ' doublon : ', cle, ' vector = ',vector
		dicTable[cle]		=	vector
		nbrRec				+=1
	return dicTable, nbrRec
def lectureTableGeo(start, cursor, table):
	dicTable	=	{}
	nbrRec		=	0
	try:
			cursor.execute("select * from indicators"+table)
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		indicator			=	ligne[start+0].strip()  #
		country				=	ligne[start+1].strip()  #
		yyyy				=	str(ligne[start+2])     #
		codeprod			=	ligne[start+3].strip()  #
		typeprod			=	ligne[start+4].strip()  #
		vector				=	ligne[start+5].strip()  #
		partner				=	ligne[start+6].strip()  #
		cle					=	indicator+'#'+country+'#'+yyyy+'#'+codeprod+'#'+typeprod+'#'+partner
		if	dicTable.has_key(cle):
			print 'table ', table, ' doublon : ', cle, ' vector = ',dicTable[cle]
			print 'table ', table, ' doublon : ', cle, ' vector = ',vector
		dicTable[cle]		=	vector
		nbrRec				+=1
	return dicTable, nbrRec
def lectureTable(start, cursor, table):
	dicTable	=	{}
	nbrRec		=	0
	try:
			cursor.execute("select * from indicators"+table)
	except:
			#error, = exc.args
			#print "code = ", error.code, " message = ", error.message
			print ("error read table = ", table)
			return
	for	ligne in cursor.fetchall():
		indicator			=	ligne[start+0].strip()  #
		country				=	ligne[start+1].strip()  #
		yyyy				=	str(ligne[start+2])     #
		codeprod			=	ligne[start+3].strip()  #
		typeprod			=	ligne[start+4].strip()  #
		vector				=	ligne[start+5].strip()  #
		cle					=	indicator+'#'+country+'#'+yyyy+'#'+codeprod+'#'+typeprod
		if	dicTable.has_key(cle):
			print 'table ', table, ' doublon : ', cle, ' vector = ',dicTable[cle]
			print 'table ', table, ' doublon : ', cle, ' vector = ',vector
		dicTable[cle]		=	vector
		nbrRec				+=1
	return dicTable, nbrRec

def lecture(table, db, schema):
	db.lower()
	schema.lower()
	dicTable			=	{}
	#open DB
	connectionIn = DBConnectCheck.connectionDB(db, schema)
	cursor 		= 	connectionIn.cursor()
	if	(db == 'oracle'):
		start =	0
	else:
		start = 1
	#read DB
	if		table == 'matrix':
			dicTable, nbrRec	=	lectureTableMatrix(start, cursor, table)
	elif	table == 'tradegeo':
			dicTable, nbrRec	=	lectureTableGeo(start, cursor, table)
	else:
			dicTable, nbrRec	=	lectureTable(start, cursor, table)
	#close DB

	connectionIn.close()

	return dicTable, nbrRec

def checkDiffTable(dicTable1, dicTable2, db1, schema1, db2, schema2):
	print 'CHECK difference between ', db1, schema1 , ' and ', db2, schema2
	keyTable1		=	dicTable1.keys()
	keyTable1.sort()
	nbrDiff			=	0
	nbrDiffVal		=	0
	for key1 in keyTable1:
		vector1		=	dicTable1[key1]
		try:
			vector2	=	dicTable2[key1]
		except:
			nbrDiff	+=	1
			print 'record with key ',key1,' EXIST in ',db1, schema1," NOT in ", db2, schema2
			continue #next iteration on the loop
		if	vector1 !=	vector2:
			print 'Different value in key :', key1
			print 'value in ',db1, schema1,' = ', vector1
			print 'value in ',db2, schema2,' = ', vector2
			nbrDiffVal	+=	1
			
	print 'CHECK difference between ', db2, schema2 , ' and ', db1, schema1
	keyTable2		=	dicTable2.keys()
	keyTable2.sort()
	nbrDiff2		=	0
	for key2 in keyTable2:
		vector2		=	dicTable2[key2]
		try:
			vector1	=	dicTable1[key2]
		except:
			nbrDiff2+=	1
			print 'record with key ',key2,' EXIST in ',db2, schema2," NOT in ", db1, schema1
			continue #next iteration on the loop
	
	print nbrDiff,'nbr record are on ',db1, schema1, ' and not in ',db2, schema2
	print nbrDiff2,'nbr record are on ',db2, schema2, ' and not in ',db1, schema1
	print 'nbr record with a different value = ',nbrDiffVal
def checkTable(table, db1, schema1, db2, schema2):
	print ('CHECK TABLE ', table, ' BETWEEN ', db1, schema1, ' AND ', db2, schema2)
	dicTable1		=	{}
	dicTable2		=	{}
	nrec1			=	0
	nrec2			=	0

	dicTable1,nrec1		=	lecture(table, db1, schema1)
	dicTable2,nrec2		=	lecture(table, db2, schema2)

	checkDiffTable(dicTable1, dicTable2, db1, schema1, db2, schema2)
	print ('For table ', table, ' in ', db1, schema1, ' nbr rec in dictionary = ', len(dicTable1),' nbr rec in ORACLE = ', nrec1)
	print ('For table ', table, ' in ', db2, schema2, ' nbr rec in dictionary = ', len(dicTable2),' nbr rec in ORACLE = ', nrec2)


 
#-------------------------------------------------------------------------------------------------

checkTable(table=args.t, db1=args.db1, schema1=args.s1, db2=args.db2, schema2=args.s2)
