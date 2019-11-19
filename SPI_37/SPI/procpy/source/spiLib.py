from decimal import *
import re
import DBAccess
import DBConnect

#
# startIndice = longueur la plus grande rencontree pour un vecteur
# comme on traite plusieurs fichiers, la longueur des vecteurs peuvent etre variable
# endYear = derniere annee selectionnee, annee la plus grande selectionnee
# startYear = calcul de l'annee de debut pour tous les vecteurs
# G_startYear = annee de debut minimum par defaut pour tous les vecteurs, si la startYear est plus petite
# alors on selectionnera la G_startYear
# nbrIndice = le nombre element pour tous les vecteurs
#
def defNbrIndice(startIndice,firstYear,endYear):	
	startYear	=	int(endYear) - startIndice 
	if	(startYear < firstYear):
		startYear	=	firstYear
		nbrIndice	=	int(endYear) - startYear + 1 
	else:
		nbrIndice	=	startIndice + 1		
	return nbrIndice, startYear
  
#si le vecteur courant est plus grand que le vecteur par defaut 
#on ne prend que les elements correspondant a la longueur par defaut
def	defStartRange(nbrIndice,nbrV):
	if	nbrV 	>	nbrIndice:			
		startRange	=	nbrV - nbrIndice
	else:
		startRange	=	0
	return	startRange
  
def defSelectdicNace(nomenclature,compteEurostat):
	dicNace       	=  	{}
	if	nomenclature== 'nace1':
		dicNace		=  	DBAccess.lectureNace1(dicNace,compteEurostat)
	else:
		dicNace		=  	DBAccess.lectureNace2(dicNace,compteEurostat)
		if	compteEurostat 		== 'bd':
			dicNace['C15']		=  'C'
			dicNace['C13_C14']	=  'C'
	return dicNace
  
def defDicCpa(nomenclature):
	dicCpa = {}
	dicCpa = DBAccess.lectureCpa2008(dicCpa, nomenclature)
  
def defSelectdicNaceSkillTech(nomenclature):
	dicNace = {}
	if	nomenclature== 'nace1':
		dicNace		=  	DBAccess.lectureNace1SkillTech(dicNace)
	else:
		dicNace		=  	DBAccess.lectureNace2SkillTech(dicNace)
	return dicNace
  
def defSelectdicNaceNE(nomenclature,compteEurostat):
	dicNaceNe       =  	{}
	dicNaceNe		=  	DBAccess.lectureNaceNE(dicNaceNe,nomenclature,compteEurostat)
	return dicNaceNe	
		
def	defDicNaceFail(dicNace):
	dicNaceFail				=	{}
	lstNace					=	list(dicNace.values()) #valeur du dictionnaire
	for	nace in dicNace:
		findNace			=	dicNace[nace]
		dicNaceFail[nace]	= 	lstNace.count(findNace) #on compte le numbre de fois que la valeur du dic apparait dans le dic
	return dicNaceFail
	
def defCreateNaceNotPresent(vector,dicIndicator,country,nace):	
	try:
		vector      	=   dicIndicator[country][nace]
	except:
		nbrKey			=	dicNaceFail[nace]
		if	(nbrKey == 2) and (len(previousVector) > 0):
			vector		=	previousVector
		else:
			fileLog.write('pas de code nace pays: '+str(country)+' nace = '+str(nace)+' nbrKey ='+str(nbrKey)+'\n')
			#continue
      
#si le vecteur courant est plus petit que la longueur du vecteur par defaut
#on va combler le debut du vecteur avec des ':'
def defFillEmpty(nbrIndice,nbrV):	
	vectorElement	=	''
	nbrAremplir		=	0
	if	nbrIndice	>	nbrV:
		nbrAremplir	=	nbrIndice -	nbrV
		for i in range(0, nbrAremplir):
			vectorElement		=	':,' +  vectorElement
	return vectorElement,nbrAremplir
  
