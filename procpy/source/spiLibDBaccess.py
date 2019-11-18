import DBAccess
import DBConnect
	
def defSelectdicNace(nomenclature,compteEurostat):
	dicNace       	=  	{}
	if	nomenclature== 'nace1':
		dicNace		=  	DBAccess.lectureNace1(dicNace,compteEurostat)
	else:
		dicNace		=  	DBAccess.lectureNace2(dicNace,compteEurostat)
	return dicNace
	
def defSelectdicNaceNE(nomenclature,compteEurostat):
	dicNaceNe       =  	{}
	dicNaceNe		=  	DBAccess.lectureNaceNE(dicNaceNe,nomenclature,compteEurostat)
	return dicNaceNe	

def defSelectdicCpaNE(nomenclature,compte):	#nomenclature=cpa2002/cpa2008
	dicCpaNe       	=  	{}					#compte=comtrade/comext
	dicCpaNe		=  	DBAccess.lectureCpaNE(nomenclature,compte)
	return dicCpaNe	
def defSelectdicSectorNE(nomenclature):	#nomenclature=cpa2002/cpa2008
	dicNe       	=  	{}				#compte=comtrade/comext
	dicNe			=  	DBAccess.lectureSectorNE(nomenclature)
	return dicNe		
#-------------------------------------------------------------------------------------------#
#TRAITEMENT DES TOTAUX POUR EXTERNAL, TRADE IN GOODS RCA et TRADE IN SERVICE RCA
#
def createTableTotal(indicator,fileLog,dicFile,dicTotalCountry,dicFileWld,dicTotalWld,startYear,tableName,typeProduit):
	vectorWorldTotal		=	dicTotalWld['WLD']['total']
	vectorNul				=	[':']*len(vectorWorldTotal)
	countrySort     		=   dicFile.keys() 
	countrySort.sort()
	for country in countrySort:
		vectorCountryTotal	=	dicTotalCountry[country]['total']
		cpaSort    			=   dicFile[country].keys()
		cpaSort.sort()
		for cpa in cpaSort:
			vectorCountry      	=   dicFile[country][cpa]
			try:
				vectorWorld      	=   dicFileWld['WLD'][cpa]
			except:
				fileLog.write('no cpa WORLD ='+cpa+'\n')
				vectorWorld      	=   vectorNul
			lstResultRCA		=	''
			lstResultSRCA		=	''
			lstResultRCAX		=	''
			lstResultSRCAX		=	''			
			lstResultXWSH		=	''
			for i in range(0,len(vectorCountry)):
				if (vectorCountryTotal[i] != ':') and (vectorWorldTotal[i] != ':') and \
				   (vectorCountry[i] != ':') and (vectorWorld[i] != ':'):					
					valueCountry		=	float(vectorCountry[i])
					valueCountryTotal	=	float(vectorCountryTotal[i])
					valueWorld			=	float(vectorWorld[i])
					valueWorldTotal		=	float(vectorWorldTotal[i])
					valueWorldX			=	valueWorld - valueCountry
					valueWorldTotalX	=	valueWorldTotal - valueCountryTotal					
					try:
						resultRCA		= 	(valueCountry/valueCountryTotal)/(valueWorld/valueWorldTotal)		
					except:
						resultRCA		=	'0'
					try:
						resultRCAX		= 	(valueCountry/valueCountryTotal)/(valueWorldX/valueWorldTotalX)		
					except:
						resultRCAX		=	'0'						
					try:
						resultSRCA		= 	(resultRCA - 1)/(resultRCA + 1)		
					except:
						resultSRCA		=	'0'	
					try:
						resultSRCAX		= 	(resultRCAX - 1)/(resultRCAX + 1)		
					except:
						resultSRCAX		=	'0'							
					try:
						resultXWSH		= 	(valueCountry/valueWorld) * 100		
					except:
						resultXWSH		=	'0'						
				else:
					resultRCA			=	':'
					resultSRCA			=	':'
					resultRCAX			=	':'
					resultSRCAX			=	':'					
					resultXWSH			=	':'										
				lstResultRCA			=	lstResultRCA+str(resultRCA)+','
				lstResultSRCA			=	lstResultSRCA+str(resultSRCA)+','
				lstResultRCAX			=	lstResultRCAX+str(resultRCAX)+','
				lstResultSRCAX			=	lstResultSRCAX+str(resultSRCAX)+','				
				lstResultXWSH			=	lstResultXWSH+str(resultXWSH)+','
			#print indicator,country,cpa,startYear,typeProduit,lstResult[:-1]
			DBAccess.majDBtable(tableName,'rca',country,str(startYear),cpa,typeProduit,lstResultRCA[:-1])
			DBAccess.majDBtable(tableName,'srca',country,str(startYear),cpa,typeProduit,lstResultSRCA[:-1])
			DBAccess.majDBtable(tableName,'xwsh',country,str(startYear),cpa,typeProduit,lstResultXWSH[:-1])
			if	typeProduit != 'sector':
				DBAccess.majDBtable(tableName,'rcax',country,str(startYear),cpa,typeProduit,lstResultRCAX[:-1])
				DBAccess.majDBtable(tableName,'srcax',country,str(startYear),cpa,typeProduit,lstResultSRCAX[:-1])	
			
def createTableCpaNE(typeProduit,compte,dicFile,startYear,fileLog,tableName):
	#liste avec les codes naces NE on creer un record avec la valeur '-' comme vecteur
	#nomenclature=cpa2002/cpa2008), sector
	if	typeProduit == 'sector':
		dicCpa					= 	defSelectdicSectorNE(typeProduit)
	else:
		dicCpa					= 	defSelectdicCpaNE(typeProduit,compte)
	countrySort     			=   dicFile.keys() 
	countrySort.sort()		
	for country in countrySort:
		cpaSort    				=   dicCpa.keys()
		cpaSort.sort()	
		for cpa in cpaSort:
			DBAccess.majDBtable(tableName,'rca',country,str(startYear),cpa,typeProduit,'-')	
			DBAccess.majDBtable(tableName,'srca',country,str(startYear),cpa,typeProduit,'-')	
			DBAccess.majDBtable(tableName,'xwsh',country,str(startYear),cpa,typeProduit,'-')
			if	typeProduit != 'sector':
				DBAccess.majDBtable(tableName,'rcax',country,str(startYear),cpa,typeProduit,'-')	
				DBAccess.majDBtable(tableName,'srcax',country,str(startYear),cpa,typeProduit,'-')	