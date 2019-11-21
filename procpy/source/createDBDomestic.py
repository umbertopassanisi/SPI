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
#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[2].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[3]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'domestic'

if G_spiIndicator == 'lppind' :
    G_indicatorEurostatNumerator = 'B1G'
    if G_nomenclature == 'nace1' :
        G_indicatorEurostatDenominator = 'EMP'
        G_unitNumerator = 'MIO_NAC_CLV2005'
        G_unitDenominator = '1000PERS'
        G_fileNumerator = '\\nama_nace*_k.tsv'  
        G_fileDenominator = '\\nama_nace*_e.tsv'
        G_baseYear = 2005
    elif G_nomenclature == 'nace2' :
        G_indicatorEurostatDenominator = 'EMP_DC'
        G_unitNumerator = 'CLV10_MNAC'
        G_unitDenominator = 'THS_PER'
        G_fileNumerator = '\\nama_10_a??.tsv' 
        G_fileDenominator = '\\nama_10_a*_e.tsv'
        G_baseYear = 2010
    else :
        sys.exit()
        
elif G_spiIndicator == 'lphind' :
    G_indicatorEurostatNumerator = 'B1G'
    if G_nomenclature == 'nace1' :
        G_indicatorEurostatDenominator = 'EMP'
        G_unitNumerator = 'MIO_NAC_CLV2005'
        G_unitDenominator = '1000HRS'
        G_fileNumerator = '\\nama_nace*_k.tsv'  
        G_fileDenominator = '\\nama_nace*_e.tsv'
        G_baseYear = 2005
    elif G_nomenclature == 'nace2' :
        G_indicatorEurostatDenominator = 'EMP_DC'
        G_unitNumerator = 'CLV10_MNAC'
        G_unitDenominator = 'THS_HW'
        G_fileNumerator = '\\nama_10_a??.tsv' 
        G_fileDenominator = '\\nama_10_a*_e.tsv'
        G_baseYear = 2010
    else :
        sys.exit()
    
elif  G_spiIndicator == 'wpeind' :
    G_indicatorEurostatNumerator = 'D1'
    if G_nomenclature == 'nace1' :
        G_indicatorEurostatDenominator = 'EMP'
        G_unitNumerator = 'MIO_NAC'
        G_unitDenominator = '1000PERS'
        G_fileNumerator = '\\nama_nace*_c.tsv'  
        G_fileDenominator = '\\nama_nace*_e.tsv'
        G_baseYear = 2005
    elif G_nomenclature == 'nace2' :
        G_indicatorEurostatDenominator = 'EMP_DC'
        G_unitNumerator = 'CP_MNAC'
        G_unitDenominator = 'THS_PER'
        G_fileNumerator = '\\nama_10_a??.tsv' 
        G_fileDenominator = '\\nama_10_a*_e.tsv'
        G_baseYear = 2010
    else :
        sys.exit()
    
elif  G_spiIndicator == 'wphind' :
    G_indicatorEurostatNumerator = 'D1'
    if G_nomenclature == 'nace1' :
        G_indicatorEurostatDenominator = 'EMP'
        G_unitNumerator = 'MIO_NAC'
        G_unitDenominator = '1000HRS'
        G_fileNumerator = '\\nama_nace*_c.tsv'  
        G_fileDenominator = '\\nama_nace*_e.tsv'
        G_baseYear = 2005
    elif G_nomenclature == 'nace2' :
        G_indicatorEurostatDenominator = 'EMP_DC'
        G_unitNumerator = 'CP_MNAC'
        G_unitDenominator = 'THS_HW'
        G_fileNumerator = '\\nama_10_a??.tsv' 
        G_fileDenominator = '\\nama_10_a*_e.tsv'
        G_baseYear = 2010
    else :
        sys.exit()
    
elif  G_spiIndicator == 'ulcind' :
    G_indicatorEurostatNumerator = 'D1'
    G_indicatorEurostatDenominator = 'B1G'
    if G_nomenclature == 'nace1' :
        G_unitNumerator = 'MIO_NAC'
        G_unitDenominator = 'MIO_NAC_CLV2005'
        G_fileNumerator = '\\nama_nace*_c.tsv'  
        G_fileDenominator = '\\nama_nace*_k.tsv'
        G_baseYear = 2005
    elif G_nomenclature == 'nace2' :
        G_unitNumerator = 'CP_MNAC'
        G_unitDenominator = 'CLV10_MNAC'
        G_fileNumerator = '\\nama_10_a??.tsv' 
        G_fileDenominator = '\\nama_10_a??.tsv'
        G_baseYear = 2010
    else :
        sys.exit()
    
