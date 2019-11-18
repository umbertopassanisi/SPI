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
Path = sys.argv[1]

G_startYear    = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName    = 'country'


G_File = 'htec_trd_tot4.tsv'
G_FileGdp = 'nama_10_gdp.tsv'

G_partner = 'WORLD'
G_flow = ['EXP', 'IMP']
G_unit = 'MIO_EUR'
G_unitGdp = 'CP_MEUR'
G_gdpIndicator = 'B1GQ'

dirUse        = Path     
dirLog        = dirUse + '\\Log'
dirTXT        = dirUse + '\\Output'
nomFichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File
nomFichierTXTGdp = dirUse + '\\Input\\tsv\\nonace\\' + G_FileGdp
fileLog       = open(dirLog + '\\createDBCountryLevelBtechBtechgdp.log', 'w')

def traitementFichierTXT(unitEurostat, flowEurostat, partnerEurostat, gdpIndicEurostat, nomFichierTXT, nomFichierTXTGdp, unitGdp):
    dicIndicator                = {}
    dicGdp                      = {}
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
            if flow in flowEurostat and partner == partnerEurostat and unit == unitEurostat:
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicator = spiLib.defDicFlow(country,flow,vector,dicIndicator)  
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    
    finalEndYear = endYear
    
    fichierTXT.close()
    
    fichierTXT     = open(nomFichierTXTGdp,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iUnit          = dicEurostat['unit']
    iIndic         = dicEurostat['indic']
    iGeoTime       = dicEurostat['geotime']
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = geotime[1].strip()
    startYear      = geotime[-1].strip()
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        unit          = ligne[iUnit].strip()
        indic         = ligne[iIndic].strip()
        geoTime       = ligne[iGeoTime].split('\t')            
        geoEuroStat   = geoTime[0].strip()
        
        try:
            country = dicNation[geoEuroStat]                    
            timeSerie = geoTime[1:]
            if indic == gdpIndicEurostat and unit == unitGdp:
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                dicGdp[country] = vector
        except:
            dicNoCountry[geoEuroStat] = geoEuroStat
    
    fichierTXT.close()
            
    spiLib.defnoCountry(dicNoCountry,fileLog)
    
    dicIndicator = spiLib.reverseAndNormalizeDic(dicIndicator, minimumYearWithActualData, int(finalEndYear))
    dicGdp = spiLib.reverseAndNormalizeDic(dicGdp, minimumYearWithActualData, int(finalEndYear))
    
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLibCreateTable.createTableCountryLevelBtechBtechgdp(dicIndicator,dicGdp,minimumYearWithActualData,fileLog,G_tableName)
    
traitementFichierTXT(G_unit,G_flow,G_partner, G_gdpIndicator,nomFichierTXT, nomFichierTXTGdp, G_unitGdp)
fileLog.close()
DBConnect.closeDB()