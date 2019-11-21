import sys
import glob
import re

import DBConnect
import DBAccess
import spiLib
import spiLibTotal
import spiLibCreateTable

#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[1].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[2]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'competition'
G_file = '\\nama_nace*_c.tsv'  
G_indicatorEurostat = 'P1'
G_unit = 'MIO_EUR'

if G_nomenclature == 'nace1':
    G_cpa = 'cpa2002'
elif G_nomenclature == 'nace2':
    G_cpa = 'cpa2008'
else:
    sys.exit()
    
dirUse = G_path     
dirLog = dirUse + '\\Log'
fichiersTXT = glob.glob(dirUse + '\\Input\\tsv\\' + G_nomenclature + G_file)
fileLog = open(dirLog + '\\createDBCompetitionImportpen' + G_nomenclature + '.log', 'w')

def traitementFichierTXT(indicatorEurostat, unitEurostat, nomenclature, cpa, files, fileLog, tableName):
    infoX                       = DBAccess.lectureCpaNaceIndicatorData('x', cpa, 'external')
    infoM                       = DBAccess.lectureCpaNaceIndicatorData('m', cpa, 'external')
    refDicX                     = infoX[0]
    startYearX                  = infoX[1]
    refDicM                     = infoM[0]
    startYearM                  = infoM[1]
    refDicGO                    = {}
    dicNoCountry                = {} 
    dicNation                   = {}
    dicNaceCheck                = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    dicNace                     = spiLib.defSelectdicNace(nomenclature, 'nama')
    minimumYearWithActualData   = 999999
    maxEndYear                  = -1
    
    files.sort()
    files.reverse() 
    
    for txt in files :
        file           = open(txt, 'r')
        line1st        = file.readline()
        list1st        = line1st.split(',')
        dicEurostat    = spiLib.defDicEurostat(list1st)
        iUnit          = dicEurostat['unit']
        iIndic         = dicEurostat['indic']
        iNace          = dicEurostat['nace']
        iGeoTime       = dicEurostat['geotime']
        geotime        = list1st[iGeoTime].split('\t')
        
        endYear        = geotime[1].strip()
        startYear      = geotime[-1].strip()
        
        for line in file :
            lineList      = line.strip('\n').split(',')
            nace          = lineList[iNace].strip()
            indicator     = lineList[iIndic].strip()
            unit          = lineList[iUnit].strip()
            geoTime       = lineList[iGeoTime].split('\t')            
            geo           = geoTime[0].strip()
            
            try :
                dicNaceCheck[nace] = nace
                country = dicNation[geo]                    
                timeSerie = geoTime[1:]

                if indicator == indicatorEurostat and nace in dicNace and unit == unitEurostat:
                    vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                    minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                    refDicGO = spiLib.defDicIndicator(country,nace,vector,refDicGO)
                    if int(endYear) > maxEndYear :
                        maxEndYear = int(endYear)
            except :
                dicNoCountry[geo] = geo
    
    refDicGO = spiLib.reverseAndNormalizeDic(refDicGO, startYearX, maxEndYear)
    refDicGO = spiLibTotal.calcNaceAggregates(refDicGO, nomenclature, 'nama')
    
    refDicX = spiLib.normalizeDicSize(refDicX, startYearX, startYearX, maxEndYear)
    refDicM = spiLib.normalizeDicSize(refDicM, startYearM, startYearX, maxEndYear)
    
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)
    
    spiLibCreateTable.createTableCompetitionImportpen(nomenclature, refDicGO, refDicX, refDicM, startYearX, fileLog, tableName)

traitementFichierTXT(G_indicatorEurostat, G_unit, G_nomenclature, G_cpa, fichiersTXT, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()