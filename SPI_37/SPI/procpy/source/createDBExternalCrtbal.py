import sys
import glob
import re
import exceptions
import DBConnect
import DBAccess
import spiLib
import spiLibTotal
import spiLibCreateTable
import spiLibComext
from pprint import pprint

#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[1].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[2]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'external'

dirUse = G_path     
dirLog = dirUse + '\\Log'
fileLog = open(dirLog + '\\createDBExternalCrtbal' + G_nomenclature + '.log', 'w')

def traitementFichierTXT(nomenclature, fileLog, tableName):
    infoX = DBAccess.lectureNaceIndicatorData('x', nomenclature, tableName)
    infoM = DBAccess.lectureNaceIndicatorData('m', nomenclature, tableName)
    
    refDicX = infoX[0]
    startYearX = infoX[1]
    
    refDicM = infoM[0]
    startYearM = infoM[1]
    
    if startYearX != startYearM:
        fileLog.write('Start year for indicators x and m are different.\n')
        return
                
    refDicX = spiLibTotal.calcNaceAggregates(refDicX, nomenclature, 'manufacturing')
    refDicM = spiLibTotal.calcNaceAggregates(refDicM, nomenclature, 'manufacturing')
       
    spiLibCreateTable.createTableExternalCrtbal(nomenclature, refDicX, refDicM, startYearM, fileLog, tableName)

traitementFichierTXT(G_nomenclature, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()