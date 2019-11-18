#generation des indicateurs trade in services geographical
#input Eurostat 
#exports:
#xdest, xdestsh
#imports:
#morig,morigsh
import sys
import glob

from pprint import pprint

import DBAccess
import spiLib
import spiLibTrade
import DBConnect

#parametre flow : m=import, x=export
G_flow      	=  sys.argv[1]
#nomenclature : bpm5 or bpm6
G_nomenclature	= sys.argv[2]
#parametre flow : 0=no destination/origine, 1=destination/origine pour xdest,xdestsh, morig,morigsh
G_destOrg  		=  sys.argv[3]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 			=  sys.argv[4]

G_flow.lower()

if	G_destOrg 	==	'1':
	G_tableName	=	'tradegeo' #tradegeo pour les destination/origine
else:
	G_tableName	=	'trade'

	
dirUse          =	Path	
dirLog          =	dirUse           +'\\Log'
dirTXT          =	dirUse           +'\\Output'
fileLog         =	open(dirLog      +'\\createDBTradeInServices.log', 'w')

if G_nomenclature == 'bpm5' :
	fichiersTXT     =	glob.glob(dirUse +'\\Input\\tsv\\service\\bop_its_det.tsv')
elif G_nomenclature == 'bpm6' :
	fichiersTXT     =	glob.glob(dirUse +'\\Input\\tsv\\service\\bop_its6_det.tsv')
else :
	sys.exit()

def traitementFichierTXT(flow,tableName,nomenclature,destOrg):
	if	flow == 'x':	flowInput = 'CRE'
	if	flow == 'm':	flowInput = 'DEB'
	startIndice			= 0
	dicIndicator        = {}
	dicNoCountry        = {}	
	dicSector       	= {}
	dicCountry			= {}
	dicCountryPartner	= {}
	dicCountry			= DBAccess.lectureNationEurostat()#cle codeEurostat, contenu code iso2
	if	destOrg == '1':
		dicCountryPartner= DBAccess.lectureNationPartner()#cle codeEurostat, contenu code iso2
		if nomenclature == 'bpm6' :
			dicCountryPartner['WRL_REST'] = 'WRL_REST'
	else:
		if nomenclature == 'bpm5' :
			dicCountryPartner = dict(WORLD='WORLD')
		else :
			dicCountryPartner = dict(WRL_REST='WRL_REST')
	
	codes = DBAccess.getNomenclature(nomenclature)		
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
		dicEurostat	= spiLibTrade.defDicEurostat(lstrec)
		iSector		= dicEurostat['sector']
		iFlow		= dicEurostat['flow'] #m=import, x=export
		iPartner	= dicEurostat['partner']
		iGeoTime	= dicEurostat['geotime']
		geotime		= lstrec[iGeoTime].split('\t')
		endYear		= geotime[1].strip()
		startYear   = geotime[-1].strip()			
		for ligneTXT in fichierTXT: 
			ligne         = ligneTXT.strip('\n') #RAPPEL strip enleve des extremites			
			ligne         = ligne.split(',')
			sector        = ligne[iSector].strip()
			flow	  	  =	ligne[iFlow].strip()
			partner	  	  =	ligne[iPartner].strip()
			geoTime		  =	ligne[iGeoTime].split('\t')		
			geoEuroStat	  = geoTime[0].strip()
			#on prend soit les importations (debit=DEB)
			#ou les exportations (credit=CRE)
			if	flowInput == flow:
				try:#controle des country reporter pas de partner a ce niveau
					country			=	dicCountry[geoEuroStat]				
					timeSerie 		=	geoTime[1:]
					if	(sector in codes) and (partner in dicCountryPartner):
						if nomenclature == 'bpm6' and partner == 'WRL_REST' :
							partner = 'WORLD'
						vector 				= 	spiLib.defVectorYears(timeSerie, startYear, endYear)#traitement de la serie Eurostat
						dicIndicator	 	=	spiLibTrade.dicIndicator(country,partner,sector,vector,dicIndicator)
						minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear)
				except:
					dicNoCountry[geoEuroStat]	= geoEuroStat
	
	
	spiLib.defnoCountry(dicNoCountry,fileLog)
	dicIndicator = spiLib.reverseAndNormalizeDicIndicatorSize(dicIndicator, minStartYear, maxEndYear)
	if	destOrg == '1':
		spiLibTrade.createIndicatorServiceDestOrg(dicIndicator,flowInput,nomenclature,minStartYear,maxEndYear,tableName,fileLog,dicCountryPartner)
	else:
		spiLibTrade.createIndicatorService(dicIndicator,flowInput,G_flow,nomenclature,minStartYear,maxEndYear,tableName,fileLog)	
                                                             
traitementFichierTXT(G_flow,G_tableName,G_nomenclature,G_destOrg)
fileLog.close()
DBConnect.closeDB()	         