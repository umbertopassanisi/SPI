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
    nation = {}
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
		cle 				= 		ligne[0].strip()	#la cle code iso2
		nation[cle]			=		ligne[0].strip()	#le contenu code iso2 
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
  
def defListNationIso2():
    nation = []
    try:
            cursor.execute("select code_eurostat, code_iso2 from nation where code_eurostat != ' ' and defaut_pays = 'Y' order by code_eurostat")
    except cx_Oracle.IntegrityError, exc:
            error, = exc.args
            print "code = ", error.code, " message = ", error.message
            return
    for    ligne in cursor.fetchall():
        nation.append(ligne[1])
    return nation
    
def lectureCpa(cpa):
	dicCpa	=	{}
	dicCpaN3=	{}
	try:
			cursor.execute("select * from "+cpa+" order by ordre")
	except	cx_Oracle.IntegrityError, exc:
			error, = exc.args
			print "code = ", error.code, " message = ", error.message
			return
	for	ligne in cursor.fetchall():
		code				=		ligne[0].strip()
		niveau				=		ligne[2]
		node				=		ligne[3].strip()
		if		niveau == 1:
				codeN1								=	code
				dicCpa[codeN1]						=	code
		elif	niveau == 2:
				codeN2								=	code
				try:
					dicCpa[codeN1][codeN2]			=	code
				except:
					dicCpa[codeN1]					=	{}
					dicCpa[codeN1][codeN2]			=	code
		elif	niveau == 3:
				codeN3								=	code
				dicCpaN3[codeN3]					=	codeN1+','+codeN2
				try:
					dicCpa[codeN1][codeN2][codeN3]	=	code
				except:
					dicCpa[codeN1][codeN2]			=	{}
					dicCpa[codeN1][codeN2][codeN3]	=	code
	return dicCpa, dicCpaN3
  
def lectureCpaSimple(nomenclature):
    cpaList = []
    try:
        cursor.execute("select code from " + nomenclature + " order by code")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for ligne in cursor.fetchall():
        cpaList.append(ligne[0])
        
    return cpaList
    
def lectureBecEurostat():
    becList = []
    try:
        cursor.execute("select code_eurostat from bec where code_eurostat is not null order by code")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for ligne in cursor.fetchall():
        becList.append(ligne[0])
        
    return becList
    
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
  
def lectureNace1SkillTech(dicNace):
    try:
        cursor.execute("select code from nace1skilltech order by code")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for ligne in cursor.fetchall():
        cle         =     ligne[0].strip()  #la cle est code 
        newkey      =     re.sub('[0-9]','',cle) # on elemine les chiffres on ne garde que les domaines, H ou DL                
        dicNace[cle]=    newkey  # on prend le premier ou les deux premiers carac.
    return dicNace

def lectureNace2SkillTech(dicNace):
    try:
        cursor.execute("select code from nace2skilltech order by code")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for ligne in cursor.fetchall():
        cle         =     ligne[0].strip()  #la cle est code 
        newkey      =     re.sub('[0-9]','',cle) # on elemine les chiffres on ne garde que les domaines, H ou DL                
        dicNace[cle]=    newkey  # on prend le premier ou les deux premiers carac.
    return dicNace
    
def dicNace(nace,compteEurostat,level): #nace=1|2,compteEurostat = NAMA|SBS|BD, level = 1|2 0=on prend tous les levels
	dicNace	=	{}
	if	level	==	'0':
		select	= "select code,niveau,ordre,"+compteEurostat+" from "+nace+" where "+compteEurostat+" =1 order by ordre"
	else:
		select	= "select code,niveau,ordre,"+compteEurostat+" from "+nace+" where "+compteEurostat+" =1 and niveau ="+level+" order by ordre"
	try:
		cursor.execute(select)
	except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
	for	ligne in cursor.fetchall():
		code 		= 	ligne[0].strip()  #la cle est code 
		dicNace[code]=	code  # le code est la cle ont les memes valeurs
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
        dateStart						= 		ligne[2] 
        dateEnd             =     ligne[3]        
    return dateStart, dateEnd 
    
def lectureNaceIndicatorData(indicator, nomenclature, tableName):
    dicIndicator = {}
    startYear    = 0
    selectTable = "select country, codeprod, vector, yyyy from indicators" + tableName + " where typeprod = '" + nomenclature + "' and indicator = '" + indicator + "' and vector <> '-' order by country, codeprod"
    try:
        cursor.execute(selectTable)
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    
    for rec in cursor.fetchall() :
        try :
            dicIndicator[rec[0]][rec[1]] = rec[2].split(',')
            startYear = rec[3]
        except :
            dicIndicator[rec[0]] = {}
            dicIndicator[rec[0]][rec[1]] = rec[2].split(',')
            startYear = rec[3]
    
    return dicIndicator, startYear
    
def lectureCpaNaceIndicatorData(indicator, nomenclature, tableName):
    dicIndicator = {}
    startYear    = 0
    selectTable = "select country, b.nacecode, vector, yyyy from indicators" + tableName + " a inner join " + nomenclature + " b on a.codeprod = b.code where typeprod = '" + nomenclature + "' and indicator = '" + indicator + "' and b.nacecode is not null order by country, codeprod"
    try:
        cursor.execute(selectTable)
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    
    for rec in cursor.fetchall() :
        try :
            dicIndicator[rec[0]][rec[1]] = rec[2].split(',')
            startYear = rec[3]
        except :
            dicIndicator[rec[0]] = {}
            dicIndicator[rec[0]][rec[1]] = rec[2].split(',')
            startYear = rec[3]
    
    return dicIndicator, startYear
    