else :
    sys.exit()


dirUse = G_path     
dirLog = dirUse + '\\Log'
dirTXT = dirUse + '\\Output'
fichiersTXTNumerator = glob.glob(dirUse + '\\Input\\tsv\\' + G_nomenclature + G_fileNumerator)
fichiersTXTDenominator = glob.glob(dirUse + '\\Input\\tsv\\' + G_nomenclature + G_fileDenominator)
fileLog = open(dirLog + '\\createDBDomesticProductivityNet' + G_nomenclature + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicatorEurostatDenominator, indicatorEurostatNumerator, unitDenominator, unitNumerator, nomenclature, filesDenominator, filesNumerator, baseYear, indicatorSpi, fileLog, tableName):
    dicIndicatorNumerator       = {}
    dicIndicatorDenominator     = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    dicNaceCheck                = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    dicNace                     = spiLib.defSelectdicNace(nomenclature, 'nama')
    minimumYearWithActualData   = 999999
    maxEndYear                  = -1
    
    filesNumerator.sort()
    filesNumerator.reverse()    
    filesDenominator.sort()
    filesDenominator.reverse()
    
    for txt in filesNumerator :
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

                if indicator == indicatorEurostatNumerator and dicNace.has_key(nace) and unit == unitNumerator:
                    vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                    minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                    dicIndicatorNumerator = spiLib.defDicIndicator(country,nace,vector,dicIndicatorNumerator)
                    if int(endYear) > maxEndYear :
                        maxEndYear = int(endYear)
            except :
                dicNoCountry[geo] = geo
                
        file.close()
    
    dicIndicatorNumerator = spiLib.reverseAndNormalizeDic(dicIndicatorNumerator, minimumYearWithActualData, maxEndYear)
    dicIndicatorNumerator = spiLibTotal.calcNaceAggregates(dicIndicatorNumerator, nomenclature, 'nama')
    
    for txt in filesDenominator :
        file           = open(txt, 'r')
        line1st        = file.readline()
        list1st        = line1st.split(',')
        dicEurostat    = spiLib.defDicEurostat(list1st)
        iUnit          = dicEurostat['unit']
        iIndic         = dicEurostat['indic']
        iNace          = dicEurostat['nace']
        iGeoTime       = dicEurostat['geotime']
        iSector        = dicEurostat['sector'] 
        geotime        = list1st[iGeoTime].split('\t')
        
        endYear        = geotime[1].strip()
        startYear      = geotime[-1].strip()
        
        for line in file :
            lineList      = line.strip('\n').split(',')
            nace          = lineList[iNace].strip()
            indicator     = lineList[iIndic].strip()
            unit          = lineList[iUnit].strip()
            geoTime       = lineList[iGeoTime].split('\t')  
            if iSector == -1 : 
                sector = 'S1'
            else :
                sector = lineList[iSector].strip()
            geo           = geoTime[0].strip()
            
            try :
                dicNaceCheck[nace] = nace
                country = dicNation[geo]                    
                timeSerie = geoTime[1:]

                if indicator == indicatorEurostatDenominator and dicNace.has_key(nace) and unit == unitDenominator and sector == 'S1':
                    vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                    dicIndicatorDenominator = spiLib.defDicIndicator(country,nace,vector,dicIndicatorDenominator)
            except :
              dicNoCountry[geo] = geo  
        
        file.close()
        
    dicIndicatorDenominator = spiLib.reverseAndNormalizeDic(dicIndicatorDenominator, minimumYearWithActualData, maxEndYear)
    dicIndicatorDenominator = spiLibTotal.calcNaceAggregates(dicIndicatorDenominator, nomenclature, 'nama')
    
    #The following lines are added on demand of B2 team to calculate aggregates that cannot be extracted from the nama_nace10_e file 
    if nomenclature == 'nace2' and indicatorEurostatDenominator == 'EMP':
        dicIndicatorDenominator = spiLibTotal.calcNace2EmpAggr(dicIndicatorDenominator)
    
    ##############################################################################################################################
    
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)   
    
    spiLibCreateTable.createTableDomesticIndex(nomenclature,dicIndicatorNumerator, dicIndicatorDenominator, indicatorSpi, minimumYearWithActualData, baseYear,fileLog, tableName)     
    
traitementFichierTXT(G_indicatorEurostatDenominator, G_indicatorEurostatNumerator, G_unitDenominator, G_unitNumerator, G_nomenclature, fichiersTXTDenominator, fichiersTXTNumerator, G_baseYear, G_spiIndicator, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()