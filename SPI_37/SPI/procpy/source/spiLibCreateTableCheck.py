import sys
import glob
import re
import DBConnect
import DBAccessCheck
import spiLib
import spiLibTotal
import pprint

#-------------------------------------------------------------------------------------------##
#TRAITEMENT STRUCTURE  ET VAEMP
#TRAITEMENT COMPETITION RATE
#
def createTable(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,tableName):
	lstTotal				=	spiLibTotal.defSelectLstTotal(nomenclature,compteEurostat)
	startYear				=	minStartYear
	dicTotalNace			=	{}
	countrySort     		=   dicIndicator.keys() 
	countrySort.sort()	
	for country in countrySort:
		dicTotalNace[country]	=	{}
		naceSort    			=   dicIndicator[country].keys()
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
				dicTotalNace = spiLibTotal.defTotalNace(dicTotalNace,indicatorSpi,nace,nomenclature,country,compteEurostat,vectorTotal,lstTotal)			
			
			#selection des code nace pour l'indicateur avant ecriture dans la base	
			if	dicNace.has_key(nace):
				print indicatorSpi,',',country,',',str(startYear),',',nace,',',nomenclature,',',vectorElement[:-1]
				
				DBAccessCheck.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorElement[:-1])
				'''
				if	indicatorSpi == 'emp': #on cree aussi l'indicateur pour la table growth
					DBAccess.majDBtable('growth','empl',country,str(startYear),nace,nomenclature,vectorElement[:-1])
				'''
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
			DBAccessCheck.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vector[:-1])	
#-------------------------------------------------------------------------------------------#
#TRAITEMENT DES TOTAUX POUR STRUCTURE  ET VAEMP
#pour les indicateurs qui derive d'une autre indicateur comme vabussh a partir de vabus
#dans cette fonction on ne recalcule plus les totaux (agregat), ils ont ete fait dans la fonction precedante
#createTable avec en retour le dictionnaire des agregats(dicTotalNace) que l'on passe en parametre				
def createTableTotal(nomenclature,dicTotalNace,dicIndicator,minStartYear,fileLog,dicNace,indicatorSpi,compteEurostat,tableName):
	startYear						=	minStartYear
	countrySort     				=   dicIndicator.keys() 
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
			naceSort    			=   dicIndicator[country].keys()
			naceSort.sort()
			for nace in naceSort:
				vector      	=   dicIndicator[country][nace]
				#le retour de va est inutile dans ce cas
				vectorOutput,va	= 	defCalculAllVectors(vector,vectorTotalNace)
				#selection des code nace pour l'indicateur avant ecriture dans la base
				if	dicNace.has_key(nace):
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
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorOutput)
#-------------------------------------------------------------------------------------------##
#TRAITEMENT STRUCTURE SIZE
#
def createTableSize(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,tableName):
	#liste avec les codes naces a selectionner pour les totaux a calculer 
	#en fonction du nace(1 ou 2) et du code national nama ou sbs
	lstTotal				=	spiLibTotal.defSelectLstTotal(nomenclature,compteEurostat)
	startYear				=	minStartYear
	dicAgregatNace			=	{}
	countrySort     		=   dicIndicator.keys() 
	countrySort.sort()	
	keyTotal				=	indicatorSpi + '_TOTAL'
	for country in countrySort:
		totalCountryExist		=	1
		naceSort    			=   dicIndicator[country].keys()
		naceSort.sort()
		for nace in naceSort:
			sizeSort    		=   dicIndicator[country][nace].keys()
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
				if	dicNace.has_key(nace): #on ne traite pas les totaux calculer
					DBAccess.majDBtable(tableName,size,country,str(startYear),nace,nomenclature,vectorOutput)
				#traitement des agregats on cree le dic par country et keyTotal(key des agregat)
				if 	lstTotal.count(nace):				
					sizeTotal	   = ':'+size #la notion de size doit se trouver dans le champ
					dicAgregatNace = spiLibTotal.defTotalNace(dicAgregatNace,indicatorSpi,nace,nomenclature,country,compteEurostat,vectorAgregat,lstTotal,sizeTotal)
	defTableTotalSize(dicAgregatNace,indicatorSpi,startYear,nomenclature,tableName)
#
#traitement total des sizes
#
def defTableTotalSize(dicAgregatNace,indicatorSpi,startYear,nomenclature,tableName):
	for country in dicAgregatNace:
		naceSort    			=   dicAgregatNace[country].keys()
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
			DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorElement[:-1])
	
def createTableGrowth(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,tableName,G_Growth):
	lstTotal		=	spiLibTotal.defSelectLstTotal(nomenclature,compteEurostat)
	startYear		=	minStartYear
	growthTime		=	G_Growth
	dicTotalNace	=	{}
	vectorInit		=	''	
	for i in range(0, growthTime):
		vectorInit = ';,' + vectorInit
	countrySort     			=   dicIndicator.keys() 
	countrySort.sort()	
	for country in countrySort:
		dicTotalNace[country]	=	{}
		naceSort    			=   dicIndicator[country].keys()
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
				dicTotalNace   = spiLibTotal.defTotalNace(dicTotalNace,indicatorSpi,nace,nomenclature,country,compteEurostat,vectorTotal,lstTotal)
			#selection des code nace pour l'indicateur avant ecriture dans la base	
			if	dicNace.has_key(nace):	
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(startYear),nace,nomenclature,vectorElement[:-1])
	#write total nace, il n'est pas necessaire de selection les codes naces, ce sont uniquement les totaux
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
	countrySort     			=   dicNation.keys() 
	countrySort.sort()	
	keyTotal					=	indicatorSpi + '_TOTAL'
	for country in countrySort:
		naceSort    			=   dicNaceNE.keys()
		naceSort.sort()
		for nace in naceSort:
			try:#dans le cas des indicateurs avec une size
				sizeLst	    	=   dicsize.values()
				sizeSort		=	set(sizeLst) #valeur unique
				list(sizeSort)	# a convertir en list	
				for	size in sizeSort:
					indicatorSize =	indicatorSpi + '_' + size					
					DBAccess.majDBtable(tableName,indicatorSize,country,str(endYear),nace,nomenclature,'-')
			except:	#si pas de size			
				DBAccess.majDBtable(tableName,indicatorSpi,country,str(endYear),nace,nomenclature,'-')