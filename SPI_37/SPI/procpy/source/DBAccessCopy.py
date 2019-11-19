import time
import cx_Oracle

nbrcommit		=	0
nbrRecOut		=	0
timeStart		=	time.time()

def connectionDB(schemaIn, schemaOut):
	schemaIn.lower()
	schemaOut.lower()
	try:
		login 			= 'spi'
		pwd				= 'wadkn23_'
		db				= 'IN1UECFD'
		connectDBDev	=	login + "/" + pwd + "@" + db
		db				= 'IN1UECFT'
		connectDBTest	=	login + "/" + pwd + "@" + db
		db				= 'IN1UECFA'
		connectDBProd	=	login + "/" + pwd + "@" + db
		#select IN database
		if	schemaIn	==	'dev':
			connectionIn=	cx_Oracle.Connection(connectDBDev)
		elif schemaIn	==	'test':
			connectionIn=	cx_Oracle.Connection(connectDBTest)
		elif schemaIn	==	'prod':
			connectionIn=	cx_Oracle.Connection(connectDBProd)
		#select OUT database
		if	schemaOut	==	'dev':
			connectionOut=	cx_Oracle.Connection(connectDBDev)
		elif schemaOut	==	'test':
			connectionOut=	cx_Oracle.Connection(connectDBTest)
		elif schemaOut	==	'prod':
			connectionOut=	cx_Oracle.Connection(connectDBProd)
			
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
	return connectionIn, connectionOut

def truncateTable(cursor,tableOracle):
	try:
			cursor.execute("truncate table "+tableOracle)
	except	cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	return cursor
def lectureTableOracle(cursor,tableOracle):
	cursor.arraysize = 1000
	try:
			cursor.execute("select * from "+tableOracle)
	except	cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	return cursor
	
def insertTable(cursor,connection,tableOracle,ligne):
	global nbrcommit
	global nbrRecOut
	global timeStart
	timeStartCommit =	time.time()
	cursor.arraysize = 1000
	insertTable	= "insert into "+tableOracle+" values "+str(ligne)
	try:
		nbrRecOut			+=1
		nbrcommit			+=1
		cursor.execute(insertTable)
		if	nbrcommit 	== 10000:
			nbrcommit	= 0
			connection.commit()
			timeCommit =	time.time()
			print ' temps en sec pour 10000 commit ', timeCommit-timeStartCommit
			print ' temps en sec depuis le debut ', timeCommit-timeStart
			timeStartCommit =	time.time()
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	return nbrRecOut
