import sys
import glob
import re

from . import DBConnect
from . import DBAccess
from . import spiLib
from . import spiLibTotal
from . import spiLibCreateTable

#parametre NACE1 ou NACE2
NaceInput      	=  sys.argv[1]
#parametre indicateur SPI firmssize,vasize,emplsize
G_IndicatorInput 	=  sys.argv[2]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[3]

G_IndicatorInput.lower()
G_Nomenclature	=  	NaceInput.lower()
G_startYear		=  	1900 # annee de debut minimum par defaut pour tous les vecteurs
G_compte		=	'sbs'
G_tableName		=	'structure'

if		(G_IndicatorInput	==	'firmssize'):
		G_IndicatorEurostat	=	'V11110'
		G_File				=	'\\sbs_sc*.tsv'	
elif	(G_IndicatorInput	==	'vasize'):
		G_IndicatorEurostat	=	'V12150'
		G_File				=	'\\sbs_sc*.tsv'			
elif	(G_IndicatorInput	==	'emplsize'):
		G_IndicatorEurostat	=	'V16110'
		G_File				=	'\\sbs_sc*.tsv'	

if	G_Nomenclature==  'nace1':
	G_LstSize			=	['1', '2-9', '1-9', '10-19','20-49','50-249','GE250','TOTAL'];#pour la selection dans Eurostat
	G_DicSize			=	{'1':'0or1To9', '2-9':'0or1To9', '1-9':'0or1To9', '10-19':'10To19','20-49':'20To49','50-249':'50To249','GE250':'GE250','TOTAL':'TOTAL'};
else:
	G_LstSize			=	['0_1', '2-9', '0-9','10-19','20-49','50-249','GE250','TOTAL'];#pour la selection dans Eurostat
	G_DicSize			=	{'0_1':'0or1To9', '2-9':'0or1To9', '0-9':'0or1To9','10-19':'10To19','20-49':'20To49','50-249':'50To249','GE250':'GE250','TOTAL':'TOTAL'};		

dirUse          =  Path 	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
fichiersTXT     =  glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+G_File)
fileLog         =  open(dirLog      +'\\createDBComtradeStructureSize'+G_IndicatorInput+G_Nomenclature+'.log', 'w')

#lecture et traitement fichier INPUT
def traitementFichierTXT(indicatorInput,indicatorInputEurostat,nomenclature,compteEurostat):
	startIndice			= 0
	dicIndicator        = {}
	dicIndicatorTotal   = {}
	dicNoCountry        = {}	
	dicNaceCheck		= {}
	dicNace       		= {}
	dicNation			= {}
	dicSize				= {}
	indicatorSpi		= indicatorInput
	indicatorEurostat	= indicatorInputEurostat
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
			size		  =	ligne[iSize].strip()
			geoTime		  =	ligne[iGeoTime].split('\t')			
			geoEuroStat	  = geoTime[0].strip()
			try:
				country	  =	dicNation[geoEuroStat]					
				timeSerie =	geoTime[1:]
				#print indicator,indicatorEurostat,indicatorInput,size,nomenclature,nace
				if	(indicator == indicatorEurostat and (G_LstSize.count(size))) and ((nomenclature == 'nace1' and nace in dicNace) or (nomenclature == 'nace2' and len(nace) < 4)):
					dicSize[size] =	size	#pour connaitre les size de eurostat
					try: #on cherche l'indicateur SPI correspondant
						indicator_size	=	indicatorSpi +'_'+ G_DicSize[size]
					except:				
						fileLog.write('pas de size '+size+' indicateur : '+indicator+' country : '+country+'\n')			
						continue #on passe on record suivant
					dicNaceCheck[nace]	=	nace #on remplit le dic pour faire un check si autant de nace que dans la table SPI
					vector 			= 	spiLib.defVectorYears(timeSerie, startYear, endYear)
					dicStartValue	=	spiLib.defDicStartValue(timeSerie,country,nace,indicator,dicStartValue,endYear)
					dicIndicator	=	spiLib.defDicIndicatorSize(country,nace,vector,indicator_size,dicIndicator)
					minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear) 					
			except:
				dicNoCountry[geoEuroStat]	=	geoEuroStat
	fileLog.write('highIndice '+str(dicStartValue['startIndice'])+' highCountry '+dicStartValue['startCountry']+\
	' Indicator '+dicStartValue['startIndicator']+' Nace '+dicStartValue['startNace']+\
	' valeur '+str(dicStartValue['startValeur'])+' startYear '+str(dicStartValue['startYear'])+'\n')
	spiLib.defnoCountry(dicNoCountry,fileLog)
	spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)
	keySize		=	list(dicSize.keys())
	keySize.sort()			
	for s	in keySize:
			fileLog.write(' List Size in Eurostat Input : '+ s +'\n')
	minStartYear = dicStartValue['startYear']
	dicIndicator = spiLib.reverseAndNormalizeDicIndicatorSize(dicIndicator, minStartYear, maxEndYear)			
	spiLibCreateTable.createTableSize(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,G_tableName)
	spiLibCreateTable.createTableNE(nomenclature,dicNation,endYear,fileLog,indicatorSpi,compteEurostat,G_tableName,G_DicSize)
traitementFichierTXT(G_IndicatorInput,G_IndicatorEurostat,G_Nomenclature,G_compte)
fileLog.close()
DBConnect.closeDB()             