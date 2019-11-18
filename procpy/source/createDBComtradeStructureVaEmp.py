import sys
import glob
import re
import exceptions
import cx_Oracle
import DBConnect
import DBAccess
import spiLib
import spiLibCreateTable
from pprint import pprint

#parametre NACE1 ou NACE2
NaceInput      	=  sys.argv[1]
#parametre indicateur SPI B1G,empl
G_IndicatorInput 	=  sys.argv[2]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[3]

G_Nomenclature	=  	NaceInput.lower()
G_startYear		=  	1900 # annee de debut minimum par defaut pour tous les vecteurs
G_compte		=	'nama'
G_tableName		=	'structure'
G_IndicatorInput.lower()

if		(G_IndicatorInput	==	'va'):
		G_IndicatorEurostat	=	'B1G'
		G_FileExt			=	'c'
		if G_Nomenclature == 'nace1' :
			G_Unit				=	'MIO_EUR'
			G_File				=	'\\nama_nace??_c.tsv'
		elif G_Nomenclature == 'nace2' :
			G_Unit				=	'CP_MEUR'
			G_File				=	'\\nama_10_a??.tsv'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'emp'):
		G_FileExt			=	'e'
		if G_Nomenclature == 'nace1' :
			G_Unit				=  	'THS_PER'
			G_IndicatorEurostat	=	'EMP'
			G_File				=	'\\nama_nace??_e.tsv'
		elif G_Nomenclature == 'nace2' :
			G_Unit				=  	'THS_PER'
			G_IndicatorEurostat	=	'EMP_DC'
			G_File				=	'\\nama_10_a??_e.tsv'
		else :
			sys.exit()
dirUse          =	Path 	
dirLog          =  	dirUse           +'\\Log'
dirTXT          =  	dirUse           +'\\Output'
fichiersTXT     =  	glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+G_File)
fileLog         =  	open(dirLog+'\\createDBComtradeStructureVaEmp'+G_IndicatorInput+G_Nomenclature+'.log','w')
   
#lecture et traitement fichier INPUT
def traitementFichierTXT(indicatorInput,indicatorInputEurostat,nomenclature,compteEurostat):
	startIndice			= 0
	dicIndicator        = {}
	dicNoCountry        = {}	
	dicNaceCheck		= {}
	dicNace       		= {}
	dicNation			= {}
	indicatorSpi		= indicatorInput
	indicatorEurostat	= indicatorInputEurostat	
	Unit				= G_Unit
	dicNace				= spiLib.defSelectdicNace(nomenclature,compteEurostat)
	dicNation			= DBAccess.lectureNationEurostat(dicNation)
	dicStartValue		= dict(startIndice=1,startCountry='',startNace='',startIndicator='',startValeur=0,startYear=1900)
	minStartYear        = 99999
	maxEndYear          = -1
	fichiersTXT.sort()	
	fichiersTXT.reverse()	
	for txt in fichiersTXT:	
		fichierTXT 	= open(txt,'r')
		rec1er     	= fichierTXT.readline() #1er rec avec les meta
		lstrec		= rec1er.split(',')
		#on selectionne les colonne de l'input d'Eurostat		
		dicEurostat	= spiLib.defDicEurostat(lstrec)
		iUnit		= dicEurostat['unit']
		iNace		= dicEurostat['nace']
		iIndic		= dicEurostat['indic']
		iSize		= dicEurostat['size']
		iSector		= dicEurostat['sector']
		iGeoTime	= dicEurostat['geotime']
		geotime		= lstrec[iGeoTime].split('\t')
		endYear		= geotime[1].strip()
		startYear   = geotime[-1].strip()
		for ligneTXT in fichierTXT: 
			ligne		= ligneTXT.strip('\n') #RAPPEL strip enleve des extremites
			ligne		= ligne.split(',')
			nace		= ligne[iNace].strip()
			indicator	= ligne[iIndic].strip()
			unit		= ligne[iUnit].strip()
			geoTime		= ligne[iGeoTime].split('\t')			
			geoEuroStat	= geoTime[0].strip()
			# la colonne sector existait pour le nama_nace64_e.tsv
			# il a disparu dans le esa2010 mais on garde le test 
			if iSector == -1 :
				sector = 'S1'
			else : 
				sector = ligne[iSector].strip()
			try:
				country	  =	dicNation[geoEuroStat]					
				timeSerie =	geoTime[1:]
				if	indicator == indicatorEurostat and (unit == Unit) and (sector == 'S1') and dicNace.has_key(nace):
					dicNaceCheck[nace]	=	nace #on remplit le dic pour faire un check si autant de nace que dans la table SPI											
					vector 				= 	spiLib.defVectorYears(timeSerie, startYear, endYear)#traitement de la serie Eurostat					
					dicStartValue		=	spiLib.defDicStartValue(timeSerie,country,nace,indicator,dicStartValue,endYear)
					dicIndicator	 =	spiLib.defDicIndicator(country,nace,vector,dicIndicator)
					minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear) 			
			except:
				dicNoCountry[geoEuroStat]	=	geoEuroStat	
	#retour avec l'annee de la  1er valeur existante dans les vecteurs
	#different de la 1er annee ou vecteur le plus long car la valeur peut etre ':'
	fileLog.write('highIndice '+str(dicStartValue['startIndice'])+' highCountry '+dicStartValue['startCountry']+\
	' Indicator '+dicStartValue['startIndicator']+' Nace '+dicStartValue['startNace']+\
	' valeur '+str(dicStartValue['startValeur'])+' startYear '+str(dicStartValue['startYear'])+'\n')
	spiLib.defnoCountry(dicNoCountry,fileLog)
	spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)
	#test des annee de debut, soit par valeur reelle ou par vecteur la valeur peut etre ':'
	if	minStartYear != dicStartValue['startYear']:
			fileLog.write('annee min. pour les vecteurs ='+str(minStartYear)+' annee min. avec une valeur ='+str(dicStartValue['startYear'])+'\n')
			minStartYear	=	dicStartValue['startYear']
	#traitement indicator
	dicIndicator = spiLib.reverseAndNormalizeDicIndicator(dicIndicator, minStartYear, maxEndYear)
	spiLibCreateTable.createTable(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,G_tableName,G_FileExt)
	spiLibCreateTable.createTableNE(nomenclature,dicNation,endYear,fileLog,indicatorSpi,compteEurostat,G_tableName)

traitementFichierTXT(G_IndicatorInput,G_IndicatorEurostat,G_Nomenclature,G_compte)
fileLog.close()
DBConnect.closeDB()	
               