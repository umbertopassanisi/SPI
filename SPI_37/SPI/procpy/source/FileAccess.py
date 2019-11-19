import re
import spiLib
import spiLibTrade

def lectureIndicator(G_dicIndicator,domain,dirUse):
	dirFile			=	dirUse + '\\input\\txt'
	fichierLecture 	=	dirFile + '\\indicator'+domain+'.txt'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	for	record in fichier:
		ligne				=	record.split(';')
		cle 				=	ligne[0].strip()  #la cle est indicateur Eurostat
		G_dicIndicator[cle]	=	ligne[1].strip()  #le contenu est indicateur SPI
	fichier.close()
	return G_dicIndicator

def lectureHS1992toCPA2002(dirCSV):
	dicFile			=	{}
	fichierLecture 	=	dirCSV + '\\hs1992tocpa2002ratio.csv'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec les meta, HS1992;HS 2007;CPA_2008;	
	for	record in fichier:
		ligne				=	record.split(';')
		codeCPA				=	ligne[1].strip()
		ratio				=	ligne[2].strip()
		#on ne prend que les code CPA de 15 a 37 inclus
		if	int(codeCPA) > 14 and int(codeCPA) < 38:
			cle 			=	ligne[0].strip()  #la cle est le code HS1992
			try:
				dicFile[cle][codeCPA]	=	ratio  #le contenu les 2 premiers chiffres du CPA2002 
			except:
				dicFile[cle]			=	{}
				dicFile[cle][codeCPA]	=	ratio
	fichier.close()
	return dicFile
	
def lectureHS1992toCPA2008(dirCSV,fileLog):
	dicFile			=	{}
	dicCpa			=	{}
	dicHs1992		=	{}
	dicCpa2008		=	{}
	fichierLecture 	=	dirCSV + '\\hs1992tocpa2008ratio.csv'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec les meta, HS1992;HS2007;HS 2007;CPA 2008;ratio	
	for	record in fichier:
		ligne						=	record.split(';')
		hs1992						=	ligne[0].strip()
		hs1992tohs2007				=	ligne[1].strip()		
		hs2007tocpa2008				=	ligne[2].strip()
		cpa2008						=	ligne[3].strip()		
		ratio						=	ligne[4].strip()
		try:
			dicHs1992[hs1992tohs2007][hs1992] 		=	hs1992
		except:
			dicHs1992[hs1992tohs2007] 				=	{}
			dicHs1992[hs1992tohs2007][hs1992] 		=	hs1992
		try:
			dicCpa2008[hs2007tocpa2008][cpa2008] 	=	ratio
		except:
			dicCpa2008[hs2007tocpa2008] 			=	{}
			dicCpa2008[hs2007tocpa2008][cpa2008] 	=	ratio
	hs1992tohs2007Sort     		=   dicHs1992.keys() 
	hs1992tohs2007Sort.sort()
	for hs1992tohs2007 in hs1992tohs2007Sort:
		for hs1992 in dicHs1992[hs1992tohs2007]:
			try:			
				for	cpa2008 in dicCpa2008[hs1992tohs2007]:
					try:
						dicFile[hs1992][cpa2008]	= dicCpa2008[hs1992tohs2007][cpa2008]						
					except:
						dicFile[hs1992]				= {}
						dicFile[hs1992][cpa2008]	= dicCpa2008[hs1992tohs2007][cpa2008]
			except:
				fileLog.write('no key hs1992tohs2007 in cpa2008 : '+hs1992tohs2007+'\n')
	hs1992Sort     		=   dicFile.keys() 
	hs1992Sort.sort()
	for hs1992 in hs1992Sort:		 
		nbrCpa	=	len(dicFile[hs1992])
		for	cpa2008 in dicFile[hs1992]:
			agregatCPA		 =	cpa2008[0:2]
			if	len(cpa2008) == 6 and (int(agregatCPA) > 9 and int(agregatCPA) < 33):
				ratio						=	1.00/nbrCpa
				try:
					dicCpa[hs1992][agregatCPA]	=	str("{:.3f}".format(ratio))
				except:
					dicCpa[hs1992]				=	{}
					dicCpa[hs1992][agregatCPA]	=	str("{:.3f}".format(ratio))
		#print hs1992, dicFile[hs1992]
	'''	
	hs1992Sort     		=   dicCpa.keys() 
	hs1992Sort.sort()
	for hs1992 in hs1992Sort:		
		print hs1992, dicCpa[hs1992]
	'''	
	fichier.close()
	return dicCpa

def lectureBEC(dirCSV):
	dicFile			=	{}
	fichierLecture 	=	dirCSV + '\\beccode.csv'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec les meta, BEC;BEC	
	for	record in fichier:
		ligne				=	record.split(';')
		cle 			=	ligne[0].strip()  #la cle est le code BEC
		dicFile[cle]	=	ligne[0].strip()  #le contenu est le code BEC
	fichier.close()
	return dicFile	
	
