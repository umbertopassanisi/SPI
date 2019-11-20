import sys
import glob
import re
from . import DBConnect
from . import DBAccess
from . import spiLib
from . import spiLibTotal
from decimal import *

#-------------------------------------------------------------------------------------------##
#TRAITEMENT STRUCTURE  ET VAEMP
#TRAITEMENT COMPETITION RATE
#
def createTable(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,tableName,fileExt=''):
	lstTotal				=	spiLibTotal.defSelectLstTotal(nomenclature,compteEurostat,fileExt)
	#dicIndicator 			=	spiLib.addValueMissing(dicIndicator, dicNace, minStartYear)
	dicIndicator 			=	spiLib.addValueMissing(dicIndicator, lstTotal, minStartYear)
	startYear				=	minStartYear
	dicTotalNace			=	{}
	countrySort     		=   list(list(list(dicIndicator.keys())))
	countrySort.sort()	
	for country in countrySort:
		dicTotalNace[country]	=	{}
		naceSort    			=   list(dicIndicator[country].keys())
		naceSort.sort()
		for nace in naceSort:
			vector      	=   dicIndicator[country][nace]
			nbrVector		=	len(vector)
			#on renvoi le vector avec des vides rempli et l'indice de depart pour le total
			#qui correspond au nombre de vides rempli
			vectorElement	=	''
			vectorTotal		=	[':']*nbrVector
			for i in range(0,nbrVector):
				valeurVector  = vector[i].split(';')
				try:
					elementVector	=	float(valeurVector[0])
				except:
					elementVector	=	':'									
				try:
					flag			=	';'+valeurVector[1]
				except:
					flag			=	''					
				vectorElement		=	vectorElement + str(elementVector) + flag + ',' 					
				vectorTotal[i]		=	elementVector
			#calcul des totaux pour l'indicateur
			if 	lstTotal.count(nace):
				dicTotalNace = spiLibTotal.defTotalNace(dicTotalNace,indicatorSpi,nace,nomenclature,country,compteEurostat,vectorTotal,lstTotal,'',fileExt)
			#selection des code nace pour l'indicateur avant ecriture dans la base	
			if	nace in dicNace:
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorElement[:-1])
				#if	indicatorSpi == 'emp': #on cree aussi l'indicateur pour la table growth
					#DBAccess.majDBtable('growth','emp',country,str(startYear),nace,nomenclature,vectorElement[:-1])
	#write total nace, il n'est pas necessaire de selection les codes naces, ce sont uniquement les totaux
	defDicTotalNace(dicTotalNace,indicatorSpi,startYear,nomenclature,tableName)
	#on renvoie le dictionnaire des TOTAUX pour traiter les cas quand un indicateur
	#total derive d'un autre indicateur comme vabussh qui vient de vabus
	return dicTotalNace 
#
#traitement total Nace pour structure et competition rate
#pour les indicateurs simple ou primaire comme vabus
def defDicTotalNace(dicTotalNace,indicatorSpi,startYear,nomenclature,tableName):
	for country in dicTotalNace:
		for nace in dicTotalNace[country]:		
			nbrV			=	len(dicTotalNace[country][nace])
			vector			=	''
			for v in range(0,nbrV):
				valeurVector  		= 	str(dicTotalNace[country][nace][v])
				try:
					vectorOutput	=	float(valeurVector) #si le champ n'est pas numerique on met :
				except:
					vectorOutput	=	':'
				vector = vector + str(vectorOutput) + ','
			DBAccess.deleteRecTable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature)
			DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vector[:-1])	
#-------------------------------------------------------------------------------------------#
#TRAITEMENT DES TOTAUX POUR STRUCTURE  ET VAEMP
#pour les indicateurs qui derive d'une autre indicateur comme vabussh a partir de vabus
#dans cette fonction on ne recalcule plus les totaux (agregat), ils ont ete fait dans la fonction precedante
#createTable avec en retour le dictionnaire des agregats(dicTotalNace) que l'on passe en parametre				
def createTableTotal(nomenclature,dicTotalNace,dicIndicator,minStartYear,fileLog,dicNace,indicatorSpi,compteEurostat,tableName):
	startYear						=	minStartYear
	countrySort     				=   list(list(dicIndicator.keys()))
	countrySort.sort()
	for country in countrySort:
		totalCountryExist			=	1
		#total business economy
		if	nomenclature == 'nace1':
			try:
				vectorTotalNace		=	dicTotalNace[country]['C-K_X_J'] #cle du total par pays
			except:
				totalCountryExist	=	0
		else:
			try:
				vectorTotalNace		=	dicTotalNace[country]['B-N_X_K'] #cle du total par pays
			except:
				totalCountryExist	=	0		
		if	totalCountryExist:
			naceSort    			=   list(dicIndicator[country].keys())
			naceSort.sort()
			for nace in naceSort:
				vector      	=   dicIndicator[country][nace]
				#le retour de va est inutile dans ce cas
				vectorOutput,va	= 	defCalculAllVectors(vector,vectorTotalNace)
				#selection des code nace pour l'indicateur avant ecriture dans la base
				if	nace in dicNace:
					DBAccess.deleteRecTable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature)
					DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorOutput)		
		else:
			fileLog.write('no total for country : '+country+' nace : '+nomenclature+' indicator : '+indicatorSpi+'\n')
	#traitement des agregats
	defAgregatTableTotal(dicTotalNace,indicatorSpi,startYear,nomenclature,tableName)	
