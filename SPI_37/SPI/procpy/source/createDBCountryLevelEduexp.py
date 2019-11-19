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

G_spiIndicator = sys.argv[1]

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path = sys.argv[2]

G_startYear    = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName    = 'country'

G_File = 'educ_figdp.tsv'
G_file2 = 'educ_uoe_fine06.tsv'

if G_spiIndicator == 'eduexp' :
    G_eurostatIndicator = 'FP01_1'
    G_eurostatIndicator2 = 'ED02-8'
    G_unit2 = 'PC_GDP'
else :
    sys.exit()
    
dirUse        = Path     
dirLog        = dirUse + '\\Log'
dirTXT        = dirUse + '\\Output'
nomFichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File
nomFichierTXT2 = dirUse + '\\Input\\tsv\\nonace\\' + G_file2
fileLog       = open(dirLog + '\\createDBCountryLevel' + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicatorSpi, indicatorEurostat, nomFichierTXT, nomFichierTXT2, indicatorEurostat2, eurostatUnit):
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
    iIndic         = dicEurostat['indic']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = int(geotime[1].strip())
    startYear      = int(geotime[-1].strip())
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        indic         = ligne[iIndic].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if indic == indicatorEurostat :
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicator[country] = vector  
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    
    fichierTXT.close()
    dicIndicator = spiLib.reverseAndNormalizeDicNoIndicator(dicIndicator, minimumYearWithActualData, int(endYear))
    
    fichierTXT     = open(nomFichierTXT2,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iIndic         = dicEurostat['indic']
    iUnit          = dicEurostat['unit']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear2       = int(geotime[1].strip())
    startYear2     = int(geotime[-1].strip())
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        indic         = ligne[iIndic].strip()
        unit          = ligne[iUnit].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if indic == indicatorEurostat2 and unit == eurostatUnit :
                vector = spiLib.defVectorYears(timeSerie, startYear2, endYear2)
                dicIndicator2[country] = vector  
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    
    fichierTXT.close()
    dicIndicator2 = spiLib.reverseAndNormalizeDicNoIndicator(dicIndicator2, int(startYear2), int(endYear2))
    
    for country in dicIndicator :
        if country not in dicIndicator2 :
            dicIndicator2[country] = []
            for i in range(startYear2-1, endYear2) :
                dicIndicator2[country].append(':')
        
    for country in dicIndicator2 : 
        if country not in dicIndicator :
            dicIndicator[country] = []
            for i in range(minimumYearWithActualData-1, endYear) :
                dicIndicator[country].append(':')
                
    yearGap = startYear2 - endYear - 1
    
    if yearGap == 0 :
        for country in dicIndicator :
            dicIndicator[country].extend(dicIndicator2[country])
    elif yearGap > 0 :
        fillingVector = []
        for i in range(0, yearGap) :
            fillingVector.append(':')
        for country in dicIndicator :
            dicIndicator[country].extend(fillingVector)
            dicIndicator[country].extend(dicIndicator2[country])
    elif yearGap < 0 :
        for country in dicIndicator :
            del dicIndicator[country][yearGap:]
        for country in dicIndicator :
            dicIndicator[country].extend(dicIndicator2[country])  
        
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLibCreateTable.createTableCountryLevelEduTech(dicIndicator,G_spiIndicator,minimumYearWithActualData,fileLog,G_tableName)
    
traitementFichierTXT(G_spiIndicator,G_eurostatIndicator,nomFichierTXT, nomFichierTXT2, G_eurostatIndicator2, G_unit2)
fileLog.close()
DBConnect.closeDB()  