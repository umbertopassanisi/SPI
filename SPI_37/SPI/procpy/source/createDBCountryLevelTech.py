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

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_spiIndicator = sys.argv[1]

#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path = sys.argv[2]

G_startYear    = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName    = 'country'

G_partner = 'WORLD'
G_File = 'htec_trd_tot4.tsv'

if G_spiIndicator   == 'xtechsh' :
    G_flow = 'EXP'
    G_unit = 'PC_TOT'
elif G_spiIndicator   == 'xtech' :
    G_flow = 'EXP'
    G_unit = 'MIO_EUR'
elif G_spiIndicator   == 'mtechsh' :
    G_flow = 'IMP'
    G_unit = 'PC_TOT'
elif G_spiIndicator   == 'mtech' :
    G_flow = 'IMP'
    G_unit = 'MIO_EUR'
else :
    sys.exit()
    
dirUse        = Path     
dirLog        = dirUse + '\\Log'
dirTXT        = dirUse + '\\Output'
nomFichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File
fileLog       = open(dirLog + '\\createDBCountryLevel' + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicatorSpi, unitEurostat, flowEurostat, partnerEurostat, nomFichierTXT):
    dicIndicator                = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    minimumYearWithActualData   = 999999
    
    fichierTXT     = open(nomFichierTXT,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iUnit          = dicEurostat['unit']
    iFlow          = dicEurostat['flow']
    iPartner       = dicEurostat['partner']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = geotime[1].strip()
    startYear      = geotime[-1].strip()
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        flow          = ligne[iFlow].strip()
        unit          = ligne[iUnit].strip()
        partner       = ligne[iPartner].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if flow == flowEurostat and partner == partnerEurostat and unit == unitEurostat:
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicator[country] = vector  
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
            
    spiLib.defnoCountry(dicNoCountry,fileLog)
    dicIndicator = spiLib.reverseAndNormalizeDicNoIndicator(dicIndicator, minimumYearWithActualData, int(endYear))
    spiLibCreateTable.createTableCountryLevelEduTech(dicIndicator,G_spiIndicator,minimumYearWithActualData,fileLog,G_tableName)
    
traitementFichierTXT(G_spiIndicator,G_unit,G_flow,G_partner,nomFichierTXT)
fileLog.close()
DBConnect.closeDB()  
    
    