#pour le calcul des ratio pour les vecteurs style vabussh 	
def defCalculAllVectors(vector='',vectorTotalNace=''):
	nbrVector					=	len(vector)
	vectorElement				= 	''
	vectorFloat					=	[':']*nbrVector
	for i in range(0,nbrVector):
		try:
			valeurVector  		= 	vector[i].split(';')
			try:
				elementVector	=	float(valeurVector[0])
			except:
				elementVector	=	':'			
		except:#dans ce cas il est deja en float
			elementVector  		= 	vector[i]		
		#calcul du pourcentage pour chaque code nace
		try:
			valeurTotal  		= 	vectorTotalNace[i].split(';')
			try:
				elementTotal	=	float(valeurTotal[0])
			except:
				elementTotal	=	':'			
		except:#dans ce cas il est deja en float
			elementTotal  		= 	vectorTotalNace[i]
		if	elementTotal		==	0:
			elementResult		=	'~'
		else:
			try:
				elementResult	=	(elementVector / elementTotal) * 100					
			except:
				elementResult	=	':'
		try:
			flag				=	';'+valeurVector[1]
		except:
			flag				=	''			
		vectorElement			=	vectorElement + str(elementResult)+flag+ ','
		vectorFloat[i]			=	elementVector
	vector  					= 	vectorElement[:-1]
	return vector, vectorFloat
	
def defAgregatTableTotal(dicTotalNace,indicatorSpi,startYear,nomenclature,tableName):
	#write total nace
	for country in dicTotalNace:
		totalCountryExist		=	1
		if	nomenclature == 'nace1':
			try:
				vectorTotalNace		=	dicTotalNace[country]['C-K_X_J'] #cle du total par pays
			except:
				totalCountryExist	=	0
		else:
			try:
				vectorTotalNace		=	dicTotalNace[country]['B-N_X_K'] #cle du total par pays
			except:
				totalCountryExist	=	0		
		if	totalCountryExist:	
			for nace in dicTotalNace[country]:
				vector      	=   dicTotalNace[country][nace]
				#le retour de va est inutile dans ce cas
				vectorOutput,va	= 	defCalculAllVectors(vector,vectorTotalNace)
				DBAccess.deleteRecTable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature)
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorOutput)
#-------------------------------------------------------------------------------------------##
#TRAITEMENT STRUCTURE SIZE
#
def createTableSize(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,tableName,fileExt=''):
	#liste avec les codes naces a selectionner pour les totaux a calculer 
	#en fonction du nace(1 ou 2) et du code national nama ou sbs
	lstTotal				=	spiLibTotal.defSelectLstTotal(nomenclature,compteEurostat,fileExt)
	dicIndicator 			=	spiLib.addValueMissingSize(dicIndicator, lstTotal, minStartYear)	
	startYear				=	minStartYear
	dicAgregatNace			=	{}
	countrySort     		=   list(dicIndicator.keys())
	countrySort.sort()	
	keyTotal				=	indicatorSpi + '_TOTAL'
	for country in countrySort:
		dicAgregatNace[country]	=	{}
		#totalCountryExist		=	1
		naceSort    			=   list(dicIndicator[country].keys())
		naceSort.sort()
		for nace in naceSort:
			sizeSort    		=   list(dicIndicator[country][nace].keys())
			sizeSort.sort()
			try:
				vectorTotalNace	=	dicIndicator[country][nace][keyTotal] #cle du total par pays	
			except:
				fileLog.write('no total for country : '+country+' nace '+nace+' indicator '+indicatorSpi+'\n')
				continue
			for size in sizeSort: #indicateur + size
				vector      	=   dicIndicator[country][nace][size]
				vectorOutput,vectorAgregat	= 	defCalculAllVectors(vector,vectorTotalNace)
				#selection des code nace pour l'indicateur avant ecriture dans la base
				if	nace in dicNace: #on ne traite pas les totaux calculer
					DBAccess.majDBtable(tableName,size,country,str(startYear),nace,nomenclature,vectorOutput)
				#traitement des agregats on cree le dic par country et keyTotal(key des agregat)
				if 	lstTotal.count(nace):				
					sizeTotal	   = ':'+size #la notion de size doit se trouver dans le champ
					dicAgregatNace = spiLibTotal.defTotalNace(dicAgregatNace,indicatorSpi,nace,nomenclature,country,compteEurostat,vectorAgregat,lstTotal,sizeTotal,fileExt)
	defTableTotalSize(dicAgregatNace,indicatorSpi,startYear,nomenclature,tableName)
