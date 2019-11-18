import re
import DBAccess

from pprint import pprint

def defDicEurostat(listInput):
	#currency,post,stk_flow,partner,geo\time
	dicEurostat	=	dict(currency=-1,sector=-1,flow=-1,partner=-1,geotime=-1)
	for	iEurostat	in range(0,len(listInput)):
		if  	re.search('currency', listInput[iEurostat], flags=re.IGNORECASE):				
				dicEurostat['currency']		=	iEurostat
		elif	re.search('post', listInput[iEurostat], flags=re.IGNORECASE) or re.search('bop_item', listInput[iEurostat], flags=re.IGNORECASE) :					
				dicEurostat['sector']		=	iEurostat
		elif	re.search('stk_flow', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['flow']			= iEurostat
		elif	re.search('partner', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['partner']		= iEurostat					
		elif	re.search('geo', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['geotime']		= iEurostat
	return dicEurostat
	
def	vectorYear(dicInput):
	yearSort    	=   dicInput.keys()
	yearSort.sort()
	startYear		=	int(yearSort[0])#1er annee
	endYear			=	int(yearSort[-1])#derniere annee
	nbrYear			=	endYear - startYear + 1 # de zero a max + 1				
	lstValue		=	[':']*nbrYear
	i				=	0
	year			=	''
	lstValeur		=	''
	for	i	in	range(0,nbrYear):
		try:
			year		= str(startYear + i)
			lstValeur	= lstValeur + str(dicInput[year])+'!'
		except:
			lstValeur	= lstValeur + ':!'
	return	lstValeur[:-1]
	
def	defDicFile(dicFileInput,country,codeCPA,year,vector,startYear,endYear):
	dicFile	=	dicFileInput
	vector	=	defVectorNormalize(year,vector,startYear,endYear)
	try:
		dicFile[country][codeCPA]		=	vector
	except:
		dicFile[country]				=	{}
		dicFile[country][codeCPA]		=	vector
	return	dicFile

def defVectorNormalize(year,vectorInput,startYear,endYear):
	vector			= vectorInput	
	vectorStartYear = -1 
	vectorEndYear	= -1
	vectorStart		= []
	vectorEnd		= []
	minStartYear	= int(startYear)#on aura besoin de l'annee de depart sous forme d'integer
	maxEndYear		= int(endYear)#de meme pour l'annee de fin
	nbrVector		= len(vector)
	nbrYear			= maxEndYear - minStartYear	
	vectorStartYear	= int(year)
	vectorEndYear	= vectorStartYear + nbrVector - 1 #on doit inclure les bornes
	if 	vectorStartYear > minStartYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
		vectorStart = [':']*(vectorStartYear - minStartYear)
	if 	vectorEndYear 	< maxEndYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
		vectorEnd	= [':']*(maxEndYear - vectorEndYear)
	vector	= vectorStart + vector + vectorEnd	
	return vector
#traitement des agregats, on cree un dic avec la valeur des cpa 
#ex : D, DA, 15 on met dans dic[D][DA][15] = valeur du cpa 15
#la somme se fait dans une autre procedure
def defDicTotal(dicFile,dicCpaN3,lenVector):
	dicTotal						=	{}
	dicAgregat						=	{}
	countrySort     				=   dicFile.keys() 
	countrySort.sort()
	for country in countrySort:
		cpaSort    					=   dicFile[country].keys()
		cpaSort.sort()
		vectorTotal					=	[0]*lenVector
		dicTotal[country]			=	{}
		dicAgregat[country]			=	{}
		for cpa in cpaSort:
			vector					=	dicFile[country][cpa]
			lstCpa					=	dicCpaN3[cpa]
			lstCpaCode				=	lstCpa.split(',')
			cpaN1					=	lstCpaCode[0]
			cpaN2					=	lstCpaCode[1]
			#on cree le dic a 3 niveau dic[D][DA][15] = vector
			try:
				dicAgregat[country][cpaN1][cpaN2][cpa] 		= vector
			except:
				try:
					dicAgregat[country][cpaN1][cpaN2]		= {}
					dicAgregat[country][cpaN1][cpaN2][cpa]	= vector
				except:
					dicAgregat[country][cpaN1] 				= {}
					dicAgregat[country][cpaN1][cpaN2]		= {}
					dicAgregat[country][cpaN1][cpaN2][cpa]	= vector				
			for i in range(0,len(vector)):
				try:
					vectorTotal[i]	=	vectorTotal[i] + int(vector[i])
				except:
					vectorTotal[i]	=	':'
		dicTotal[country]['total']	=	vectorTotal
		#print country, dicAgregat[country]
	return 	dicTotal, dicAgregat
	
def defPrintAgregat(dicCountryAgregat,lenVector):
	dicTotal								=	dicCountryAgregat.copy()
	dicAgregat								=	dicCountryAgregat.copy()
	countrySort								=	dicAgregat.keys() 
	countrySort.sort()
	for country in countrySort:
		for cpaN1 in dicAgregat[country].keys():
			print country, cpaN1
			for cpaN2 in dicAgregat[country][cpaN1].keys():
				print country, cpaN1, cpaN2
				for cpaN3 in dicAgregat[country][cpaN1][cpaN2].keys():
					print country, cpaN1, cpaN2,cpaN3
	return

def defDicCalculAgregat(dicCountryAgregat,lenVector):
	dicTotalN1								=	{}
	dicTotalN2								=	{}
	dicAgregat								=	dicCountryAgregat.copy()
	countrySort								=	dicAgregat.keys() 
	countrySort.sort()
	for country in countrySort:
		cpaN1Sort							=	dicAgregat[country].keys()
		cpaN1Sort.sort()
		for cpaN1 in cpaN1Sort:
			vectorTotalN1					=	[0]*lenVector
			dicTotalN1[country]				=	{}
			dicTotalN2[country]				=	{}			
			dicTotalN1[country][cpaN1]		=	vectorTotalN1
			cpaN2Sort						=	dicAgregat[country][cpaN1].keys()
			for cpaN2 in cpaN2Sort:
				vectorTotalN2				=	[0]*lenVector
				dicTotalN2[country][cpaN2]	=	vectorTotalN2
				cpaN3Sort					=	dicAgregat[country][cpaN1][cpaN2].keys()
				for cpaN3 in cpaN3Sort:
					vector					=	dicAgregat[country][cpaN1][cpaN2][cpaN3]
					for i in range(0,len(vector)):
						try:
							vectorTotalN2[i]	=	vectorTotalN2[i] + int(vector[i])
						except:
							vectorTotalN2[i]	=	':'
						try:
							vectorTotalN1[i]	=	vectorTotalN1[i] + int(vector[i])
						except:
							vectorTotalN1[i]	=	':'
				dicTotalN2[country][cpaN2]	=	vectorTotalN2
		dicTotalN1[country][cpaN1]			=	vectorTotalN1
	return 	dicTotalN1, dicTotalN2
def defDicTotalSector(dicFile,lenVector):
	dicTotal						=	{}
	countrySort     				=   dicFile.keys() 
	countrySort.sort()
	for country in countrySort:
		sectorSort    				=   dicFile[country].keys()
		sectorSort.sort()
		vectorTotal					=	[0]*lenVector
		dicTotal[country]			=	{}
		#le total des sectors est contenu dans le sector 200
		vector						=   dicFile[country]['200']
		for i in range(0,len(vector)):
			try:
				vectorTotal[i]	=	int(vector[i])
			except:
				vectorTotal[i]	=	':'
		dicTotal[country]['total']	=	vectorTotal
	return 	dicTotal

def defDicTotalBec(dicFile,lenVector):
	dicTotal						=	{}
	countrySort     				=   dicFile.keys() 
	countrySort.sort()
	for country in countrySort:
		becSort    					=   dicFile[country].keys()
		becSort.sort()
		vectorTotal					=	[0]*lenVector
		dicTotal[country]			=	{}
		for bec in becSort:
			if	len(bec)			== 1:
				vector      			=   dicFile[country][bec]
				for i in range(0,len(vector)):
					try:
						vectorTotal[i]	=	vectorTotal[i] + int(vector[i])
					except:
						vectorTotal[i]	=	':'
		dicTotal[country]['total']	=	vectorTotal
	return 	dicTotal
	
def	dicIndicator(country,partner,sector,vector,dicIndicator):
	try:  				
		dicIndicator[country][sector][partner]  	= vector
	except:
		try:
			dicIndicator[country][sector]  			= {}
			dicIndicator[country][sector][partner]  = vector
		except:
			dicIndicator[country]        			= {}
			dicIndicator[country][sector]  			= {}
			dicIndicator[country][sector][partner]  = vector
	return dicIndicator	

def	createIndicatorService(dicIndicator,flowInput,G_flow,compte,minStartYear,maxEndYear,tableName,fileLog):
	if compte == 'bpm5' :
		codeTotal = '200'
	else :
		codeTotal = 'S'

	flowParam		= G_flow
	startYear		= minStartYear
	nbrVector		= int(maxEndYear) - int(minStartYear) + 1
	totalWld		= []
	dicGeoSector	= {}
	dicGeoSector,totalWld	= createDicGeoSector(dicIndicator,minStartYear,maxEndYear)
	countrySort     = dicGeoSector.keys() 
	countrySort.sort()
	for country in countrySort:
		sectorSort	= dicGeoSector[country].keys()
		sectorSort.sort()
		for sector	in sectorSort:
			vector			= dicIndicator[country][sector]['WORLD']
			vectorGeoTotal 	= dicGeoSector[country][codeTotal]
			try:
				vectorEu27		= dicIndicator['EU27'][sector]['WORLD']
			except:
				vectorEu27		= [':']*nbrVector
			try:
				vectorEu28		= dicIndicator['EU28'][sector]['WORLD']
			except:
				vectorEu28		= [':']*nbrVector
			try:				
				vectorEu27Total	= dicGeoSector['EU27'][codeTotal]
			except:
				vectorEu27Total = [':']*nbrVector
			try:
				vectorEu28Total	= dicGeoSector['EU28'][codeTotal]
			except:
				vectorEu28Total = [':']*nbrVector
			lstX			= ''
			lstXshare		= ''
			lstXspeu27		= ''
			lstXspeu28		= ''
			for i in range(0,nbrVector):
				try:
					valueVector			=	float(vector[i])
				except:
					valueVector			=	vector[i]
				try:
					valueVectorGeoTotal	=	float(vectorGeoTotal[i])
					xshare				=	(valueVector/valueVectorGeoTotal)*100
				except:
					valueVectorGeoTotal	=	':'
					xshare				=	':'
				try:
					valueVectorEu27		=	float(vectorEu27[i])
				except:
					valueVectorEu27		=	':'
				try:
					valueVectorEu27Total=	float(vectorEu27Total[i])					
					xspeu27Float		=	(valueVector/valueVectorGeoTotal)/(valueVectorEu27/valueVectorEu27Total)
					xspeu27				= 	str("{:.8f}".format(xspeu27Float))
				except:
					xspeu27				=	':'
				try:
					valueVectorEu28		=	float(vectorEu28[i])
				except:
					valueVectorEu28		=	':'
				try:
					valueVectorEu28Total=	float(vectorEu28Total[i])
					xspeu28Float		=	(valueVector/valueVectorGeoTotal)/(valueVectorEu28/valueVectorEu28Total)					
					xspeu28				= 	str("{:.8f}".format(xspeu28Float))
				except:
					xspeu28				=	':'
				lstX		= lstX + str(valueVector)+','	
				lstXshare	= lstXshare + str(xshare)+','
				lstXspeu27	= lstXspeu27 + str(xspeu27)+','
				lstXspeu28	= lstXspeu28 + str(xspeu28)+','
			DBAccess.majDBtable(tableName,flowParam,country,str(startYear),sector,compte,lstX[:-1])
			DBAccess.majDBtable(tableName,flowParam+'share',country,str(startYear),sector,compte,lstXshare[:-1])
			DBAccess.majDBtable(tableName,flowParam+'speu27',country,str(startYear),sector,compte,lstXspeu27[:-1])
			DBAccess.majDBtable(tableName,flowParam+'speu28',country,str(startYear),sector,compte,lstXspeu28[:-1])

def	createIndicatorServiceDestOrg(dicIndicator,flowInput,compte,minStartYear,maxEndYear,tableName,fileLog,dicCountryPartner):
	if	flowInput == 'CRE':#export
		nameAbsolute		= 'xdest'
		nameDistribution	= 'xdestsh'
	else:
		nameAbsolute		= 'morig'
		nameDistribution	= 'morigsh'	
		
	startYear		= minStartYear
	nbrVector		= int(maxEndYear) - int(minStartYear) + 1
	totalWld		= []
	dicGeoSector	= {}
	dicGeoSector,totalWld	= createDicGeoSector(dicIndicator,minStartYear,maxEndYear)
	countrySort     = dicIndicator.keys() 
	countrySort.sort()
	for country in countrySort:
		sectorSort	= dicIndicator[country].keys()
		sectorSort.sort()
		for sector	in sectorSort:
			partnerSort		= dicIndicator[country][sector].keys()
			partnerSort.sort()
			for partner in partnerSort:	
				vector		= dicIndicator[country][sector][partner]
				lstValue	= ''
				lstdestOrig	= ''
				for i in range(0,nbrVector):
					try:
						destOrigValue	= float(vector[i])/float(totalWld[i])
						destOrig		= str("{:.8f}".format(destOrigValue))
					except:
						destOrig		= ':'
					lstValue			= lstValue + str(vector[i])+','	
					lstdestOrig			= lstdestOrig + str(destOrig)+','
				partnerIso2				= dicCountryPartner[partner]
				DBAccess.majDBtableGeo(tableName,nameAbsolute,country,str(startYear),sector,compte,lstValue[:-1],partnerIso2)
				DBAccess.majDBtableGeo(tableName,nameDistribution,country,str(startYear),sector,compte,lstdestOrig[:-1],partnerIso2)
					
def createDicGeoSector(dicIndicator,minStartYear,maxEndYear):
	nbrVector		= int(maxEndYear) - int(minStartYear) + 1
	dicGeoSector	= {}
	totalWld		= [0]*nbrVector
	countrySort     = dicIndicator.keys() 
	countrySort.sort()
	for country in countrySort:
		sectorSort	= dicIndicator[country].keys()
		sectorSort.sort()
		dicGeoSector[country]	= {}
		for sector	in sectorSort:
			dicGeoSector[country][sector]	= {}
			totalGeoSector	=	[0]*nbrVector
			partnerSort		= 	dicIndicator[country][sector].keys()
			partnerSort.sort()
			if	sector == '200' or sector =='S':
				for partner in partnerSort:
					if	partner == 'WORLD':
						vector		= dicIndicator[country][sector][partner]
						#pour le total on prend la somme des EU27 + EXT_EU27
						#modification du 15/01/2015 suite a la demande de la B2
						#le total est WORLD
						for i in range(0,nbrVector):
							try:
								totalGeoSector[i] = float(vector[i])
							except:
								totalGeoSector[i] = ':'
							try:
								totalWldValue	  = float(vector[i])
							except:
								totalWldValue	  = 0.0							
							try:
								totalWld[i]		  = totalWld[i] + totalWldValue
							except:
								totalWld[i]		  = ':'	
			dicGeoSector[country][sector] = totalGeoSector
			#print country, sector,totalGeoSector
	return dicGeoSector, totalWld
	
