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

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_spiIndicator = sys.argv[1]

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path = sys.argv[2]

G_startYear    = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName    = 'country'

G_File = 'hrst_st_nocc.tsv'
G_File2 = 'nama_10_a10_e.tsv'

if G_spiIndicator == 'hrst' :
    G_category = 'HRST'
    G_age      = 'Y15-74'
    G_isco     = 'TOTAL'
    G_unit     = 'THS' 
    
    G_naceCode = 'TOTAL'
    G_item     = 'EMP_DC'
    G_unit2    = 'THS_PER'
    
else :
    sys.exit()
    
dirUse        = Path     
dirLog        = dirUse + '\\Log'
dirTXT        = dirUse + '\\Output'
nomFichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File
nomFichierTXT2= dirUse + '\\Input\\tsv\\nace2\\' + G_File2
fileLog       = open(dirLog + '\\createDBCountryLevel' + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicatorSpi, categoryEurostat, ageEurostat, iscoEurostat, unitEurostat, nomFichierTXT, nomFichierTXT2, naceEurostat, itemEurostat, unitEurostat2):
    dicIndicator                = {}
    dicIndicator2               = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    minimumYearWithActualData   = 999999
    
    fichierTXT     = open(nomFichierTXT,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iCategory      = dicEurostat['category']
    iUnit          = dicEurostat['unit']
    iIsco          = dicEurostat['isco']
    iAge      = dicEurostat['age']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = geotime[1].strip()
    startYear      = geotime[-1].strip()
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        category      = ligne[iCategory].strip()
        isco          = ligne[iIsco].strip()
        age           = ligne[iAge].strip()
        unit          = ligne[iUnit].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if unit == unitEurostat and age == ageEurostat and isco == iscoEurostat and category == categoryEurostat :
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicator[country] = vector  
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    
    fichierTXT.close()
    spiLib.defnoCountry(dicNoCountry,fileLog)
    
    fichierTXT     = open(nomFichierTXT2,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iNace          = dicEurostat['nace']
    iUnit          = dicEurostat['unit']
    iIndic         = dicEurostat['indic']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear2       = geotime[1].strip()
    startYear2     = geotime[-1].strip()
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        nace          = ligne[iNace].strip()
        unit          = ligne[iUnit].strip()
        indic         = ligne[iIndic].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if unit == unitEurostat2 and indic == itemEurostat and nace == naceEurostat :
                vector = spiLib.defVectorYears(timeSerie, startYear2, endYear2)
                dicIndicator2[country] = vector  
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    
    fichierTXT.close()
    
    dicIndicator = spiLib.reverseAndNormalizeDic(dicIndicator, minimumYearWithActualData, int(endYear))
    dicIndicator2 = spiLib.reverseAndNormalizeDic(dicIndicator2, minimumYearWithActualData, int(endYear))
    
    spiLibCreateTable.createTableCountryLevelFdi(dicIndicator, dicIndicator2, G_spiIndicator, minimumYearWithActualData, fileLog, G_tableName)
    
traitementFichierTXT(G_spiIndicator, G_category, G_age, G_isco, G_unit,nomFichierTXT, nomFichierTXT2, G_naceCode, G_item, G_unit2)
fileLog.close()
DBConnect.closeDB()  