#
#traitement total des sizes
#
def defTableTotalSize(dicAgregatNace,indicatorSpi,startYear,nomenclature,tableName):
	for country in dicAgregatNace:
		naceSort    			=   list(dicAgregatNace[country].keys())
		naceSort.sort()		
		for nace in naceSort:#le nace arrive avec la size
			lstNace			= 	nace.split(':')	
			naceNoSize 		= 	lstNace[0]
			indicatorSize	= 	lstNace[1]			
			keyTotal		=	naceNoSize + ':' +indicatorSpi + '_TOTAL'
			vectorTotalNace	=	dicAgregatNace[country][keyTotal]
			vector			=	dicAgregatNace[country][nace]
			vectorOutput,va	= 	defCalculAllVectors(vector,vectorTotalNace)				
			DBAccess.majDBtable(tableName,indicatorSize,country,str(startYear),naceNoSize,nomenclature,vectorOutput)
#-------------------------------------------------------------------------------------------#
#TRAITEMENT GROWTH
#				
def defDicTotalNaceGrowth(dicTotalNace,indicatorSpi,startYear,nomenclature,tableName,growthTime):
	#write total nace
	vectorInit		=	''
	for i in range(0, growthTime):
		vectorInit = ':,' + vectorInit
	for country in dicTotalNace:
		for nace in dicTotalNace[country]:		
			nbrVector		=	len(dicTotalNace[country][nace])
			vector      	=   dicTotalNace[country][nace]
			vectorElement	=	vectorInit
			for i in range(growthTime,nbrVector):
				try:
					valeurVector	= float(vector[i]) #si le champ n'est pas numerique on met :
				except:
					valeurVector	= ':'					
				if	growthTime != 0:
					try:
						valeurVectorOld	= float(vector[i- growthTime])
						valeurVector 	= defGrowthTime(growthTime,valeurVector,valeurVectorOld)		
					except:
						valeurVector	= ':'					
				vectorElement = vectorElement + str(valeurVector) + ','
			DBAccess.deleteRecTable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature)
			DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorElement[:-1])
	
def createTableGrowth(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,tableName,G_Growth,fileExt=''):
	#24/02/2015 on exclu du total tous les indicateurs vak * de GROWTH
	lstTotal		=	()
	if	indicatorSpi[0:2] != 'va':
		lstTotal	=	spiLibTotal.defSelectLstTotal(nomenclature,compteEurostat,fileExt)
	#on complete les naces manquants avec les valeurs ':'
	dicIndicator 	=	spiLib.addValueMissing(dicIndicator, lstTotal, minStartYear)
	startYear		=	minStartYear
	growthTime		=	G_Growth
	dicTotalNace	=	{}
	vectorInit		=	''	
	for i in range(0, growthTime):
		vectorInit = ';,' + vectorInit
	countrySort     			=   list(dicIndicator.keys())
	countrySort.sort()	
	for country in countrySort:
		dicTotalNace[country]	=	{}
		naceSort    			=   list(dicIndicator[country].keys())
		naceSort.sort()
		for nace in naceSort:
			vector      	=   dicIndicator[country][nace]
			nbrVector		=	len(vector)
			#on renvoi le vector avec des vides rempli et l'indice de depart pour le total
			#qui correspond au nombre de vides rempli
			vectorTotal		=	[0.0]*nbrVector #pour le calcul des agregats		
			vectorElement	=	vectorInit
			for i in range(growthTime,nbrVector):
				valeurVectorLst  	= vector[i].split(';')								
				try:
					valeurVector	= float(valeurVectorLst[0])
				except:
					valeurVector	= ':'
				valeurAgregat		= valeurVector#on conserve la valeur pour le calcul de l'agregat
				if	growthTime != 0:
					valeurVectorOldLst  = vector[i- growthTime].split(';')
					try:
						valeurVectorOld	= float(valeurVectorOldLst[0])
						valeurVector 	= defGrowthTime(growthTime,valeurVector,valeurVectorOld)		
					except:
						valeurVector	= ':'						
				#element pour le calcul des agregats
				#on transmet aussi celui pour le temps (-1 ou -5) dans elementTotalTime				
				try:
					flag			=	';'+valeurVectorLst[1]
				except:
					flag			=	''					
				vectorElement		=	vectorElement + str(valeurVector) + flag + ',' 					
				vectorTotal[i]		=	valeurAgregat #pour calcul agregat venant du vecteur
				
			#calcul des totaux pour l'indicateur
			if 	lstTotal.count(nace):
				dicTotalNace   = spiLibTotal.defTotalNace(dicTotalNace,indicatorSpi,nace,nomenclature,country,compteEurostat,vectorTotal,lstTotal,'',fileExt)
			#selection des code nace pour l'indicateur avant ecriture dans la base	
			if	nace in dicNace:
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorElement[:-1])
	#write total nace, il n'est pas necessaire de selection les codes naces, ce sont uniquement les totaux
	#27/02/015 PAS de calcul d'agregat pour les volumes va*
	if	indicatorSpi[0:2] != 'va':
		defDicTotalNaceGrowth(dicTotalNace,indicatorSpi,startYear,nomenclature,tableName,growthTime)
	
