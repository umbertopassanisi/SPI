import 	re
import	cx_Oracle
import 	DBConnect

cursor 			= 	DBConnect.connection.cursor()
nbrcommit		=	0

def lectureNation(nation):
	try:
			cursor.execute("select code_iso3, code_iso2 name from nation")
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		cle 				= 		ligne[0].strip()  #la cle est code iso3
		nation[cle]         =		ligne[1].strip()  #le code code iso2
	return nation
def lectureNationEurostat(nation=''):
	nation	= {}
	try:
			cursor.execute("select code_eurostat, code_iso2 from nation where code_eurostat != ' ' and defaut_pays = 'Y' order by code_eurostat")
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		cle 				= 		ligne[0].strip()  #la cle est code eurostat
		nation[cle]         =		ligne[1].strip()  #le code code iso2
	return nation
def lectureNationPartner(nation=''):
	nation	= {}
	try:
			cursor.execute("select code_eurostat, code_iso2 from nation where code_eurostat != ' ' and partner = 'Y' order by code_iso2")
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		cle 				= 		ligne[0].strip()  #la cle est code eurostat
		nation[cle]         =		ligne[1].strip()  #le code code iso2
	return nation	
def lectureNationUN(nation):
	try:
			cursor.execute("select code_un, code_iso2 from nation where code_un > 0 and world_manufacture = 'Y' order by code_un")
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		cle 				= 		str(ligne[0]).strip()  		  #la cle est code UN
		nation[cle]         =		ligne[1].strip()  			  #le code code iso2
	return nation
def lectureNationService():
	nation	=	{}
	try:
			cursor.execute("select code_iso2, code_eurostat, world_service from nation where world_service = 'Y' order by code_iso2")
	except	cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		cle 				= 		ligne[0].strip()  		  #la cle code iso2
		nation[cle]         =		ligne[0].strip()  		 #le contenu code iso2 
	return nation
def lectureSector():
	sector	=	{}
	try:
			cursor.execute("select code, ordre from sector order by ordre")
	except	cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		cle 				= 		ligne[0].strip()  		  #la cle est le code sector eurostat
		sector[cle]         =		ligne[0].strip()  		  #le contenu est le code sector eurostat
	return sector			
def lectureSectorWto(eurostat=0):
	sector	=	{}
	try:
			cursor.execute("select code, codewto, ordre from sector where codewto != '0' order by ordre")
	except	cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	if	eurostat:#pour traiter les sector avec input Eurostat
		for	ligne in cursor.fetchall():
			cle 				= 		ligne[0].strip()#la cle est le code sector wto
			sector[cle]         =		ligne[0].strip()#le contenu est le code sector eurostat	
	else:#pour traiter les sector avec input WTO		
		for	ligne in cursor.fetchall():
			cle 				= 		ligne[1].strip()#la cle est le code sector wto
			sector[cle]         =		ligne[0].strip()#le contenu est le code sector eurostat
	return sector		
def lectureNace1(dicNace,compteEurostat):
	try:
		cursor.execute("select code,"+compteEurostat+" from nace1 where "+compteEurostat+" =1 order by code")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 
		newkey  	= 	re.sub('[0-9]','',cle) # on elemine les chiffres on ne garde que les domaines, H ou DL				
		dicNace[cle]=	newkey  # on prend le premier ou les deux premiers carac.
	return dicNace
def lectureNace2(dicNace,compteEurostat):
	try:
		cursor.execute("select code,"+compteEurostat+" from nace2 where "+compteEurostat+" =1 order by code")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 
		newkey  	= 	re.sub('[0-9]','',cle) # on elemine les chiffres on ne garde que les domaines, H ou DL				
		dicNace[cle]=	newkey  # on prend le premier ou les deux premiers carac.
	return dicNace 	
def lectureNace1Total(dicNaceTotal):
	try:
		cursor.execute("select code from nace1total order by code")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 				
		dicNaceTotal[cle]=	ligne[0].strip()  # 
	return dicNaceTotal
def lectureNace2Total(dicNaceTotal):
	try:
		cursor.execute("select code from nace2total order by code")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 				
		dicNaceTotal[cle]=	ligne[0].strip()  # 
	return dicNaceTotal
	
def lectureNaceNE(dicNaceNe,nomenclature,compteEurostat):
	try:
		cursor.execute("select code from "+nomenclature+" where "+compteEurostat+" = 0 order by code")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 				
		dicNaceNe[cle]=	ligne[0].strip()  # 
	return dicNaceNe
	
def lectureCpaNE(nomenclature,compte):
	dicNe	=	{}
	try:
		cursor.execute("select code from "+nomenclature+" where "+compte+" = 0 order by code")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 				
		dicNe[cle]	=	ligne[0].strip()  # 
	return dicNe
	
def lectureSectorNE(nomenclature):
	dicNe	=	{}
	try:
		cursor.execute("select code,codewto ordre from sector where codewto = '0' order by ordre")
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		cle 		= 	ligne[0].strip()  #la cle est code 				
		dicNe[cle]	=	ligne[0].strip()  # 
	return dicNe		
	
def lectureInfo():
	try:
			cursor.execute("select * from info")
	except cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		dateStart			= 	  ligne[2] 
		dateEnd             =     ligne[3]        
	return dateStart, dateEnd 

def majDBtable(tableName,indicator,country,yyyy,codeprod,typeprod,vector): 
	insertTable	= "insert into indicators"+tableName+" (indicator,country,yyyy,codeprod,typeprod,vector) values\
	('"+indicator+"','"+country+"',"+yyyy+",'"+codeprod+"','"+typeprod+"','"+vector+"')"
	#print insertTable

	try:        
		cursor.execute(insertTable)
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return

def majDBtableGeo(tableName,indicator,country,yyyy,codeprod,typeprod,vector,partner):
	global nbrcommit
	nbrcommit += 1
	insertTable	= "insert into indicators"+tableName+" (indicator,country,yyyy,codeprod,typeprod,vector,partner) values\
	('"+indicator+"','"+country+"',"+yyyy+",'"+codeprod+"','"+typeprod+"','"+vector+"','"+partner+"')"
	#print insertTable
	try:      
		cursor.execute(insertTable)
		if	nbrcommit 	== 1000:
			nbrcommit	= 0
			DBConnect.connection.commit()
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return

