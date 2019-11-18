import  cx_Oracle

def	connectionDB():
	login = 'spi'
	pwd   = 'wadkn23_'
	#base dev digit
	#db    = 'IN1UECFD'
	#base test digit
	#db    = 'IN1UECFT'
	#base PROD digit
	db    = 'IN1UECFA'
	connectDB			=	login + "/" + pwd + "@" + db
	return	connectDB
		
def closeDB():
	connection.commit()
	connection.close()

connectDB			=	connectionDB()
connection			=	cx_Oracle.Connection(connectDB)