def lectureNomGeoIndicatorData(indicator, nomenclature, tableName):
    dicIndicator = {}
    startYear    = 0
    selectTable = "select country, codeprod, vector, yyyy, partner from indicators" + tableName + " where typeprod = '" + nomenclature + "' and indicator = '" + indicator + "' order by country, codeprod"
    try:
        cursor.execute(selectTable)
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    
    for rec in cursor.fetchall() :
        try :
            dicIndicator[rec[0]][rec[1]][rec[4]] = rec[2].split(',')
            startYear = rec[3]
        except :
            try :
                dicIndicator[rec[0]][rec[1]] = {}
                dicIndicator[rec[0]][rec[1]][rec[4]] = rec[2].split(',')
                startYear = rec[3]
            except :
                dicIndicator[rec[0]] = {}
                dicIndicator[rec[0]][rec[1]] = {}
                dicIndicator[rec[0]][rec[1]][rec[4]] = rec[2].split(',')
                startYear = rec[3]
    
    return dicIndicator, startYear
    
def majDBtable(tableName,indicator,country,yyyy,codeprod,typeprod,vector): 
    insertTable = "insert into indicators"+tableName+" (indicator,country,yyyy,codeprod,typeprod,vector) values\
    ('"+indicator+"','"+country+"',"+yyyy+",'"+codeprod+"','"+typeprod+"','"+vector+"')"

    try:        
		cursor.execute(insertTable)
    except cx_Oracle.IntegrityError, exc:
		error, = exc.args
		print "code = ", error.code, " message = ", error.message
		return
    
def deleteRecTable(tableName,indicator,country,yyyy,codeprod,typeprod): 
	deleteRecTable	= "delete from indicators"+tableName+" where indicator="+\
	"'"+indicator+"' and country='"+country+"' and yyyy='"+yyyy+"' and codeprod='"+codeprod+"'"
	#print insertTable
	try:        
		cursor.execute(deleteRecTable)
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
    
def buildBecCorrespondance():
    becDic = {}
    try:
        cursor.execute("select code_eurostat, code from bec where code_eurostat is not null order by code")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for ligne in cursor.fetchall():
        becDic[ligne[0]] = ligne[1]
        
    return becDic

def getInsertedNomCodeList(indicator, nomenclature, tableName):
    listCode = []
    
    try:
        cursor.execute("select distinct(codeprod) from indicators" + tableName + " where typeprod = '" + nomenclature + "' and indicator = '" + indicator + "' order by codeprod")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for ligne in cursor.fetchall():
        listCode.append(ligne[0])
        
    return listCode

def getEurostatNations():
    listNation = []
    
    try:
        cursor.execute("select code_iso2 from nation where defaut_pays = 'Y'")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for rec in cursor.fetchall():
        listNation.append(rec[0])
        
    return listNation

def getIndicators(domain):
    listIndicator = []
    
    try: 
        cursor.execute("select id_indicator from indicators where id_domain = '" + domain + "' and node = 'E'")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    for rec in cursor.fetchall():
        listIndicator.append(rec[0])
    
    return listIndicator

def getIndicatorYear(domain, indicator, nomenclature):
    year = 0
    
    try: 
        cursor.execute("select min(yyyy) from indicators" + domain + " where indicator = '" + indicator + "' and typeprod = '" + nomenclature + "'")
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    
    for rec in cursor.fetchall():
        year = rec[0]
    
    if year == None:
        year = 9999#si il n y a aucun record on met une annee par defaut
    
    return year

def deleteIndicators(domain, nomenclature = '', indicator = []):
    queryString = ''
    
    if domain == 'matrix' :
        queryString = 'delete from matrix'
    else :
        queryString = 'delete from indicators' + domain
    
    if nomenclature != '' or len(indicator) > 0 :
        queryString = queryString + ' where'
           
        if nomenclature != '' :
            queryString = queryString + " typeprod = '" + nomenclature + "'"
            
            if len(indicator) > 0 :
                queryString = queryString + ' and'
        if len(indicator) > 0 :
            queryString = queryString + ' indicator in (' + ', '.join("'" + item + "'" for item in indicator) + ')'
                    
    try: 
        cursor.execute(queryString)
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    return
    
def setUpdateDate(domain):
    
    if domain == 'matrix' :
        domain = 'sectoral interrelations'
    
    queryString = "update update_info set update_date = sysdate where domain = '" + domain + "'"
    
    try:
        cursor.execute(queryString)
    except cx_Oracle.IntegrityError, exc:
        error, = exc.args
        print "code = ", error.code, " message = ", error.message
        return
    return 

def getNomenclature(nomenclature):
    queryString = 'select code from ' + nomenclature
    
    try: 
        cursor.execute(queryString)
    except:
        print "An error occured executing : " + queryString
        return
    
    codes = []
    
    for rec in cursor.fetchall():
        codes.append(rec[0])
    
    return frozenset(codes)
    
    