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
G_tableName = 'externalgeo'
G_worldTableName = 'external'
if G_spiIndicator == 'xdestsh': #1 pour import et 2 pour export dans la notation comext
    G_destor = 'xdest'
    G_world = 'x'  
elif G_spiIndicator == 'morigsh':
    G_destor = 'morig'
    G_world = 'm'
else :
    sys.exit()
  
dirUse = G_path     
dirLog = dirUse + '\\Log'
fileLog = open(dirLog + '\\createDBExternalGeoShare' + G_nomenclature + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(nomenclature, indicatorDestor, indicatorWorld, indicatorSpi, worldTableName, fileLog, tableName):
    infoWorld = DBAccess.lectureNaceIndicatorData(indicatorWorld, nomenclature, worldTableName)
    infoDestor = DBAccess.lectureNomGeoIndicatorData(indicatorDestor, nomenclature, tableName)
    
    refDicWorld    = infoWorld[0]
    startYearWorld = infoWorld[1]
    refDicDestor   = infoDestor[0]
    startYearDestor = infoDestor[1]
    
    if startYearWorld != startYearDestor:
        worldVec = refDicDestor
        while type(worldVec) is not list:
            worldVec = worldVec[list(worldVec.keys())[0]]
        refDicWorld = spiLib.normalizeDicSize(refDicWorld, startYearWorld, startYearDestor, startYearDestor + len(worldVec) - 1)
        
    spiLibCreateTable.createTableExternalGeoShare(nomenclature, refDicWorld, refDicDestor, indicatorSpi, startYearDestor, fileLog, tableName)
    

traitementFichierTXT(G_nomenclature, G_destor, G_world, G_spiIndicator, G_worldTableName, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()