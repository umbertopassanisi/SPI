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

G_spiIndicator = sys.argv[1]

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path = sys.argv[2]

G_startYear    = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName    = 'country'

G_Unit = 'PC'
G_age  = 'Y15-64'    
G_sex  = 'T'

## removed 20180326
##if G_spiIndicator   == 'edusl' :
##    G_File = 'edat_lfse_05.tsv'
##elif G_spiIndicator == 'edusup' :
##    G_File = 'edat_lfse_06.tsv'
##elif G_spiIndicator == 'edut' :
##    G_File = 'edat_lfse_07.tsv'
##elif G_spiIndicator == 'edust' :
##    G_File = 'edat_lfse_08.tsv'
##else :
##    sys.exit()
G_File = 'edat_lfse_03.tsv'  # added 20190326

dirUse        = Path     
dirLog        = dirUse + '\\Log'
dirTXT        = dirUse + '\\Output'
nomFichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File

fileLog       = open(dirLog + '\\createDBCountryLevel' + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicatorSpi, unitEurostat, ageEurostat, sexEurostat, nomFichierTXT):
    dicIndicator                = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    minimumYearWithActualData   = 999999

    ## added 20190326
    iscedTOindicator = {
        'ED0-2': 'edusl',
        'ED3_4': 'edusup',
        'ED5-8': 'edut',
        'ED3-8': 'edust'
    }
    
    fichierTXT     = open(nomFichierTXT,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iUnit          = dicEurostat['unit']
    iAge           = dicEurostat['age']
    iSex           = dicEurostat['sex']
    iIsced         = dicEurostat['indic']  ## added 20190326
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = geotime[1].strip()
    startYear      = geotime[-1].strip()
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        age           = ligne[iAge].strip()
        unit          = ligne[iUnit].strip()
        sex           = ligne[iSex].strip()
        indicator     = iscedTOindicator[ligne[iIsced].strip()]  ## added 20190326
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if sex == sexEurostat and age == ageEurostat and unit == unitEurostat and indicator == indicatorSpi:  # added indicator check to if statement 20190326
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicator[country] = vector    
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
            
    spiLib.defnoCountry(dicNoCountry,fileLog)
    dicIndicator = spiLib.reverseAndNormalizeDicNoIndicator(dicIndicator, minimumYearWithActualData, int(endYear))
    spiLibCreateTable.createTableCountryLevelEduTech(dicIndicator,G_spiIndicator,minimumYearWithActualData,fileLog,G_tableName)
    
traitementFichierTXT(G_spiIndicator,G_Unit,G_age,G_sex,nomFichierTXT)
fileLog.close()
DBConnect.closeDB()  
    
    

