import sys
import glob
import re
import exceptions
import DBConnect
import DBAccess
import spiLib
import spiLibTotal
import spiLibCreateTableCheck
import spiLibCreateTable


#parametre NACE1 ou NACE2
NaceInput      	=  sys.argv[1]
#parametre indicateur Eurostat vabus,emplbus,firms
G_IndicatorInput 	=  sys.argv[2]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[3]
G_country 	=  sys.argv[4]

G_IndicatorInput.lower()
G_Nomenclature	=  	NaceInput.lower()
G_startYear		=  	1900 # annee de debut minimum par defaut pour tous les vecteurs
G_compte		=	'sbs'
G_tableName		=	'structure'

if		(G_IndicatorInput	==	'firms'):
		G_IndicatorSPI_T	=  	'noTotal'
		G_IndicatorEurostat	=	'V11110'		
		G_File				=	'\\sbs_na*.tsv'
elif	(G_IndicatorInput	==	'vabus'):
		G_IndicatorSPI_T	=  	'vabussh'
		G_IndicatorEurostat	=	'V12150'
		G_File				=	'\\sbs_na*.tsv'
elif	(G_IndicatorInput	==	'emplbus'):
		G_IndicatorSPI_T	=  	'emplbussh'
		G_IndicatorEurostat	=	'V16110'
		G_File				=	'\\sbs_sc*.tsv'	
		
dirUse          =  Path 	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
fichiersTXT     =  glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+G_File)
fileLog         =  open(dirLog      +'\\createDBComtradeStructure'+G_IndicatorInput+G_Nomenclature+'.log', 'w')

#lecture et traitement fichier INPUT
def traitementFichierTXT(indicatorInput,indicatorInputEurostat,nomenclature,compteEurostat):
	startIndice			= 0
	dicIndicator        = {}
	dicIndicatorTotal   = {}
	dicNoCountry        = {}	
	dicNaceCheck		= {}
	dicNace       		= {}
	dicAgregatNace 		= {}
	dicNation			= {}
	indicatorSpi		= indicatorInput	
	indicatorSpiTotal	= G_IndicatorSPI_T
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
			if	iSize	  ==	-1:
				size	  = 'TOTAL'
			else:
				size	  =	ligne[iSize].strip()
			try:
				#country	  =	dicNation[geoEuroStat]					
				country	  =	dicNation[G_country]				
				timeSerie =	geoTime[1:]
				if	(indicator == indicatorEurostat ) and (size == 'TOTAL') and (geoEuroStat == G_country) and\
					((nomenclature == 'nace1' and dicNace.has_key(nace)) or \
					(nomenclature == 'nace2' and len(nace) < 4)):
					dicNaceCheck[nace]	=	nace #on remplit le dic pour faire un check si autant de nace que dans la table SPI											
					vector 			= 	spiLib.defVectorYears(timeSerie, startYear, endYear)#traitement de la serie Eurostat
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
	dicIndicator = spiLib.reverseAndNormalizeDicIndicator(dicIndicator, minStartYear, maxEndYear)
	countrySort  =   dicIndicator.keys()
	'''
	for country in countrySort:
		naceSort    			=   dicIndicator[country].keys()
		naceSort.sort()
		for nace in naceSort:
			vector      	=   dicIndicator[country][nace]
			print country, minStartYear, maxEndYear, nace, vector
	'''
	#print '----------------------AGREAGATE------------------------------'
	#creation indicateur SPI par ex vabus avec en retour le dic des agregats
	dicAgregatNace = spiLibCreateTableCheck.createTable(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,G_tableName)
	countrySort  =   dicAgregatNace.keys()
	'''
	for country in countrySort:
		naceSort    			=   dicAgregatNace[country].keys()
		naceSort.sort()
		for nace in naceSort:
			vector      	=   dicAgregatNace[country][nace]
			#print country, minStartYear, maxEndYear, nace, vector
	'''
	if	indicatorSpiTotal != 'noTotal':	
		#creation indicateur total SPI par ex vabussh
		spiLibCreateTable.createTableTotal(nomenclature,dicAgregatNace,dicIndicator,minStartYear,fileLog,dicNace,indicatorSpiTotal,compteEurostat,G_tableName)
		spiLibCreateTable.createTableNE(nomenclature,dicNation,endYear,fileLog,indicatorSpiTotal,compteEurostat,G_tableName)
	spiLibCreateTable.createTableNE(nomenclature,dicNation,endYear,fileLog,indicatorSpi,compteEurostat,G_tableName)

traitementFichierTXT(G_IndicatorInput,G_IndicatorEurostat,G_Nomenclature,G_compte)
fileLog.close()
DBConnect.closeDB()             