def defDicComext(listInput):
	dicComext = {}
	
	for iComext in range(0, len(listInput)) :
		if listInput[iComext].strip() == 'REPORTER':				
			dicComext['reporter'] = iComext
		elif listInput[iComext].strip() == 'PARTNER':	
			dicComext['partner'] = iComext
		elif listInput[iComext].strip() == 'PRODUCT':	
			dicComext['product'] = iComext
		elif listInput[iComext].strip() == 'FLOW': 	
			dicComext['flow'] = iComext
		elif listInput[iComext].strip() == 'PERIOD':
			dicComext['period'] = iComext
		elif listInput[iComext].strip() == 'INDICATOR_VALUE':	
			dicComext['value'] = iComext
	
	return dicComext
  
def defDicEurostat(listInput):
	dicEurostat	=	dict(unit=-1,nace=-1,indic=-1,size=-1,geo=-1, sex=-1, age=-1, partner=-1, flow=-1, category=-1, isco=-1, post=-1, sector=-1)
	for	iEurostat	in range(0,len(listInput)):
		if  	re.search('unit', listInput[iEurostat], flags=re.IGNORECASE):				
				dicEurostat['unit']		=	iEurostat
		elif	re.search('nace', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['nace']		=	iEurostat
		elif	re.search('indic', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['indic']	= iEurostat
		elif	re.search('na_item', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['indic']	= iEurostat		
		elif	re.search('size', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['size']		= iEurostat
		elif	re.search('value', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['size']		= iEurostat						
		elif	re.search('geo', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['geotime']	= iEurostat
		elif	re.search('sex', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['sex']	    = iEurostat
		elif	re.search('age', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['age']	    = iEurostat
		elif	re.search('partner', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['partner']	= iEurostat
		elif	re.search('flow', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['flow']	    = iEurostat
		elif	re.search('category', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['category']	= iEurostat
		elif	re.search('isco', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['isco']	    = iEurostat
		elif	re.search('post', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['post']	    = iEurostat
		elif	re.search('sector', listInput[iEurostat], flags=re.IGNORECASE):					
				dicEurostat['sector']	= iEurostat
		elif	re.search('currency', listInput[iEurostat], flags=re.IGNORECASE):				
				dicEurostat['unit']		=	iEurostat
		elif	re.search('entity', listInput[iEurostat], flags=re.IGNORECASE):				
				dicEurostat['entity']	=	iEurostat
		elif	re.search('item', listInput[iEurostat], flags=re.IGNORECASE):				
				dicEurostat['item']		=	iEurostat
		elif	re.search('isced', listInput[iEurostat], flags=re.IGNORECASE):				
				dicEurostat['indic']	=	iEurostat
	return dicEurostat
  
def defnoCountry(dicNoCountry,fileLog):
	for noCountry in dicNoCountry:
		fileLog.write(' Country code Eurostat not exist: '+noCountry+' in table Nation\n')
    
def defUselessCode(dicCode, fileLog):
	for code in dicCode:
		fileLog.write('The code ' + code + ' is available in the input but has not been processed.\n')
    
def	defDicNaceCheck(dicNaceCheck,dicNace,fileLog):
	naceTableDbSort =   list(list(dicNace.keys()))
	naceTableDbSort.sort()
	for naceTableDb	in naceTableDbSort:
		try:
			nace	=	dicNaceCheck[naceTableDb]
		except:
			fileLog.write('Nace : '+naceTableDb+' not exist in input file\n')
      
def	defVector(timeSerie):
	vector	  = []
	serie	  =	timeSerie
	for i in range(0,len(serie)): #on commence a l'annee la plus haute 
		element		= serie[i].strip() #on enleve les blanc avant et apres
		subelement  = re.sub('[" "]',';',element)#
		'''
		subelement  = re.sub('[" ",a-z]','#',element)#on traite aussi les cas 120 cpaie il va devenir 120.00000		
		subelement  = re.sub('#{1,}','.00000',subelement)#si plus de un : on met a zero cf cpuio eurostat
		subelement  = re.sub(':.00000',':',subelement)#on a parfois des cas comme : c 
		'''
		vector.append(subelement)
	return vector
  
def defVectorYears(timeSerie='', startYear='', endYear=''):
	vector	  = []
	serie	  =	timeSerie
	vector.append(endYear)#la premiere valeur du vecteur est l'annee la plus haute
	for i in range(0,len(serie)): #on commence a l'annee la plus haute 
		element		= serie[i].strip() #on enleve les blanc avant et apres	
		subelement  = re.sub('[" ",a-z]','',element)#on enleve les flag 
		vector.append(subelement)
	vector.append(startYear)#la derniere valeur du vecteur est l'annee la plus basse
	return vector	
  
def	defMinMaxYear(startYear=0,minStartYear=0,endYear=0,maxEndYear=0):
	if 	int(endYear) > int(maxEndYear):
		maxEndYear = int(endYear)
	if 	int(startYear) < int(minStartYear):
		minStartYear = int(startYear)
	return	minStartYear, maxEndYear 
  
def defDicStartValue(timeSerie,country,nace,indicator,dicStartValue,endYear):
	serie	  =	timeSerie
	for i in range(0,len(serie)): #on commence a l'annee la plus haute 
		element		= serie[i].strip()#on enleve les blanc avant et apres
		subelement  = re.sub('[a-z]','',element)#on enleve les flags eventuels
		subelement.strip()#on enleve les blanc avant et apres
		try:
			valeur	=	float(subelement)
		except:
			valeur	= 	-1						
		if	(valeur > 0) and (i > dicStartValue['startIndice']):
			dicStartValue['startIndice']	= 	i
			dicStartValue['startCountry'] 	= 	country
			dicStartValue['startNace']		=	nace
			dicStartValue['startIndicator']	= 	indicator
			dicStartValue['startValeur']	=	valeur
			dicStartValue['startYear']		=	int(endYear) - i
	return dicStartValue
  
def	defDicIndicator(country,nace,vector,dicIndicator):
	try:  				
		dicIndicator[country][nace]  = vector
	except:
		dicIndicator[country]        = {}
		dicIndicator[country][nace]  = vector
	return dicIndicator

def	defDicIndicators(country,indicator,vector,dicIndicator):
	try:  				
		dicIndicator[country][indicator]  = vector
	except:
		dicIndicator[country]        	  = {}
		dicIndicator[country][indicator]  = vector
	return dicIndicator

def	defDicFlow(country,flow,vector,dicIndicator):
	try:  				
		dicIndicator[country][flow]  = vector
	except:
		dicIndicator[country]        = {}
		dicIndicator[country][flow]  = vector
	return dicIndicator
  
def dicIndicatorTotal(country,nace,vector,dicIndicatorTotal):
	try:  				
		dicIndicatorTotal[country][nace]  = vector
	except:
		dicIndicatorTotal[country]        = {}
		dicIndicatorTotal[country][nace]  = vector
	return dicIndicatorTotal	
  
def defAllVector(oldVector,newVector):
	nbrEle		=	len(oldVector)
	#ON  TRAITE  LES FLAGS
	for i in range(1,nbrEle-1):#le 1er et le dernier element sont des years debut et fin
		lstOldVector	=	oldVector[i].split(';')
		lstNewVector	=	newVector[i].split(';')
		valOldVector	=	lstOldVector[0]
		valNewVector	=	lstNewVector[0]
		try:
			flgOldVector=	lstOldVector[1]
		except:
			flgOldVector=	''
		try:
			flgNewVector=	lstNewVector[1]
		except:
			flgNewVector=	''
		try:
			valOldVector=	float(lstOldVector[0])
			valNewVector=	float(lstNewVector[0])
			addValue	=	valOldVector + valNewVector
		except:
			addValue	=	valOldVector
		flags			=	flgOldVector + flgNewVector
		flags.strip()
		if	len(flags) > 0:
			valAdd			=	str(addValue) + ';' + flags
		else:
			valAdd			=	str(addValue)
		returnVector[i]	=	valAdd
		
	returnVector[0]		=	oldVector[0]#on rajoute l'annee de debut
	returnVector[-1]	=	oldVector[-1]#on rajoute l'annee de fin
	return returnVector	
  
def	defDicIndicatorSizeOld(country,nace,vector,indicator_size,dicIndicator):
	nbrEle		=	len(vector)
	ancienV		= []
	#for i in range(0,nbrEle): #on commence a l'annee la plus haute
	try:
		#print 'has_key  ',country,nace,vector,indicator_size, nbrEle
		print('has_key  ', country, nace, indicator_size, dicIndicator[country][nace])
		#print 'has_key complet ', dicIndicator[country][nace][indicator_size]
		ancienV = dicIndicator[country][nace][indicator_size]
		print('oldVector', ancienV)
		'''
		for	i in range(0,nbrEle):
			try:
				dicIndicator[country][nace][indicator_size][i] = dicIndicator[country][nace][indicator_size][i] + vector[i]
			except:
				dicIndicator[country][nace][indicator_size][i] = ':'
		'''
	except:
		try:
			dicIndicator[country][nace]						= {}
			dicIndicator[country][nace][indicator_size]		= vector
			print('has_key try ', country, nace, indicator_size, dicIndicator[country][nace][indicator_size])
			#print 'si le country existe pas',nace, country, indicator_size, i
		except:#si  country,nace, indicator_size existe pas
			dicIndicator[country]							= {}
			dicIndicator[country][nace]						= {}
			dicIndicator[country][nace][indicator_size]		= vector
			print('has_key EXCEPT ', country, nace, indicator_size, dicIndicator[country][nace][indicator_size])
	#if	indicator_size == 'emplsize_1To9':
		#print country,nace,vector,indicator_size,dicIndicator[country][nace][indicator_size]
	return dicIndicator
	
def	defDicIndicatorSize(country,nace,vector,indicator_size,dicIndicator):
	nbrEle		=	len(vector)
	#for i in range(0,nbrEle): #on commence a l'annee la plus haute 
	try:
		try:
			#oldVector = dicIndicator[country][nace][indicator_size]
			for	i in range(1,nbrEle-1):
				try:
					valueVector		=	float(vector[i])
					valueDic		=	float(dicIndicator[country][nace][indicator_size][i])
					dicIndicator[country][nace][indicator_size][i] = valueVector + valueDic
				except:
					dicIndicator[country][nace][indicator_size][i] = ':'
		except:
			dicIndicator[country][nace][indicator_size]	= vector
	except:#si le vecteur existe pas
		try:
			dicIndicator[country][nace]        				= {}
			dicIndicator[country][nace][indicator_size]		= vector			
			#print 'si le country existe pas',nace, country, indicator_size, i
		except:#si  country,nace, indicator_size existe pas
			dicIndicator[country]							= {}
			dicIndicator[country][nace]        				= {}
			dicIndicator[country][nace][indicator_size]		= vector			
	return dicIndicator

#fonction n'est plus utilisee, elle servait a creer un indicateur de niveau 1
#quand il n'existait uniquement qu'un de niveau deux
#ex: A10 et pas de A mais pas A10 et ensuite A20	
def	defNaceFail():
	dicNaceFail			=	spiLib.defDicNaceFail(dicNace)
	vector				=	[]
	try:
		vector      	=   dicIndicator[country][nace]
	except:
		nbrKey			=	dicNaceFail[nace]
		if	(nbrKey == 2):
			vector		=	previousVector
		else:
			fileLog.write('pas de code nace pays: '+str(country)+' nace = '+str(nace)+' nbrKey ='+str(nbrKey)+'\n')
			#continue #continues with the next iteration of the loop : next nace			
	previousVector	=	vector
  
def reverseAndNormalizeDicIndicatorSize(dicIndicator='', startYear='', endYear=''):
	'''la fonction prend un dictionnaire defini avec defVectorYears et retourne ce meme dictionnaire
	avec les vecteurs inverses, sans les annees de debut et fin et completes en debut et fin avec des valeurs
	vides le vas echeant'''
	valueStartYear 	= -1 
	valueEndYear	= -1
	vectorStart		= []
	vectorEnd		= []
	numberToRemove  = 0
	minStartYear	= int(startYear)#on aura besoin de l'annee de depart sous forme d'integer
	maxEndYear		= int(endYear)#de meme pour l'annee de fin
	countrySort     = list(dicIndicator.keys())
	countrySort.sort()
	for country in countrySort :
		naceSort    		=   list(dicIndicator[country].keys())
		naceSort.sort()
		for nace in naceSort:		
			sizeSort   		=   list(dicIndicator[country][nace].keys())
			sizeSort.sort()
			for size in sizeSort: #indicateur + size	
				vectorStart		= []#on reset ces valeurs pour chaque vecteur
				vectorEnd		= []
				valueStartYear 	= int(dicIndicator[country][nace][size][-1])#on isole les annees de debut et de fin de chaque vecteur
				valueEndYear	= int(dicIndicator[country][nace][size][0])
				vectorNew= dicIndicator[country][nace][size][1:-1]#on retire du vecteur les annees
				dicIndicator[country][nace][size]=vectorNew
				if 	valueEndYear > maxEndYear :
					numberToRemove = valueEndYear - maxEndYear
					del dicIndicator[country][nace][size][0:numberToRemove]
				if 	valueStartYear 	> minStartYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
					vectorStart 	= [':']*(valueStartYear - minStartYear)
				dicIndicator[country][nace][size].extend(vectorStart)#on ajoute les valeurs de depart definies au prealable
				dicIndicator[country][nace][size].reverse()#on inverse le vecteur
				if 	valueEndYear 	< maxEndYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
					vectorEnd		= [':']*(maxEndYear - valueEndYear)
				dicIndicator[country][nace][size].extend(vectorEnd)#on ajoute les valeurs de fin definies au prealable
				if 	valueStartYear < minStartYear :
					numberToRemove = minStartYear - valueStartYear
					del dicIndicator[country][nace][size][0:numberToRemove]
	return dicIndicator	
  
def reverseAndNormalizeDicIndicator(dicIndicator='', startYear='', endYear=''):
	'''la fonction prend un dictionnaire defini avec defVectorYears et retourne ce meme dictionnaire
	avec les vecteurs inverses, sans les annees de debut et fin et completes en debut et fin avec des valeurs
	vides le vas echeant'''
	valueStartYear 	= -1 
	valueEndYear	= -1
	vectorStart		= []
	vectorEnd		= []
	numberToRemove  = 0
	minStartYear	= int(startYear)#on aura besoin de l'annee de depart sous forme d'integer
	maxEndYear		= int(endYear)#de meme pour l'annee de fin
	countrySort     = list(dicIndicator.keys())
	countrySort.sort()	
	for country in countrySort :
		naceSort    		=   list(dicIndicator[country].keys())
		naceSort.sort()
		for nace in naceSort:#on boucle sur les vecteurs du dictionnaire
			vectorStart		= []#on reset ces valeurs pour chaque vecteur
			vectorEnd		= []
			valueStartYear 	= int(dicIndicator[country][nace][-1])#on isole les annees de debut et de fin de chaque vecteur
			valueEndYear	= int(dicIndicator[country][nace][0])
			if 	valueStartYear > minStartYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
				vectorStart = [':']*(valueStartYear - minStartYear)
			if 	valueEndYear < maxEndYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
				vectorEnd	= [':']*(maxEndYear - valueEndYear)
			del dicIndicator[country][nace][0]#on retire du vecteur les annees
			del dicIndicator[country][nace][-1]
			if 	valueEndYear > maxEndYear :
				numberToRemove = valueEndYear - maxEndYear
				del dicIndicator[country][nace][0:numberToRemove]
			dicIndicator[country][nace].extend(vectorStart)#on ajoute les valeurs de depart definies au prealable
			dicIndicator[country][nace].reverse()#on inverse le vecteur
			dicIndicator[country][nace].extend(vectorEnd)#on ajoute les valeurs de fin definies au prealable
			if 	valueStartYear < minStartYear :
				numberToRemove = minStartYear - valueStartYear
				del dicIndicator[country][nace][0:numberToRemove]
	return dicIndicator
  
def reverseAndNormalizeDicIndicators(dicIndicators='', startYear='', endYear=''):
	'''la fonction prend un dictionnaire defini avec defVectorYears et retourne ce meme dictionnaire
	avec les vecteurs inverses, sans les annees de debut et fin et completes en debut et fin avec des valeurs
	vides le vas echeant'''
	valueStartYear 	= -1 
	valueEndYear	= -1
	vectorStart		= []
	vectorEnd		= []
	numberToRemove  = 0
	minStartYear	= int(startYear)#on aura besoin de l'annee de depart sous forme d'integer
	maxEndYear		= int(endYear)#de meme pour l'annee de fin
	countrySort     = list(dicIndicators.keys())
	countrySort.sort()	
	for country in countrySort :
		indicatorSort    		=   list(dicIndicators[country].keys())
		indicatorSort.sort()
		for indicator in indicatorSort:#on boucle sur les vecteurs du dictionnaire
			vectorStart		= []#on reset ces valeurs pour chaque vecteur
			vectorEnd		= []
			valueStartYear 	= int(dicIndicators[country][indicator][-1])#on isole les annees de debut et de fin de chaque vecteur
			valueEndYear	= int(dicIndicators[country][indicator][0])
			if 	valueStartYear > minStartYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
				vectorStart = [':']*(valueStartYear - minStartYear)
			if 	valueEndYear < maxEndYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
				vectorEnd	= [':']*(maxEndYear - valueEndYear)
			del dicIndicators[country][indicator][0]#on retire du vecteur les annees
			del dicIndicators[country][indicator][-1]
			if 	valueEndYear > maxEndYear :
				numberToRemove = valueEndYear - maxEndYear
				del dicIndicators[country][indicator][0:numberToRemove]
			dicIndicators[country][indicator].extend(vectorStart)#on ajoute les valeurs de depart definies au prealable
			dicIndicators[country][indicator].reverse()#on inverse le vecteur
			dicIndicators[country][indicator].extend(vectorEnd)#on ajoute les valeurs de fin definies au prealable
			if 	valueStartYear < minStartYear :
				numberToRemove = minStartYear - valueStartYear
				del dicIndicators[country][indicator][0:numberToRemove]
	return dicIndicators
  
def reverseAndNormalizeDicNoIndicator(dicNoIndicator='', startYear='', endYear=''):
	'''la fonction prend un dictionnaire defini avec defVectorYears et retourne ce meme dictionnaire
	avec les vecteurs inverses, sans les annees de debut et fin et completes en debut et fin avec des valeurs
	vides le vas echeant'''
	valueStartYear 	= -1 
	valueEndYear	= -1
	vectorStart		= []
	vectorEnd		= []
	numberToRemove  = 0
	minStartYear	= int(startYear)#on aura besoin de l'annee de depart sous forme d'integer
	maxEndYear		= int(endYear)#de meme pour l'annee de fin
	countrySort     = list(dicNoIndicator.keys())
	countrySort.sort()	
	for country in countrySort :
		vectorStart		= []#on reset ces valeurs pour chaque vecteur
		vectorEnd		= []
		valueStartYear 	= int(dicNoIndicator[country][-1])#on isole les annees de debut et de fin de chaque vecteur
		valueEndYear	= int(dicNoIndicator[country][0])
		if 	valueStartYear > minStartYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
			vectorStart = [':']*(valueStartYear - minStartYear)
		if 	valueEndYear < maxEndYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
			vectorEnd	= [':']*(maxEndYear - valueEndYear)
		del dicNoIndicator[country][0]#on retire du vecteur les annees
		del dicNoIndicator[country][-1]
		if 	valueEndYear > maxEndYear :
			numberToRemove = valueEndYear - maxEndYear
			del dicNoIndicator[country][0:numberToRemove]
		dicNoIndicator[country].extend(vectorStart)#on ajoute les valeurs de depart definies au prealable
		dicNoIndicator[country].reverse()#on inverse le vecteur
		dicNoIndicator[country].extend(vectorEnd)#on ajoute les valeurs de fin definies au prealable
		if 	valueStartYear < minStartYear :
			numberToRemove = minStartYear - valueStartYear
			del dicNoIndicator[country][0:numberToRemove]
	return dicNoIndicator
  
def reverseAndNormalizeDicFlow(dicIndicator='', startYear='', endYear=''):
	'''la fonction prend un dictionnaire defini avec defVectorYears et retourne ce meme dictionnaire
	avec les vecteurs inverses, sans les annees de debut et fin et completes en debut et fin avec des valeurs
	vides le vas echeant'''
	valueStartYear 	= -1 
	valueEndYear	= -1
	vectorStart		= []
	vectorEnd		= []
	numberToRemove  = 0
	minStartYear	= int(startYear)#on aura besoin de l'annee de depart sous forme d'integer
	maxEndYear		= int(endYear)#de meme pour l'annee de fin
	countrySort     = list(dicIndicator.keys())
	countrySort.sort()	
	for country in countrySort :
		flowSort    		=   list(dicIndicator[country].keys())
		flowSort.sort()
		for flow in flowSort:#on boucle sur les vecteurs du dictionnaire
			vectorStart		= []#on reset ces valeurs pour chaque vecteur
			vectorEnd		= []
			valueStartYear 	= int(dicIndicator[country][flow][-1])#on isole les annees de debut et de fin de chaque vecteur
			valueEndYear	= int(dicIndicator[country][flow][0])
			if 	valueStartYear > minStartYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
				vectorStart = [':']*(valueStartYear - minStartYear)
			if 	valueEndYear < maxEndYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
				vectorEnd	= [':']*(maxEndYear - valueEndYear)
			del dicIndicator[country][flow][0]#on retire du vecteur les annees
			del dicIndicator[country][flow][-1]
			if 	valueEndYear > maxEndYear :
				numberToRemove = valueEndYear - maxEndYear
				del dicIndicator[country][flow][0:numberToRemove]
			dicIndicator[country][flow].extend(vectorStart)#on ajoute les valeurs de depart definies au prealable
			dicIndicator[country][flow].reverse()#on inverse le vecteur
			dicIndicator[country][flow].extend(vectorEnd)#on ajoute les valeurs de fin definies au prealable
			if 	valueStartYear < minStartYear :
				numberToRemove = minStartYear - valueStartYear
				del dicIndicator[country][flow][0:numberToRemove]
	return dicIndicator
  
def findMinimumYearWithActualData(timeSerie, startYear, minimumYearWithActualData):
	'''La fonction renvoie l'annee a partir de laquelle le vecteur presente des donnees exploitables'''
	actualStartYear = 0
	cpt=0
	for i in reversed(timeSerie) :
		if i.strip() != ':' :
			actualStartYear = startYear + cpt
			break
		cpt = cpt + 1
	if(actualStartYear<minimumYearWithActualData) :
		minimumYearWithActualData = actualStartYear
		
	return minimumYearWithActualData
  
def reverseAndNormalizeDic(dic, startYear, endYear):	
	'''la fonction prend n importe quel dictionnaire dont le dernier niveau est un vecteur de nombres
	dont la premiere et derniere valeur sont respectivement l annee de fin et l annee de depart. elle 
	retourne le meme dictionnaire avec les vecteurs inverses et les annees supprimees. elle normalise
	egalement ces vecteurs sur base d une annee de depart et une annee de fin fournie. les annes 
	doivent etre fournies en integer '''
	
	dicKeys = list(dic.keys())#tri des cles du dictionnaire au cas ou ca serait utile
	dicKeys.sort()
	
	for dicKey in dicKeys :
		if type(dic[dicKey]) is list: #si on a affaire a une liste, on est au dernier niveau, on peut donc proceder a l inversion du vecteur
			dic[dicKey] = reverseAndNormalizeVector(dic[dicKey], startYear, endYear)
		else :#sinon on a a nouveau affaire a un sous dictionnaire, on retourne dans la fonction recursivement
			dic[dicKey] = reverseAndNormalizeDic(dic[dicKey], startYear, endYear)
	
	return dic

def reverseAndNormalizeVector(vector, startYear, endYear):
	'''cette fonction inverse un vecteur dont la premiere valeur est l annee de fin et la derniere l annee
	de debut. elle retourne ce meme vecteur, normalise sur base des annee de debut et de fin passee en 
	parametre'''
	vectorStart		= []#initialisation des variable de comblement
	vectorEnd		= []
	valueStartYear 	= int(vector[-1])#on isole les annees de debut et de fin de chaque vecteur
	valueEndYear	= int(vector[0])
	if 	valueStartYear > startYear :#on cree les element a ajouter si l'annee de depart ne correspond pas a l'annee minimum
		vectorStart = [':']*(valueStartYear - startYear)
	if 	valueEndYear < endYear :#on cree les elements a ajouter si l'annee de fin n'est pas l'annee maximum
		vectorEnd	= [':']*(endYear - valueEndYear)
	del vector[0]#on retire du vecteur les annees
	del vector[-1]
	if 	valueEndYear > endYear :
		numberToRemove = valueEndYear - endYear
		del vector[0:numberToRemove]
	vector.extend(vectorStart)#on ajoute les valeurs de depart definies au prealable
	vector.reverse()#on inverse le vecteur
	vector.extend(vectorEnd)#on ajoute les valeurs de fin definies au prealable
	if 	valueStartYear < startYear :
		numberToRemove = startYear - valueStartYear
		del vector[0:numberToRemove]		
	
	return vector
  
def normalizeDicSize(dic, dicYear, refStartYear, refEndYear):
	for key in dic :
		if type(dic[key]) is list :
			dic[key] = normalizeVectorSize(dic[key], dicYear, refStartYear, refEndYear)
		else :
			dic[key] = normalizeDicSize(dic[key], dicYear, refStartYear, refEndYear)
	return dic

def normalizeVectorSize(vector, vectorStartYear, refStartYear, refEndYear):
	if len(vector) > 1 or vector[0] != '-':
		vectorStart		= []
		vectorEnd		= []
		vectorEndYear	= vectorStartYear + len(vector) - 1
		if vectorStartYear > refStartYear :
			vectorStart = [':']*(vectorStartYear - refStartYear)
		if 	vectorEndYear < refEndYear :
			vectorEnd	= [':']*(refEndYear - vectorEndYear)
		if vectorEndYear > refEndYear :
			numberToRemove = vectorEndYear - refEndYear
			del vector[-numberToRemove:]
		if 	vectorStartYear < refStartYear :
			numberToRemove = refStartYear - vectorStartYear
			del vector[0:numberToRemove]	
		vector = vector + vectorEnd
		vector = vectorStart + vector
	return vector
  
def	addValueMissing(dicIndicator, lstTotal, minStartYear):
	#vectorMissing	=	[':']*(maxEndYear - minStartYear)
	keyCountry		=	list(dicIndicator.keys())[0]
	keyNace			=	list(dicIndicator[keyCountry].keys())[0]
	vectorMissing	=	[':']*len(dicIndicator[keyCountry][keyNace])
	countrySort		=	list(dicIndicator.keys())
	countrySort.sort()
	for country in countrySort:
		#on balaie la liste des nace pour savoir s'il en manque dans le dic des indicateurs
		for nace	in lstTotal:
			try:
				valeurExistante				=	dicIndicator[country][nace]
			except:
				dicIndicator[country][nace] =	vectorMissing
	return dicIndicator
#25/02/2015 fonction ajoute des missing values d'Eurostat 
def	addValueMissingNace(dicIndicator, dicNace, minStartYear):
	#vectorMissing	=	[':']*(maxEndYear - minStartYear)
	keyCountry		=	list(dicIndicator.keys())[0]
	keyNace			=	list(dicIndicator[keyCountry].keys())[0]
	vectorMissing	=	[':']*len(dicIndicator[keyCountry][keyNace])
	countrySort		=	list(dicIndicator.keys())
	countrySort.sort()
	for country in countrySort:
		naceKeySort	=	list(list(dicNace.keys()))
		naceKeySort.sort()
		#on balaie la liste des nace pour savoir s'il en manque dans le dic des indicateurs
		for nace	in naceKeySort:
			try:
				valeurExistante				=	dicIndicator[country][nace]
			except:
				dicIndicator[country][nace] =	vectorMissing
	return dicIndicator	
def	addValueMissingSize(dicIndicator, lstTotal, minStartYear):
	#dicIndicator[country][nace][indicator_size]
	keyCountry		=	list(dicIndicator.keys())[0]
	keyNace			=	list(dicIndicator[keyCountry].keys())[0]
	vectorMissing	=	[':']*len(dicIndicator[keyCountry][keyNace])
	countrySort		=	list(dicIndicator.keys())
	countrySort.sort()
	for country in countrySort:
		#on balaie la liste pour le calcul des totaux des nace  
		#pour savoir s'il en manque dans le dic des indicateurs
		for nace	in lstTotal:
			try:
				valeurExistante				=	dicIndicator[country][nace]
			except:
				sizeLst	= list(dicIndicator[country][nace].keys())
				sizeLst.sort()
				for	size in sizeLst:
					dicIndicator[country][nace][size] =	vectorMissing
	return dicIndicator	