def	defGrowthTime(growthTime=0,elementVector=':',elementVectorOld=':'):
	valueResult				= ':'
	valueCurrentTime		= elementVector
	valueOldTime			= elementVectorOld
	if	valueOldTime		==	0:
		valueResult			=	'~'
	else:
		try:
			exposant		= float(1.0/growthTime)
			valueResult		= (((valueCurrentTime / valueOldTime)**exposant) - 1) * 100
		except:
			valueResult		=	':'
	return 	valueResult
						
#-------------------------------------------------------------------------------------------#
#TRAITEMENT NE
#	
def createTableNE(nomenclature='',dicNation='',endYear='',fileLog='',indicatorSpi='',compteEurostat='',tableName='',dicsize=''):
	#liste avec les codes naces NE on creer un record avec la valeur '-' comme vecteur
	dicNaceNE					= 	spiLib.defSelectdicNaceNE(nomenclature,compteEurostat)
	countrySort     			=   list(dicNation.keys())
	countrySort.sort()	
	keyTotal					=	indicatorSpi + '_TOTAL'
	for country in countrySort:
		naceSort    			=   list(dicNaceNE.keys())
		naceSort.sort()
		for nace in naceSort:
			try:#dans le cas des indicateurs avec une size
				sizeLst	    	=   list(dicsize.values())
				sizeSort		=	set(sizeLst) #valeur unique
				list(sizeSort)	# a convertir en list	
				for	size in sizeSort:
					indicatorSize =	indicatorSpi + '_' + size					
					DBAccess.majDBtable(tableName,indicatorSize,country,str(endYear),nace,nomenclature,'-')
			except:	#si pas de size			
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(endYear),nace,nomenclature,'-')
        
def createTableSkillTech(nomenclature, dicIndicator, startYear, fileLog, tableName):
	dicAggr   = {}
	dicAggr   = spiLibTotal.defDicSkillTech(nomenclature, dicAggr)
	dicTot    = {}
	dicVash   = {}

	for country in dicIndicator :
		dicTot[country] = {}
		for type in dicAggr :
			for aggr in dicAggr[type] :
				dicTot[country][aggr] = []
				for code in dicAggr[type][aggr] :
					if dicTot[country][aggr] == [] :
						try:
							for i in range(0, len(dicIndicator[country][code])):
								dicTot[country][aggr].append(dicIndicator[country][code][i])
						except:
							dicTot[country][aggr] = [':']
					else :
						for i in range(0, len(dicTot[country][aggr])) :
							a = ':'
							b = ':'
							try : 
								a = float(dicTot[country][aggr][i])
							except :
								pass
							try :
								b = float(dicIndicator[country][code][i])
							except : 
								pass
							if a != ':' and b != ':' :
								dicTot[country][aggr][i] = '{0:.8f}'.format(a + b)
							else : 
								dicTot[country][aggr][i] = ':'
			
	vectorTotalEU = {}
	if nomenclature == 'nace1' :
		try:
			vectorTotalEU['EU27'] = dicIndicator['EU27']['TOTAL']
		except:
			fileLog.write('no eurostat total for EU27\n')
	if nomenclature == 'nace2' :		
		try:
			vectorTotalEU['EU28'] = dicIndicator['EU28']['TOTAL']
		except:
			fileLog.write('no eurostat total for EU28\n')
	
	for country in dicIndicator :
		try:
			vectorTotal = dicIndicator[country]['TOTAL']
		except:
			fileLog.write('no eurostat total for country : '+ country + '\n')
			continue
		for type in dicAggr :
			for aggr in dicAggr[type] :
				try:
					vectorAggr = dicTot[country][aggr]
				except:
					fileLog.write('no eurostat ' + aggr + ' for country : ' + country + '\n')
					break
				vectorResultVash = []
				vectorResultVasp = {}
				for eu in vectorTotalEU :
					vectorResultVasp[eu] = []
				for i in range(0, len(vectorTotal)) :
					a = ':'
					b = ':'
					try : 
						b = float(vectorTotal[i])
					except :
						pass
					try :
						a = float(vectorAggr[i])
					except :
						pass
					if a == ':' or b == ':' :
						vectorResultVash.append(':')
					else :
						vectorResultVash.append(str(round((a/b)*100, 5)))
					for eu in vectorTotalEU :
						c = ':'
						d = ':'
						try : 
							c = float(dicTot[eu][aggr][i])
						except :
							pass
						try :
							d = float(vectorTotalEU[eu][i])
						except :
							pass
						if a == ':' or b == ':' or c == ':' or d == ':' :
							vectorResultVasp[eu].append(':')
						else :
							vectorResultVasp[eu].append(str(round((a/b)/(c/d), 5)))
				if len(vectorResultVash) > 0 :
					DBAccess.majDBtable(tableName,type + 'vash_' + aggr,country,str(startYear),'default',nomenclature, ','.join(vectorResultVash))
				for eu in vectorTotalEU :
					if len(vectorResultVasp[eu]) > 0 :
						DBAccess.majDBtable(tableName,type + 'vaspeu_' + aggr,country,str(startYear),'default',nomenclature, ','.join(vectorResultVasp[eu]))
            
