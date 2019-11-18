import sys
import glob
import re
import exceptions
import cx_Oracle
import DBConnect
import DBAccess
import spiLib
import spiLibCreateTable

#parametre NACE1 ou NACE2
NaceInput      	=  sys.argv[1]
#parametre indicateur SPI en minuscule
G_IndicatorInput 	=  sys.argv[2]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[3]

G_Nomenclature	=  	NaceInput.lower()
G_startYear		=  	1900 # annee de debut minimum par defaut pour tous les vecteurs
G_compte		=	'nama'
G_tableName		=	'structure'
G_IndicatorInput.lower()

if		(G_IndicatorInput	==	'vakeur'):
		G_IndicatorEurostat	=	'B1G'
		G_FileExt			=	'k'
		G_Growth			=	0
		if G_Nomenclature == 'nace1' :
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = 'MIO_EUR_CLV2005'
		elif G_Nomenclature == 'nace2' :
			G_File = 'nama_10_a??*'
			G_Unit = 'CLV10_MEUR'
		else :
			sys.exit()			
elif	(G_IndicatorInput	==	'vaknat'):
		G_IndicatorEurostat	=	'B1G'
		G_FileExt			=	'k'
		G_Growth			=	0	
		if G_Nomenclature == 'nace1' :
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = 'MIO_NAC_CLV2005'
		elif G_Nomenclature == 'nace2' :
			G_File = 'nama_10_a??*'
			G_Unit = 'CLV10_MNAC'
		else :
			sys.exit()	
elif	(G_IndicatorInput	==	'vakind'):
		G_IndicatorEurostat	=	'B1G'
		G_FileExt				=	'k'
		G_Growth			=	0		
		if G_Nomenclature == 'nace1' :
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = 'I2005'
		elif G_Nomenclature == 'nace2' :
			G_File = 'nama_10_a??*'
			G_Unit = 'CLV_I10'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'vakgr'):
		G_IndicatorEurostat	=	'B1G'
		G_FileExt				=	'k'
		G_Growth			=	1
		if G_Nomenclature == 'nace1' :
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = 'MIO_NAC_CLV2005'
		elif G_Nomenclature == 'nace2' :
			G_File = 'nama_10_a??*'
			G_Unit = 'CLV10_MNAC'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'vakgr5'):
		G_IndicatorEurostat	=	'B1G'
		G_FileExt			=	'k'
		G_Growth			=	5
		if G_Nomenclature == 'nace1' :
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = 'MIO_NAC_CLV2005'
		elif G_Nomenclature == 'nace2' :
			G_File = 'nama_10_a??'
			G_Unit = 'CLV10_MNAC'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'emplgr'):
		G_FileExt				=	'e'
		G_Growth			=	1
		if G_Nomenclature == 'nace1' :
			G_IndicatorEurostat	=	'EMP'
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = '1000PERS'
		elif G_Nomenclature == 'nace2' :
			G_IndicatorEurostat	=	'EMP_DC'
			G_File = 'nama_10_a??_e'
			G_Unit = 'THS_PER'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'emplgr5'):
		G_FileExt				=	'e'
		G_Growth			=	5
		if G_Nomenclature == 'nace1' :
			G_IndicatorEurostat	=	'EMP'
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = '1000PERS'
		elif G_Nomenclature == 'nace2' :
			G_IndicatorEurostat	=	'EMP_DC'
			G_File = 'nama_10_a??_e'
			G_Unit = 'THS_PER'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'hours'):
		G_FileExt				=	'e'
		G_Growth			=	0	
		if G_Nomenclature == 'nace1' :
			G_IndicatorEurostat	=	'EMP'
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = '1000HRS'
		elif G_Nomenclature == 'nace2' :
			G_IndicatorEurostat	=	'EMP_DC'
			G_File = 'nama_10_a??_e'
			G_Unit = 'THS_HW'
		else :
			sys.exit()	
elif	(G_IndicatorInput	==	'hoursgr'):
		G_FileExt				=	'e'
		G_Growth			=	1
		if G_Nomenclature == 'nace1' :
			G_IndicatorEurostat	=	'EMP'
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = '1000HRS'
		elif G_Nomenclature == 'nace2' :
			G_IndicatorEurostat	=	'EMP_DC'
			G_File = 'nama_10_a??_e'
			G_Unit = 'THS_HW'
		else :
			sys.exit()
