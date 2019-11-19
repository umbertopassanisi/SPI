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
G_File = 'bop_fdi_main.tsv'
G_File2 = 'bop_fdi6_geo.tsv'
G_FileGdp = 'nama_10_gdp.tsv'
  
G_unit = 'MIO_EUR'
G_gdpUnit = 'CP_MEUR'
G_gdpIndicator = 'B1GQ'

if G_spiIndicator == 'fdifineu27' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '555'
    G_partner           = 'EU27'
    G_partner2          = 'EU27'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdifineu28' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '555'
    G_partner           = 'EU28'
    G_partner2          = 'EU28'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdifinexeu27' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '555'
    G_partner           = 'EXT_EU27'
    G_partner2          = 'EXT_EU27'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdifinexeu28' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '555'
    G_partner           = 'EXT_EU28'
    G_partner2          = 'EXT_EU28'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdifinworld' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '555'
    G_partner           = 'WORLD'
    G_partner2          = 'WRL_REST'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdifouteu27' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '505'
    G_partner           = 'EU27'
    G_partner2          = 'EU27'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdifouteu28' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '505'
    G_partner           = 'EU28'
    G_partner2          = 'EU28'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdifoutexeu27' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '505'
    G_partner           = 'EXT_EU27'
    G_partner2          = 'EXT_EU27'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdifoutexeu28' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '505'
    G_partner           = 'EXT_EU28'
    G_partner2          = 'EXT_EU28'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdifoutworld' :
    G_eurostatIndicator = 'FLOWS'
    G_post              = '505'
    G_partner           = 'WORLD'
    G_partner2          = 'WRL_REST'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdisineu27' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '555'
    G_partner           = 'EU27'
    G_partner2          = 'EU27'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdisineu28' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '555'
    G_partner           = 'EU28'
    G_partner2          = 'EU28'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdisinexeu27' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '555'
    G_partner           = 'EXT_EU27'
    G_partner2          = 'EXT_EU27'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdisinexeu28' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '555'
    G_partner           = 'EXT_EU28'
    G_partner2          = 'EXT_EU28'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdisinworld' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '555'
    G_partner           = 'WORLD'
    G_partner2          = 'WRL_REST'
    G_item              = 'DI__D__F'
elif G_spiIndicator == 'fdisouteu27' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '505'
    G_partner           = 'EU27'
    G_partner2          = 'EU27'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdisouteu28' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '505'
    G_partner           = 'EU28'
    G_partner2          = 'EU28'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdisoutexeu27' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '505'
    G_partner           = 'EXT_EU27'
    G_partner2          = 'EXT_EU27'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdisoutexeu28' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '505'
    G_partner           = 'EXT_EU28'
    G_partner2          = 'EXT_EU28'
    G_item              = 'DO__D__F'
elif G_spiIndicator == 'fdisoutworld' :
    G_eurostatIndicator = 'STOCKS'
    G_post              = '505'
    G_partner           = 'WORLD'
    G_partner2          = 'WRL_REST'
    G_item              = 'DO__D__F'
else :
    sys.exit()
    