def createTableCountryLevelOpen(dicIndicators, startYear, fileLog, tableName):
	res    = []
	gdp    = []
	x      = []
	m	   = []
	for country in dicIndicators :
		gdp    = []
		x      = []
		m	   = []
		res = []
		try : 
			gdp = dicIndicators[country]['B1GQ']
		except :
			pass
		try :
			x   = dicIndicators[country]['P6']
		except :
			pass
		try :
			m   = dicIndicators[country]['P7']
		except :
			pass
		
		if not gdp  or not x or not m :
			fileLog.write('no data for country : '+ country + '\n')
			continue 
		else :
			for i in range(0, len(gdp)) :
				if gdp[i] == ':' or x[i] == ':' or m[i] == ':' :
					res.append(':')
				else :
					resCalc = ((float(x[i])+float(m[i]))/(2*float(gdp[i])))*100
					res.append(str(resCalc))
		DBAccess.majDBtable(tableName,'open',country,str(startYear),'default','default', ','.join(res))
    
def createTableCountryLevelEduTech(dicIndicator, spiIndicator,startYear, filelog, tableName):
	for country in dicIndicator :
		DBAccess.majDBtable(tableName, spiIndicator, country, str(startYear), 'default', 'default', ','.join(dicIndicator[country]))
    
def createTableCountryLevelFdi(dicIndicator,dicGdp, spiIndicator,startYear,fileLog,tableName):
	res    = []
	fdi    = []
	gdp    = []
	
	for country in dicIndicator :
		res = []
		gdp = []
		fdi = dicIndicator[country]
		
		try :
			gdp = dicGdp[country]
		except :
			fileLog.write('No gdp data for country' + country + '\n')
			continue
		
		for i in range(0, len(fdi)) :
			if gdp[i] == ':' or fdi[i] == ':' :
				res.append(':')
			else :
				res.append(str((float(fdi[i])/float(gdp[i]))*100))
		
		DBAccess.majDBtable(tableName,spiIndicator,country,str(startYear),'default','default', ','.join(res))
    
def createTableCountryLevelBtechBtechgdp(dicIndicator,dicGdp, startYear,fileLog,tableName):
	res    = []
	resGdp = []
	x      = []
	m      = []
	gdp    = []
	for country in dicIndicator :
		gdp    = []
		x      = []
		m	   = []
		res    = []
		resGdp = []
		try : 
			gdp = dicGdp[country]
		except :
			pass
		try :
			x   = dicIndicator[country]['EXP']
		except :
			pass
		try :
			m   = dicIndicator[country]['IMP']
		except :
			pass
		
		if not x or not m :
			fileLog.write('no btech data for country : '+ country + '\n')
			continue
		else :
			if not gdp :
				fileLog.write('no btechgdp data for country : '+ country + '\n')
				
			for i in range(0, len(x)) :
				if x[i] == ':' or m[i] == ':' :
					res.append(':')
					resGdp.append(':')
				else :
					resCalc = float(x[i])-float(m[i])
					res.append(str(resCalc))
					
					if gdp :
						try:
							resCalcGdp = (resCalc/float(gdp[i]))*100
							resGdp.append(str(resCalcGdp))
						except:
							resGdp.append(':')
						
		DBAccess.majDBtable(tableName,'btech',country,str(startYear),'default','default', ','.join(res))
		if gdp :
			DBAccess.majDBtable(tableName,'btechgdp',country,str(startYear),'default','default', ','.join(resGdp))
      
def createTableNaceRatio(nomenclature, dicIndicatorA, dicIndicatorB, indicator, startYear, fileLog, tableName) :
	'''this function creates database records that are the result of a ratio : indicator A over indicator B'''
	
	res = []
	a   = []
	b   = []
	
	for country in dicIndicatorA : 
		for nace in dicIndicatorA[country] :
			res = []
			a   = []
			b   = []
			
			try :
				a = dicIndicatorA[country][nace]
			except : 
				continue
			try :
				b = dicIndicatorB[country][nace]
			except : 
				continue
			for i in range(0, len(a)) :
				if a[i] == ':' or b[i] == ':' :
					res.append(':')
				elif float(b[i]) == 0 :
					res.append('~')
				else :
					res.append(str(float(a[i])/float(b[i])))
						
			DBAccess.majDBtable(tableName, indicator, country, str(startYear), nace, nomenclature, ','.join(res))
      
