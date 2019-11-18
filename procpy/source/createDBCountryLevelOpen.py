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
Path = sys.argv[1]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'country'
G_spiIndicator = 'open'
G_File = '\\nama_10_gdp.tsv'

G_Unit = 'CP_MEUR'  
G_IndicatorEurostat = ['B1GQ', 'P6', 'P7']

dirUse = Path     
dirLog = dirUse + '\\Log'
dirTXT = dirUse + '\\Output'
nomFichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File
fileLog = open(dirLog + '\\createDBCountryLevelOpen.log', 'w')

def traitementFichierTXT(indicatorInputEurostat, unitEurostat, nomFichierTXT):
    startIndice                 = 0
    dicIndicators               = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    indicatorEurostat           = indicatorInputEurostat
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    #dicStartValue       = dict(startIndice=1,startCountry='',startNace='',startIndicator='',startValeur=0)
    minimumYearWithActualData   = 999999
    
    fichierTXT     = open(nomFichierTXT,'r')
    rec1er         = fichierTXT.readline() #1er rec avec les meta
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iUnit          = dicEurostat['unit']
    iIndic         = dicEurostat['indic']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = geotime[1].strip()
    startYear      = geotime[-1].strip()
        
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',') #RAPPEL strip enleve des extremites
        indicator     = ligne[iIndic].strip()
        unit          = ligne[iUnit].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if indicator in indicatorEurostat and unit == unitEurostat:
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicators = spiLib.defDicIndicators(country,indicator,vector,dicIndicators)    
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    spiLib.defnoCountry(dicNoCountry,fileLog)
    dicIndicators = spiLib.reverseAndNormalizeDicIndicators(dicIndicators, minimumYearWithActualData, int(endYear))
    spiLibCreateTable.createTableCountryLevelOpen(dicIndicators,minimumYearWithActualData,fileLog,G_tableName)
    
traitementFichierTXT(G_IndicatorEurostat,G_Unit,nomFichierTXT)
fileLog.close()
DBConnect.closeDB()  
  