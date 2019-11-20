import sys
import glob
import re
import exceptions
import pprint
from . import DBConnect
from . import DBAccess
from . import FileAccess
from . import spiLib
from . import spiLibCreateTable

#parametre NACE1 ou NACE2
NaceInput      	=  sys.argv[1]
#parametre indicateur Eurostat V11110, V12150, V16110, V92110
G_IndicatorInput 	=  sys.argv[2]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[3]

#G_IndicatorInput.lower()
G_Nomenclature	=  	NaceInput.lower()
G_Size			=	'TOTAL'
G_startYear		=  	1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName		=	'competition'
		
dirUse          =  	Path	
dirLog          =  	dirUse           +'\\Log'
dirTXT          =  	dirUse           +'\\Output'

if		(G_IndicatorInput		==	'V92110'):
		G_compte		=	'sbs'
		if	G_Nomenclature== 	'nace1':			
			fichiersTXT =  	glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+'\\sbs_sc*.tsv')
		else:	
			fichiersTXT =  	glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+'\\sbs_na*.tsv')
else:
		G_compte		=	'bd'
		fichiersTXT     =  	glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+'\\bd_9b*.tsv')

fileLog         =  	open(dirLog+'\\createDBComtradeCompetitionRate'+G_IndicatorInput+G_Nomenclature+'.log','w')

#lecture et traitement fichier INPUT
def traitementFichierTXT(indicatorInput,nomenclature,compteEurostat):
	startIndice			= 0
	dicIndicator        = {}
	dicIndicatorTotal   = {}
	dicNoCountry        = {}	
	dicNaceCheck		= {}
	dicNace       		= {}
	dicNation			= {}
	dicIndicatorDomain	= {}	
	dicIndicatorDomain	= FileAccess.lectureIndicator(dicIndicatorDomain,'competition',dirUse)
	indicatorSpi		= dicIndicatorDomain[indicatorInput]	
	dicNace				= spiLib.defSelectdicNace(nomenclature,compteEurostat)
	dicNation			= DBAccess.lectureNationEurostat(dicNation)
	dicStartValue		= dict(startIndice=1,startCountry='',startNace='',startIndicator='',startValeur=0,startYear=1900)
	minStartYear        = 99999
	maxEndYear          = -1	
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
		iGeoTime	= dicEurostat['geotime']
		geotime		= lstrec[iGeoTime].split('\t')
		endYear		= geotime[1].strip()
		startYear   = geotime[-1].strip()		
		#nace_r1,indic_sb,size_emp,geo\time
		#E,V11110,TOTAL,ES	9037 	6410 	3544 	3311 	3336 	3084
		for ligneTXT in fichierTXT: 
			ligne         = ligneTXT.strip('\n') #RAPPEL strip enleve des extremites
			ligne         = ligne.split(',')
			nace          = ligne[iNace].strip()
			indicator	  =	ligne[iIndic].strip()
			sizeEurostat  =	ligne[iSize].strip()
			
			#la colonne size n'existe pas pour le NACE2 pour les sbs_na *on rempli donc la condition a chaque fois
			if	nomenclature	== 'nace2' and compteEurostat == 'sbs':
				sizeEurostat	=	'TOTAL'
			else:
				sizeEurostat	=	ligne[iSize].strip()

			geoTime		  =	ligne[iGeoTime].split('\t')			
			geoEuroStat	  = geoTime[0].strip()			
			try:
				country	  =	dicNation[geoEuroStat]					
				timeSerie =	geoTime[1:]
				#indicateur pour savoir si on doit selectionner les indicateurs
				#dans la liste definie dans la table oracle ou uniquement sur la longueur (4)
				#la regle est si nace1 alors on prend la liste
				#si bd on prend tout			
				#if	indicator  == indicatorInput and sizeEurostat == G_Size and dicNace.has_key(nace):
				if	indicator  == indicatorInput and sizeEurostat == G_Size:				
					dicNaceCheck[nace]	=	nace #on remplit le dic pour faire un check si autant de nace que dans la table SPI
					vector 			= 	spiLib.defVectorYears(timeSerie, startYear, endYear)
					dicStartValue	=	spiLib.defDicStartValue(timeSerie,country,nace,indicator,dicStartValue,endYear)
					dicIndicator	=	spiLib.defDicIndicator(country,nace,vector,dicIndicator)
					minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear) 	
			except:
				dicNoCountry[geoEuroStat]	=	geoEuroStat	
	
	fileLog.write('highIndice '+str(dicStartValue['startIndice'])+' highCountry '+dicStartValue['startCountry']+\
	' Indicator '+dicStartValue['startIndicator']+' Nace '+dicStartValue['startNace']+\
	' valeur '+str(dicStartValue['startValeur'])+' startYear '+str(dicStartValue['startYear'])+'\n')
	spiLib.defnoCountry(dicNoCountry,fileLog)
	spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)
	minStartYear = dicStartValue['startYear']
	#traitement indicator
	dicIndicator = spiLib.reverseAndNormalizeDicIndicator(dicIndicator, minStartYear, maxEndYear)	
	spiLibCreateTable.createTable(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,G_tableName)	
	spiLibCreateTable.createTableNE(nomenclature,dicNation,endYear,fileLog,indicatorSpi,compteEurostat,G_tableName)
traitementFichierTXT(G_IndicatorInput,G_Nomenclature,G_compte)
fileLog.close()
DBConnect.closeDB()             