def createTableNacePercentage(nomenclature, dicIndicatorA, dicIndicatorB, indicator, startYear, fileLog, tableName) :
	'''this function creates database records that are the result of a ratio : indicator A over indicator B'''
	
	res = []
	a   = []
	b   = []
	
	for country in dicIndicatorA : 
		for nace in dicIndicatorA[country] :
			res = []
			a   = []
			b   = []
			
			try :
				a = dicIndicatorA[country][nace]
			except : 
				continue
			try :
				b = dicIndicatorB[country][nace]
			except : 
				continue
			for i in range(0, len(a)) :
				if a[i] == ':' or b[i] == ':' :
					res.append(':')
				elif float(b[i]) == 0 :
					res.append('~')
				else :
					res.append(str((float(a[i])/float(b[i]))*100))
						
			DBAccess.majDBtable(tableName, indicator, country, str(startYear), nace, nomenclature, ','.join(res))	
      
def createTableNaceGrowth(nomenclature, dicIndicator, indicator, startYear, growthTime, fileLog, tableName) :
	res = []
	ref = []
	
	for country in dicIndicator :
		for nace in dicIndicator[country] :
			res = []
			ref = dicIndicator[country][nace]
			if ref[0] != '-' :
				for i in range(growthTime, len(ref)) :
					current = ref[i]
					old		= ref[i - growthTime]
					if current == ':' or old == ':' :
						res.append(':')
					elif current == '~' or old == '~' :
						res.append(':')
					else :
						res.append(str(defGrowthTime(growthTime, float(current), float(old))))
				DBAccess.majDBtable(tableName, indicator, country, str(startYear + growthTime), nace, nomenclature, ','.join(res))
			else :
				DBAccess.majDBtable(tableName, indicator, country, str(startYear + growthTime), nace, nomenclature, '-')
        
def	defGrowthTime(growthTime=0,elementVector=':',elementVectorOld=':'):
	valueResult				= ':'
	valueCurrentTime		= elementVector
	valueOldTime			= elementVectorOld		 			 
	try:
		exposant			= float(1.0/growthTime)
		valueResult			= (((valueCurrentTime / valueOldTime)**exposant) - 1) * 100
	except:
		valueResult		=	':'
	return 	valueResult
  
def createTableExternalXM(indicator, nomenclature, minYear, dicIndicator, tableName, fileLog):
	
	for country in dicIndicator:
		for code in dicIndicator[country]:
			res = []
			refIntra = {}
			refExtra = {}
			
			try :
				refIntra = dicIndicator[country][code]['EU27_INTRA']
			except: 
				fileLog.write('Missing intra EU27 reference for country ' + country + ' and code ' + code + '.\n')
				continue
			
			try :
				refExtra = dicIndicator[country][code]['EU27_EXTRA']
			except: 
				fileLog.write('Missing extra EU27 reference for country ' + country + ' and code ' + code + '.\n')
				continue
			
			for i in range(0, len(refIntra)):
				if refIntra[i] == ':' or refExtra[i] == ':':
					res.append(':')
				else:
					res.append(str((int(refIntra[i]) + int(refExtra[i]))))
			DBAccess.majDBtable(tableName, indicator, country, str(minYear), code, nomenclature, ','.join(res))
      
def createTableDomesticIndex(nomenclature, dicIndicatorA, dicIndicatorB, indicator, startYear, baseYear, fileLog, tableName) :
	
	res = []
	a   = []
	b   = []
	if startYear <= baseYear:
		indexYear = baseYear - startYear #l annee de debut doit etre inferieure a l annee sur laquelle se base l'index sinon ca n a pas d interet
	else:
		fileLog.write('The start year is above the index year, the computation is impossible.')
		sys.exit()
	
	for country in dicIndicatorA : 
		for nace in dicIndicatorA[country] :
			res = []
			a   = []
			b   = []
			try :
				a = dicIndicatorA[country][nace]
			except : 
				continue
			try :
				b = dicIndicatorB[country][nace]
			except : 
				continue
			for i in range(0, len(a)):
				if a[i] == ':' or b[i] == ':' :
					res.append(':')
				elif float(b[i]) == 0 :
					res.append('~')
				else :
					res.append(float(a[i])/float(b[i]))
			
			refYear = res[indexYear]
			
			for i in range(0, len(res)):
				if res[i] == ':' or refYear == ':':
					res[i] = ':'
				elif res[i] == '~' or refYear == '~':
					res[i] = '~'
				elif refYear == 0:
					res[i] = '~'
				else :
					res[i] = str((res[i]/refYear)*100)
						
			DBAccess.majDBtable(tableName, indicator, country, str(startYear), nace, nomenclature, ','.join(res))
      