def lectureTradeGoodsRCA(fichierTXT):
	dicFile			=	{}
	dicFileWld		=	{}
	fichierLecture 	=	fichierTXT
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec annee min et max
	lstrec		= rec1er.split(',')
	startYear   = lstrec[0].strip()
	endYear		= lstrec[1].strip()	
	#WLD,13,2000,190335109146!:!:!:!:!:!284236292080
	for	record in fichier:
		ligne				=	record.split(',')
		country				=	ligne[0].strip()
		codeCPA				=	ligne[1].strip()
		year				=	ligne[2].strip()
		vectorStr			=	ligne[3].strip()
		vector				=	vectorStr.split('!')
		if	country == 'WLD':
			dicFileWld		=	spiLibTrade.defDicFile(dicFileWld,country,codeCPA,year,vector,startYear,endYear)
		else:
			dicFile			=	spiLibTrade.defDicFile(dicFile,country,codeCPA,year,vector,startYear,endYear)
	fichier.close()
	return dicFile, dicFileWld, startYear, endYear
	
def lectureTradeServiceRCA(fichierTXT):
	dicFile			=	{}
	dicFileWld		=	{}
	fichierLecture 	=	fichierTXT
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec annee min et max
	lstrec		= rec1er.split(',')
	startYear   = lstrec[0].strip()
	endYear		= lstrec[1].strip()	
	#WLD,13,2000,190335109146!:!:!:!:!:!284236292080
	for	record in fichier:
		ligne				=	record.split(',')
		country				=	ligne[0].strip()
		codeCPA				=	ligne[1].strip()
		year				=	ligne[2].strip()
		vectorStr			=	ligne[3].strip()
		vector				=	vectorStr.split('!')
		if	country == 'WL':
			dicFileWld		=	spiLibTrade.defDicFile(dicFileWld,'WLD',codeCPA,year,vector,startYear,endYear)
		else:
			dicFile			=	spiLibTrade.defDicFile(dicFile,country,codeCPA,year,vector,startYear,endYear)
	fichier.close()
	return dicFile, dicFileWld, startYear, endYear
	
def lectureNationUN(dirTXT):
	dicFile			=	{}
	fichierLecture 	=	dirTXT + '\\nations.txt'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec les meta, HS1992;HS 2007;CPA_2008;	
	for	record in fichier:
		ligne				=	record.split(',')
		codeISO2			=	ligne[1].strip()
		codeUN				=	ligne[6].strip()
		world_manufacture	=	ligne[7].strip()		
		if	world_manufacture == 'Y':
			cle 			=	codeUN  #la cle est le code UN
			dicFile[cle]	=	codeISO2  #la cle est le code IS02 
	fichier.close()
	return dicFile

def lectureNationUNInverse(dirTXT):
	dicFile			=	{}
	fichierLecture 	=	dirTXT + '\\nations.txt'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	rec1er     	= fichier.readline() #1er rec avec les meta, HS1992;HS 2007;CPA_2008;	
	for	record in fichier:
		ligne				=	record.split(',')
		codeISO2			=	ligne[1].strip()
		codeUN				=	ligne[6].strip()
		world_manufacture	=	ligne[7].strip()		
		if	world_manufacture == 'Y':
			cle 			=	codeISO2  #la cle est le code UN
			dicFile[cle]	=	codeUN  #la cle est le code IS02 
	fichier.close()
	return dicFile
	
def lectureFileWto(dirCSV):
	minStartYear        = 99999
	maxEndYear          = -1
	dicFile				= {}
	fichierLecture 		= dirCSV + '\\wto.csv'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print "le fichier ", fichierLecture, " est introuvable"
	#1er rec avec les meta
	#Topic_code,Topic_desc,DataSet_code,DataSet_desc,Country_code=4,
	#Country_desc,Flow_code=6,Flow_desc,Indicator_code=8,Indicator_desc,
	#Partner_Country_code=10,Partner_Country_desc,Unit_code=12,
	#Unit_desc,Year=14,Value=15,Value_Flag,Notes_Export
	rec1er     	= fichier.readline() 
	for	recordIn in fichier:
		record =	re.sub('[a-z],','',recordIn) #enleve les , dans certaine variable	
		ligne				=	record.split(',')
		try:
			country_code		=	ligne[4].strip('"')
			flow_code			=	ligne[6].strip('"')
			indicator_code		=	ligne[8].strip('"') #sector
			partner_Country_code=	ligne[10].strip('"')
			unit_code			=	ligne[12].strip('"')
			year				=	ligne[14].strip()
			value				=	ligne[15].strip()
		except:
			pass #ne fait rien, continue a l'instruction suivante
		#on ne prend que les exports
		if	flow_code		==	'X':
			minStartYear,maxEndYear = spiLib.defMinMaxYear(year,minStartYear,year,maxEndYear)
			try:
				dicFile[country_code][indicator_code][year]		= value		
			except:
				try:
					dicFile[country_code][indicator_code]		= {}
					dicFile[country_code][indicator_code][year]	= value	
				except:
					dicFile[country_code]						= {}
					dicFile[country_code][indicator_code]		= {}
					dicFile[country_code][indicator_code][year]	= value	
	fichier.close()
	return dicFile,minStartYear,maxEndYear