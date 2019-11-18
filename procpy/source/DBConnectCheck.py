import time
import cx_Oracle
import DBAccessCopy

def connectionDB(schemaIn):
	schemaIn.lower()
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
			
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
	return connectionIn