elif	(G_IndicatorInput	==	'hoursgr5'):
		G_FileExt				=	'e'
		G_Growth			=	5	
		if G_Nomenclature == 'nace1' :
			G_IndicatorEurostat	=	'EMP'
			G_File = 'nama_nace??_'+G_FileExt
			G_Unit = '1000HRS'
		elif G_Nomenclature == 'nace2' :
			G_IndicatorEurostat	=	'EMP_DC'
			G_File = 'nama_10_a??_e'
			G_Unit = 'THS_HW'
		else :
			sys.exit()	
		
dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
fichiersTXT     =  glob.glob(dirUse +'\\Input\\tsv\\'+G_Nomenclature+'\\'+G_File+'.tsv')
fileLog         =  open(dirLog      +'\\createDBComtradeGrowth'+G_IndicatorInput+G_Nomenclature+'.log', 'w')

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
		#recherche de la position de chaque variable dans input eurostat
		#on selectionne les colonne de l'input d'Eurostat		
		dicEurostat	= spiLib.defDicEurostat(lstrec)
		iUnit		= dicEurostat['unit']
		iNace		= dicEurostat['nace']
		iIndic		= dicEurostat['indic']
		iSector		= dicEurostat['sector']
		iSize		= dicEurostat['size']
		iGeoTime	= dicEurostat['geotime']
		geotime		= lstrec[iGeoTime].split('\t')
		endYear		= geotime[1].strip()
		startYear   = geotime[-1].strip()		
		#nace 1 : unit,sector,nace_r1,indic_na,geo\time
		#nace 2 : unit,nace_r2,indic_na,sector,geo\time		
		#MIO_EUR,A,B1G,AT	: 	: 	: 	3781.7 	4375.5 	4322.6 	3827.4 	3542.7 	3921.8 	3763.1 
		for ligneTXT in fichierTXT: 
			ligne         = ligneTXT.strip('\n') #RAPPEL strip enleve des extremites			
			ligne         = ligne.split(',')
			nace          = ligne[iNace].strip()
			indicator	  =	ligne[iIndic].strip()
			unit	  	  =	ligne[iUnit].strip()
			geoTime		  =	ligne[iGeoTime].split('\t')
			geoEuroStat	  = geoTime[0].strip()
			if iSector == -1 :
				sector = 'S1'
			else :
				sector = ligne[iSector].strip()  
			try:
				country	  =	dicNation[geoEuroStat]
				timeSerie =	geoTime[1:]
				#indicateur pour savoir si on doit selectionner les indicateurs
				#dans la liste definie dans la table oracle ou uniquement sur la longueur (4)
				#la regle est si nace1 alors on prend la liste
				#si nace2 et nama on prend la liste sur sbs on teste sur la longueur max 4
				if	indicator == indicatorEurostat and (unit == Unit) and (sector == 'S1') and dicNace.has_key(nace):
					dicNaceCheck[nace]	=	nace #on remplit le dic pour faire un check si autant de nace que dans la table SPI											
					vector 				= 	spiLib.defVectorYears(timeSerie, startYear, endYear)#traitement de la serie Eurostat					
					dicStartValue		=	spiLib.defDicStartValue(timeSerie,country,nace,indicator,dicStartValue,endYear)	
					dicIndicator	 	=	spiLib.defDicIndicator(country,nace,vector,dicIndicator)
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
	spiLibCreateTable.createTableGrowth(nomenclature,dicIndicator,fileLog,minStartYear,dicNace,indicatorSpi,compteEurostat,G_tableName,G_Growth,G_FileExt)
	spiLibCreateTable.createTableNE(nomenclature,dicNation,endYear,fileLog,indicatorSpi,compteEurostat,G_tableName)
                                                             
traitementFichierTXT(G_IndicatorInput,G_IndicatorEurostat,G_Nomenclature,G_compte)
fileLog.close()
DBConnect.closeDB()	         