def createTableExternalTbalRtbal(nomenclature, dicX, dicM, startYear, fileLog, tableName):
	
	tbal = []
	rtbal = []
	x = []
	m = []
	
	for country in dicX:
		for code in dicX[country]:
			tbal = []
			rtbal = []
			x = dicX[country][code]
			try:
				m = dicM[country][code]
			except:
				continue
			for i in range(0, len(x)):
				if x[i] == ':' or m[i] == ':':
					tbal.append(':')
					rtbal.append(':')
				else:
					tmp = float(x[i]) - float(m[i])
					tbal.append('{0:.8f}'.format(tmp))
					tmp = float(tmp)/(float(x[i]) + float(m[i]))
					rtbal.append('{0:.8f}'.format(tmp))		
			DBAccess.majDBtable(tableName, 'tbal', country, str(startYear), code, nomenclature, ','.join(tbal))
			DBAccess.majDBtable(tableName, 'rtbal', country, str(startYear), code, nomenclature, ','.join(rtbal))
      
def createTableTradeTrbalRbal(nomenclature, dicX, dicM, startYear, fileLog, tableName):
	
	trbal = []
	rbal = []
	x = []
	m = []
	
	for country in dicX:
		for code in dicX[country]:
			trbal = []
			rbal = []
			x = dicX[country][code]
			try:
				m = dicM[country][code]
			except:
				continue
			for i in range(0, len(x)):
				if x[i] == ':' or m[i] == ':':
					trbal.append(':')
					rbal.append(':')
				else:
					tmp = float(x[i]) - float(m[i])
					trbal.append('{0:.8f}'.format(tmp))
					try: 
						tmp = float(tmp)/(float(x[i]) + float(m[i]))
						rbal.append('{0:.8f}'.format(tmp))	
					except:
						rbal.append('~')	
			DBAccess.majDBtable(tableName, 'trbal', country, str(startYear), code, nomenclature, ','.join(trbal))
			DBAccess.majDBtable(tableName, 'rbal', country, str(startYear), code, nomenclature, ','.join(rbal))
      
def createTableExternalCrtbal(nomenclature, dicX, dicM, startYear, fileLog, tableName):
	crtbal = []
	x = []
	m = []
	xtotal = []
	mtotal = []
	
	for country in dicX:
		for code in dicX[country]:
			if code != 'TOTAL':
				crtbal = []
				x = dicX[country][code]
				try:
					m = dicM[country][code]
				except:
					continue
				try:
					xtotal = dicX[country]['TOTAL']
				except:
					continue
				try:
					mtotal = dicM[country]['TOTAL']
				except:
					continue
				
				for i in range(0, len(x)):
					if x[i] == ':' or m[i] == ':' or xtotal[i] == ':' or mtotal[i] == ':' :
						crtbal.append(':')
					else:
						xi = float(x[i])
						mi = float(m[i])
						xtotali = float(xtotal[i])
						mtotali = float(mtotal[i])
						try:
							crtbal.append('{0:.8f}'.format(((xi-mi)/(xi+mi))*((xi+mi)/(xtotali+mtotali))))
						except:
							crtbal.append('~')
				
				DBAccess.majDBtable(tableName, 'crtbal', country, str(startYear), code, nomenclature, ','.join(crtbal))
        
def createTableExternalXMShare(indicator, nomenclature, minYear, dicIndicator, tableName, fileLog):
	
	res = []
	ref = {}
	refTotal = {}
	for country in dicIndicator:
		try :
			refTotal = dicIndicator[country]['TOTAL']
		except: 
			fileLog.write('Missing TOTAL reference for country ' + country + '.\n')
			continue
		for code in dicIndicator[country]:
			if code != 'TOTAL':
				res = []
				ref = dicIndicator[country][code]
	
				for i in range(0, len(ref)):
					if ref[i] == ':' or refTotal[i] == ':':
						res.append(':')
					elif float(refTotal[i]) == 0:
						res.append('~')
					else:
						res.append(str((float(ref[i])/float(refTotal[i]))*100))
				DBAccess.majDBtable(tableName, indicator, country, str(minYear), code, nomenclature, ','.join(res))
        
def createTableExternalSpecialisation(indicator, nomenclature, dicIndicator, startYear, reference, fileLog, tableName):
	res = []
	refNum = []
	refDen = []
	
	for country in dicIndicator:
		for code in dicIndicator[country]:
			res = []
			refNum = dicIndicator[country][code]
			try:
				refDen = dicIndicator[reference][code]
			except:
				fileLog.write('No ' + reference + ' for code ' + code + ' and country ' + country + ' .\n')
				continue
			for i in range(0,len(refNum)):
				if refDen[i] == ':' or refNum[i]==':':
					res.append(':')
				elif refDen[i] == '~' or refNum[i] == '~':
					res.append('~')
				else:
					res.append('{0:.8f}'.format(((float(refNum[i])/100)/(float(refDen[i])/100))))
			DBAccess.majDBtable(tableName, indicator, country, str(startYear), code, nomenclature, ','.join(res))
      
def createTableNomenclatureBasic(dicIndicator, indicator, nomenclature, startYear, tableName):
	for country in dicIndicator:
		for code in dicIndicator[country]:
			DBAccess.majDBtable(tableName, indicator, country, str(startYear), code, nomenclature, ','.join(dicIndicator[country][code]))
			
