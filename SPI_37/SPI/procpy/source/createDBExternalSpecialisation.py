import sys
import glob
import re
import exceptions
import DBConnect
import DBAccess
import spiLib
import spiLibTotal
import spiLibCreateTable
import pprint
import spiLibComext

G_spiIndicator = sys.argv[1]
#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[2].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[3]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'external'

if G_spiIndicator == 'xspeu27':
    G_reference = 'EU27'
    G_baseIndicator = 'xsh'
elif G_spiIndicator == 'xspeu28':
    G_reference = 'EU28'
    G_baseIndicator = 'xsh'
elif G_spiIndicator == 'xspea19':
    G_reference = 'EA19'
    G_baseIndicator = 'xsh'
elif G_spiIndicator == 'mspeu27':
    G_reference = 'EU27'
    G_baseIndicator = 'msh'
elif G_spiIndicator == 'mspeu28':
    G_reference = 'EU28'
    G_baseIndicator = 'msh'
elif G_spiIndicator == 'mspea19':
    G_reference = 'EA19'
    G_baseIndicator = 'msh'
else :
    sys.exit()
    
dirUse = G_path     
dirLog = dirUse + '\\Log'
fileLog = open(dirLog + '\\createDBExternalSpecialisation' + G_nomenclature + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicator, nomenclature, reference, baseIndicator, fileLog, tableName):
    info = DBAccess.lectureNaceIndicatorData(baseIndicator, nomenclature, tableName)
    
    refDic = info[0]
    startYear = info[1]
    
    spiLibCreateTable.createTableExternalSpecialisation(indicator, nomenclature, refDic, startYear, reference, fileLog, tableName)

traitementFichierTXT(G_spiIndicator, G_nomenclature, G_reference, G_baseIndicator, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()