dirUse = Path     
dirLog = dirUse + '\\Log'
dirTXT = dirUse + '\\Output'
fichierTXT = dirUse + '\\Input\\tsv\\nonace\\' + G_File
fichierTXTGdp = dirUse + '\\Input\\tsv\\nonace\\' + G_FileGdp
fichierTXT2 = dirUse + '\\Input\\tsv\\nace2\\' + G_File2
fileLog = open(dirLog + '\\createDBCountryLevel' + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(tableName, spiIndicator, indicEurostat, postEurostat, unitEurostat, partnerEurostat, gdpIndicEurostat, nomFichierTXT, nomFichierTXTGdp, nomFichierTXT2, partnerEurostat2, itemEurostat, gdpUnit):
    dicIndicator                = {}
    dicIndicator2               = {}
    dicGdp                      = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    minimumYearWithActualData   = 999999
    
    fichierTXT     = open(nomFichierTXT,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iIndic         = dicEurostat['indic']
    iPostTime      = dicEurostat['post']
    iPartner       = dicEurostat['partner']
    iGeo           = dicEurostat['geotime']
    
    posttime       = lstrec[iPostTime].split('\t')
    endYear        = int(posttime[1].strip())
    startYear      = int(posttime[-1].strip())
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        indic         = ligne[iIndic].strip()
        geo           = ligne[iGeo].strip()
        partner       = ligne[iPartner].strip()
        postTime      = ligne[iPostTime].split('\t')
        post          = postTime[0].strip()
        
        try:
            country = dicNation[geo]                    
            timeSerie = postTime[1:]
            if partner == partnerEurostat and post == postEurostat and indic == indicEurostat :
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicator[country] = vector 
        except:
            dicNoCountry[geo] = geo
    
    fichierTXT.close()        
    dicIndicator   = spiLib.reverseAndNormalizeDic(dicIndicator, minimumYearWithActualData, endYear)
    fileEndYear   = endYear
           
    fichierTXT     = open(nomFichierTXT2,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iIndic         = dicEurostat['indic']
    iPartnerTime   = dicEurostat['partner']
    iGeo           = dicEurostat['geotime']
    iItem          = dicEurostat['item']
           
    geotime         = lstrec[iGeo].split('\t')
    endYear2        = int(geotime[1].strip())
    startYear2      = int(geotime[-1].strip())
    
    for ligneTXT in fichierTXT: 
        ligne         = ligneTXT.strip('\n').split(',')
        indic         = ligne[iIndic].strip()
        item          = ligne[iItem].strip()
        partner       = ligne[iPartnerTime].strip()
        geotime       = ligne[iGeo].split('\t')
        geo           = geotime[0].strip()

        try:
            country = dicNation[geo]                    
            timeSerie = geotime[1:]
            if partner == partnerEurostat2 and indic == indicEurostat  and item == itemEurostat:
                vector = spiLib.defVectorYears(timeSerie, startYear2, endYear2)
                dicIndicator2[country] = vector   
        except:
            dicNoCountry[geo] = geo           
    
    fichierTXT.close()      
    dicIndicator2   = spiLib.reverseAndNormalizeDic(dicIndicator2, startYear2, endYear2)
    finalEndYear   = endYear2    
            
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
    
    fichierTXT     = open(nomFichierTXTGdp,'r')
    rec1er         = fichierTXT.readline()
    lstrec         = rec1er.split(',')
    dicEurostat    = spiLib.defDicEurostat(lstrec)
    iIndic         = dicEurostat['indic']
    iGeoTime       = dicEurostat['geotime']
    iUnit          = dicEurostat['unit']
    
    geotime        = lstrec[iGeoTime].split('\t')
    endYear        = int(geotime[1].strip())
    startYear      = int(geotime[-1].strip())
    
    for ligneTXT in fichierTXT :
        ligne       = ligneTXT.strip('\n').split(',')
        indic       = ligne[iIndic].strip()
        unit        = ligne[iUnit].strip()
        geoTime     = ligne[iGeoTime].split('\t')            
        geoEurostat = geoTime[0].strip()
        
        try:
            country = dicNation[geoEurostat]                    
            timeSerie = geoTime[1:]
            if indic == gdpIndicEurostat and unit == gdpUnit:
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                dicGdp[country] = vector
        except:
            dicNoCountry[geoEurostat] = geoEurostat        
        
    fichierTXT.close()
    dicGdp = spiLib.reverseAndNormalizeDic(dicGdp, minimumYearWithActualData, finalEndYear)
    
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLibCreateTable.createTableCountryLevelFdi(dicIndicator,dicGdp,spiIndicator,minimumYearWithActualData,fileLog,tableName)
            
traitementFichierTXT(G_tableName, G_spiIndicator, G_eurostatIndicator, G_post, G_unit, G_partner, G_gdpIndicator, fichierTXT, fichierTXTGdp, fichierTXT2, G_partner2, G_item, G_gdpUnit)
fileLog.close()
DBConnect.closeDB()