def createTableNomenclaturePartner(dicIndicator, indicator, nomenclature, startYear, tableName):
	for country in dicIndicator:
		for code in dicIndicator[country]:
			for partner in dicIndicator[country][code]:
				DBAccess.majDBtableGeo(tableName, indicator, country, str(startYear), code, nomenclature, ','.join(dicIndicator[country][code][partner]), partner)
        
def createTableExternalGeoShare(nomenclature, dicWorld, dicDestor, indicator, startYear, fileLog, tableName):
	res = []
	refNum = []
	refDen = []
	
	for country in dicDestor:
		for code in dicDestor[country]:
			try:
				refDen = dicWorld[country][code]
			except:
				fileLog.write('No world data for code ' + code + ' and country ' + country + ' .\n')
				continue
			for partner in dicDestor[country][code]:
				res = []
				refNum = dicDestor[country][code][partner]
				
				for i in range(0,len(refNum)):
					if refDen[i] == ':' or refNum[i]==':':
						res.append(':')
					elif refDen[i] == '~' or refNum[i] == '~' or float(refDen[i]) == 0:
						res.append('~')
					else:
						res.append('{0:.8f}'.format(float(refNum[i])/float(refDen[i])))
				DBAccess.majDBtableGeo(tableName, indicator, country, str(startYear), code, nomenclature, ','.join(res), partner)
        
def createTableCompetitionOpen(nomenclature, dicVa, dicX, dicM, startYear, fileLog, tableName):
	res = []
	refX = []
	refM = []
	refVa = []
	for country in dicVa: 
		for code in dicVa[country]:
			res = []
			refVa = dicVa[country][code]
			try:
				refX = dicX[country][code]
				refM = dicM[country][code]
			except:
				fileLog.write('No export or import data for code ' + code + ' and country ' + country + '.\n')
				continue
			for i in range(0,len(refVa)):
				if refVa[i] == ':' or refX[i] == ':' or refM[i] == ':':
					res.append(':')
				elif refVa[i] == '~' or refX[i] == '~' or refM[i] == '~' or float(refVa[i]) == 0 :
					res.append('~')
				else:
					res.append('{0:.8f}'.format((float(refX[i])+float(refM[i]))/(2*float(refVa[i])*1000000)))
			DBAccess.majDBtable(tableName, 'open', country, str(startYear), code, nomenclature, ','.join(res))
      
def createTableCompetitionImportpen(nomenclature, dicGO, dicX, dicM, startYear, fileLog, tableName):
	res = []
	refX = []
	refM = []
	refGO = []
	for country in dicGO:
		for code in dicGO[country]:
			res = []
			refGO = dicGO[country][code]
			try:
				refX = dicX[country][code]
				refM = dicM[country][code]
			except:
				fileLog.write('No export or import data for code ' + code + ' and country ' + country + '.\n')
				continue
			
			for i in range(0, len(refGO)):
				if refGO[i] == ':' or refX[i] == ':' or refM[i] == ':':
					res.append(':')
				elif refGO[i] == '~' or refX[i] == '~' or refM[i] == '~' :
					res.append('~')
				else :
					ac = float(refGO[i])*1000000 + float(refM[i]) - float(refX[i])
					try:
						res.append('{0:.8f}'.format(float(refM[i])/ac))
					except:
						res.append('~')
			DBAccess.majDBtable(tableName, 'importpen', country, str(startYear), code, nomenclature, ','.join(res))
			
def createTableTotalShare(dicIndicator, startYear, indicator, nomenclature, fileLog, tableName):
	res = []
	total = []
	ref = []
	
	for country in dicIndicator :
	    try : 
	        total = dicIndicator[country]['TOTAL']
	    except :
	        fileLog.write('No total for country + ' + country + '\n');
	        continue
	    
	    for code in dicIndicator[country] :
	    	res = []
	        ref = dicIndicator[country][code]	
	        
        	for i in range(0, len(ref)) :
        		try :
        			curTotal = total[i]
        		except :
        			res.append(':')
        			continue
        		
        		if ref[i] == ':' or curTotal == ':' :
        			res.append(':')
        		elif ref[i] == '~' or curTotal == '~' or float(curTotal) == 0:
        			res.append('~')
        		else :	 
        			res.append('{0:.8f}'.format((float(ref[i])/float(curTotal))*100))   
        	
        	DBAccess.majDBtable(tableName, indicator, country, str(startYear), code, nomenclature, ','.join(res))    

def createTableOverOtherShare(dicNumerator, dicDenominator, startYear, indicator, nomenclature, tableName):	
	for country in dicNumerator :
		for code in dicNumerator[country] :
			res = []
			for i, value in enumerate(dicNumerator[country][code]) :
				try :
					numerator = float(value)
					denominator = float(dicDenominator[country][code][i])
					share = str(round((numerator/denominator)*100, 8))
				except (ValueError, KeyError) :
					share = ':'
				except ZeroDivisionError :
					share = '~'
				
				res.append(share)
				
			DBAccess.majDBtable(tableName, indicator, country, str(startYear), code, nomenclature, ','.join(res))
					
				
				
				
	