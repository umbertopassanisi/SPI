import sys
import pprint
import FileAccess
import spiLibTrade
import spiLibDBaccess
import DBConnect
import DBAccess

#parametre 
#G_IndicatorInput=  sys.argv[1]
#parametre cpa2002, cpa2008, BEC
G_typeProduit 	=  sys.argv[1]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[2]

G_tableName		=	'external'
G_compte		=	'comtrade'
#G_IndicatorInput.lower()
G_typeProduit.lower()
		
dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
fichierTXT     	=  dirUse      		+'\\Output\\comtrade\\tradeingoodsRCA'+G_typeProduit+'.txt'
fileLog         =  open(dirLog      +'\\createDBTradeInGoodsRCA.log', 'w')

def traitementFichierTXT(fichierTXT,G_typeProduit,G_compte):
	startIndice			= 0
	dicFile        		= {}
	dicFileWld        	= {}
	dicTotalCountry    	= {}
	dicCountryAgregat  	= {}
	dicCountry			= {}
	dicCountryWld		= {}	
	dicTotalWld			= {}
	startYear			= 0
	endYear				= 0
	lenVector			= 0
	typeProduit			= G_typeProduit #cpa2002, cpa2008, BEC
	compte				= G_compte
	dicFile,dicFileWld,startYear,endYear	= FileAccess.lectureTradeGoodsRCA(fichierTXT)
	lenVector			= int(endYear) - int(startYear) + 1
	if	typeProduit		== 'bec':
		dicTotalCountry	= spiLibTrade.defDicTotalBec(dicFile,lenVector)
		dicTotalWld		= spiLibTrade.defDicTotalBec(dicFileWld,lenVector)
	else:
		dicCpa			= {}
		dicCpaN3		= {}
		dicCpa,dicCpaN3 = DBAccess.lectureCpa(typeProduit) #dicCpa et dic par code cpaN3
		dicTotalCountry,dicCountryAgregat 	= spiLibTrade.defDicTotal(dicFile,dicCpaN3,lenVector)
		dicFileN1,dicFileN2	= spiLibTrade.defDicCalculAgregat(dicCountryAgregat,lenVector)
		#total World
		dicCountryAgregat={}
		dicTotalWld,dicCountryAgregat		= spiLibTrade.defDicTotal(dicFileWld,dicCpaN3,lenVector) 
		dicFileWldN1,dicFileWldN2	= spiLibTrade.defDicCalculAgregat(dicCountryAgregat,lenVector)
		
	spiLibDBaccess.createTableTotal('rca',fileLog,dicFile,dicTotalCountry,dicFileWld,dicTotalWld,startYear,G_tableName,G_typeProduit)
	if	typeProduit		!= 'bec':
		spiLibDBaccess.createTableTotal('rca',fileLog,dicFileN1,dicTotalCountry,dicFileWldN1,dicTotalWld,startYear,G_tableName,G_typeProduit)
		spiLibDBaccess.createTableTotal('rca',fileLog,dicFileN2,dicTotalCountry,dicFileWldN2,dicTotalWld,startYear,G_tableName,G_typeProduit)		

traitementFichierTXT(fichierTXT,G_typeProduit,G_compte)
fileLog.close() 
DBConnect.closeDB()       