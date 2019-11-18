import sys
import glob
import re
import exceptions
import DBConnect
import DBAccess
import spiLib
import spiLibTotal
import spiLibCreateTable
from pprint import pprint

#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[1].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[2]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'competition'

if G_nomenclature == 'nace1':
    G_cpa = 'cpa2002'
elif G_nomenclature == 'nace2':
    G_cpa = 'cpa2008'
else:
    sys.exit()
    
dirUse = G_path     
dirLog = dirUse + '\\Log'
fileLog = open(dirLog + '\\createDBCompetitionOpen' + G_nomenclature + '.log', 'w')

def traitementFichierTXT(nomenclature, cpa, fileLog, tableName):
    infoVa = DBAccess.lectureNaceIndicatorData('va', nomenclature, 'structure')
    infoX  = DBAccess.lectureCpaNaceIndicatorData('x', cpa, 'external')
    infoM  = DBAccess.lectureCpaNaceIndicatorData('m', cpa, 'external')
    
    refDicVa    = infoVa[0]
    startYearVa = infoVa[1]
    refDicX     = infoX[0]
    startYearX  = infoX[1]
    refDicM     = infoM[0]
    startYearM  = infoM[1]
    
    refVec = refDicX
    vectorCheck = 1
    while type(refVec) is not list:
        refVec = refVec[refVec.keys()[vectorCheck]]
        if type(refVec) is list:
            while len(refVec) == 1:
                vectorCheck += 1
                refVec = refVec[refVec.keys()[vectorCheck]]

    refDicVa = spiLib.normalizeDicSize(refDicVa, startYearVa, startYearX, startYearX + len(refVec) - 1)
    refDicM = spiLib.normalizeDicSize(refDicM, startYearM, startYearX, startYearX + len(refVec) - 1)
    
    spiLibCreateTable.createTableCompetitionOpen(nomenclature, refDicVa, refDicX, refDicM, startYearX, fileLog, tableName)
    
traitementFichierTXT(G_nomenclature, G_cpa, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()