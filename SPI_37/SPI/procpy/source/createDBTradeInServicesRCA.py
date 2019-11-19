import sys
import FileAccess
import spiLibTrade
import spiLibDBaccess
import DBConnect

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 	=  sys.argv[1]

G_tableName		=	'trade'
G_compte		=	'sector'
G_typeProduit	=	'sector'
		
dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
fichierTXT     	=  dirUse      		+'\\Output\\wto\\tradeinservice.txt'
fileLog         =  open(dirLog      +'\\createDBTradeInServiceRCA.log', 'w')

def traitementFichierTXT(fichierTXT,G_typeProduit,G_compte):
	startIndice			= 0
	dicFile        		= {}
	dicFileWld        	= {}
	dicTotalCountry    	= {}
	dicTotalWld			= {}
	startYear			= 0
	endYear				= 0
	lenVector			= 0
	typeProduit			= G_typeProduit
	compte				= G_compte
	dicFile,dicFileWld,startYear,endYear = FileAccess.lectureTradeServiceRCA(fichierTXT)
	lenVector			= int(endYear) - int(startYear) + 1
	dicTotalCountry		= spiLibTrade.defDicTotalSector(dicFile,lenVector)
	dicTotalWld			= spiLibTrade.defDicTotalSector(dicFileWld,lenVector)
	spiLibDBaccess.createTableTotal('rca',fileLog,dicFile,dicTotalCountry,dicFileWld,dicTotalWld,startYear,G_tableName,typeProduit)	
traitementFichierTXT(fichierTXT,G_typeProduit,G_compte)
fileLog.close() 
DBConnect.closeDB()       