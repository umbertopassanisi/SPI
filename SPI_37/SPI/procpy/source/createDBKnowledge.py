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
#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[2].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[3]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'knowledge'

if G_spiIndicator == 'rdintens' :
    G_indicatorEurostatDenominator = 'B1G'
    G_unitNumerator = 'MIO_EUR'
    if G_nomenclature == 'nace1' :
        G_fileNumerator = '\\rd_e_berdind.tsv'
        G_fileDenominator = '\\nama_nace*_c.tsv'
        G_unitDenominator = 'MIO_EUR'
    elif G_nomenclature == 'nace2' :
        G_fileNumerator = '\\rd_e_berdindr2.tsv'
        G_fileDenominator = '\\nama_10_a??.tsv'
        G_unitDenominator = 'CP_MEUR'
    else :
        sys.exit() 
elif G_spiIndicator == 'patintens' :
    G_indicatorEurostatDenominator = 'B1G'
    G_unitDenominator = 'CP_MEUR'
    if G_nomenclature == 'nace1' :
        G_unitNumerator = 'NR'
        G_fileNumerator = '\\pat_ep_nnac.tsv'
        G_fileDenominator = '\\nama_nace*_c.tsv'
        G_unitDenominator = 'MIO_EUR'
    elif G_nomenclature == 'nace2' :
        G_unitNumerator = 'NR'
        G_fileNumerator = '\\pat_ep_nnac2.tsv'
        G_fileDenominator = '\\nama_10_a??.tsv'
        G_unitDenominator = 'CP_MEUR'
    else :
        sys.exit() 
elif G_spiIndicator == 'patintrd' :
    G_indicatorEurostatDenominator = ''
    G_unitDenominator = 'MIO_EUR'
    if G_nomenclature == 'nace1' :
        G_unitNumerator = 'NR'
        G_fileNumerator = '\\pat_ep_nnac.tsv'
        G_fileDenominator = '\\rd_e_berdind.tsv'
    elif G_nomenclature == 'nace2' :
        G_unitNumerator = 'NR'
        G_fileNumerator = '\\pat_ep_nnac2.tsv'
        G_fileDenominator = '\\rd_e_berdindr2.tsv'
    else :
        sys.exit() 
    
else :
    sys.exit()
    
dirUse = G_path     
dirLog = dirUse + '\\Log'
dirTXT = dirUse + '\\Output'
fichierTXTNumerator = dirUse + '\\Input\\tsv\\' + G_nomenclature + G_fileNumerator
fichiersTXTDenominator = glob.glob(dirUse + '\\Input\\tsv\\' + G_nomenclature + G_fileDenominator)
fileLog = open(dirLog + '\\createDBKnowledge' + G_nomenclature + G_spiIndicator + '.log', 'w')

def traitementFichierTXT(indicatorEurostatDenominator, unitDenominator, unitNumerator, nomenclature, filesDenominator, fileNumerator, indicatorSpi, fileLog, tableName):
    dicIndicatorNumerator       = {}
    dicIndicatorDenominator     = {}
    dicNoCountry                = {}    
    dicNation                   = {}
    dicNaceCheck                = {}
    dicNation                   = DBAccess.lectureNationEurostat(dicNation)
    dicNace                     = spiLib.defSelectdicNace(nomenclature, 'nama')
    minimumYearWithActualData   = 999999
    maxEndYear                  = -1

    filesDenominator.sort()
    filesDenominator.reverse()
    
    file = open(fileNumerator, 'r')
    line1st        = file.readline()
    list1st        = line1st.split(',')
    dicEurostat    = spiLib.defDicEurostat(list1st)
    iUnit          = dicEurostat['unit']
    iNace          = dicEurostat['nace']
    iGeoTime       = dicEurostat['geotime']
    geotime        = list1st[iGeoTime].split('\t')
    
    endYear        = geotime[1].strip()
    startYear      = geotime[-1].strip()
    
    #This code is added to create special aggregates asked on 30-09-2016
    if (indicatorSpi == 'patintens' or indicatorSpi == 'patintrd') and nomenclature == 'nace2' :
        dicNace['C10'] = 'C'
        dicNace['C11'] = 'C'
        dicNace['C12'] = 'C'
        dicNace['C13'] = 'C'
        dicNace['C14'] = 'C'
        dicNace['C15'] = 'C'
        dicNace['C31'] = 'C'
        dicNace['C32'] = 'C'
    #________________________________________________________________________
        
    for line in file :
        lineList      = line.strip('\n').split(',')
        nace          = lineList[iNace].strip()
        unit          = lineList[iUnit].strip()
        geoTime       = lineList[iGeoTime].split('\t')            
        geo           = geoTime[0].strip()
        
        try :
            dicNaceCheck[nace] = nace
            country = dicNation[geo]                    
            timeSerie = geoTime[1:]

            if nace in dicNace and unit == unitNumerator:
                vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                minimumYearWithActualData = spiLib.findMinimumYearWithActualData(timeSerie,int(startYear),minimumYearWithActualData)
                dicIndicatorNumerator = spiLib.defDicIndicator(country,nace,vector,dicIndicatorNumerator)
                if int(endYear) > maxEndYear :
                    maxEndYear = int(endYear)
        except :
            dicNoCountry[geo] = geo
            
    file.close()
    
    dicIndicatorNumerator = spiLib.reverseAndNormalizeDic(dicIndicatorNumerator, minimumYearWithActualData, maxEndYear)
    
    #This code is added to create special aggregates asked on 30-09-2016
    if (indicatorSpi == 'patintens' or indicatorSpi == 'patintrd') and nomenclature == 'nace2' :
        for country in dicIndicatorNumerator :
            try :
                C10 = dicIndicatorNumerator[country]['C10']
                C11 = dicIndicatorNumerator[country]['C11']
                C12 = dicIndicatorNumerator[country]['C12']
            except :
                C10 = []
                C11 = []
                C12 = []
            
            try :
                C13 = dicIndicatorNumerator[country]['C13']
                C14 = dicIndicatorNumerator[country]['C14']
                C15 = dicIndicatorNumerator[country]['C15']
            except :
                C13 = []
                C14 = []
                C15 = []
                
            try :
                C31 = dicIndicatorNumerator[country]['C31']
                C32 = dicIndicatorNumerator[country]['C32']
            except :
                C31 = []
                C32 = []
                
            res = []

            for i in range(0, len(C10)) :
                if C10[i] == ':' or C11[i] == ':' or C12[i] == ':' :
                    res.append(':')
                else :
                    res.append(str(float(C10[i]) + float(C11[i]) + float(C12[i])))
                            
            if len(res) > 0 :
                dicIndicatorNumerator[country]['C10-C12'] = res
                
            res = []
            
            for i in range(0, len(C13)) :
                if C13[i] == ':' or C14[i] == ':' or C15[i] == ':' :
                    res.append(':')
                else :
                    res.append(str(float(C13[i]) + float(C14[i]) + float(C15[i])))
                            
            if len(res) > 0 :
                dicIndicatorNumerator[country]['C13-C15'] = res
                
            res = []
            
            for i in range(0, len(C31)) :
                if C31[i] == ':' or C32[i] == ':' :
                    res.append(':')
                else :
                    res.append(str(float(C31[i]) + float(C32[i])))
                            
            if len(res) > 0 :
                dicIndicatorNumerator[country]['C31_C32'] = res
    #__________________________________________________________________________
    
    dicIndicatorNumerator = spiLibTotal.calcNaceAggregates(dicIndicatorNumerator, nomenclature, 'nama')
    
    for txt in filesDenominator :
        file           = open(txt, 'r')
        line1st        = file.readline()
        list1st        = line1st.split(',')
        dicEurostat    = spiLib.defDicEurostat(list1st)
        iUnit          = dicEurostat['unit']
        try :
            iIndic         = dicEurostat['indic']
        except :
            pass
        iNace          = dicEurostat['nace']
        iGeoTime       = dicEurostat['geotime']
        geotime        = list1st[iGeoTime].split('\t')
        
        endYear        = geotime[1].strip()
        startYear      = geotime[-1].strip()
        for line in file :
            lineList      = line.strip('\n').split(',')
            nace          = lineList[iNace].strip()
            if iIndic != -1:
                indicator     = lineList[iIndic].strip()
            else :
                indicator     = 'noindicator'
            unit          = lineList[iUnit].strip()
            geoTime       = lineList[iGeoTime].split('\t')            
            geo           = geoTime[0].strip()
            
            try :
                dicNaceCheck[nace] = nace
                country = dicNation[geo]                    
                timeSerie = geoTime[1:]
                if indicator != 'noindicator':
                    if indicator == indicatorEurostatDenominator and nace in dicNace and unit == unitDenominator:
                        vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                        dicIndicatorDenominator = spiLib.defDicIndicator(country,nace,vector,dicIndicatorDenominator)   
                         
                else :
                    if nace in dicNace and unit == unitDenominator:
                        vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                        dicIndicatorDenominator = spiLib.defDicIndicator(country,nace,vector,dicIndicatorDenominator)
            except :
              dicNoCountry[geo] = geo  
        
        file.close()
        
    dicIndicatorDenominator = spiLib.reverseAndNormalizeDic(dicIndicatorDenominator, minimumYearWithActualData, maxEndYear)
    dicIndicatorDenominator = spiLibTotal.calcNaceAggregates(dicIndicatorDenominator, nomenclature, 'nama')
      
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)  
    
    spiLibCreateTable.createTableNacePercentage(nomenclature,dicIndicatorNumerator, dicIndicatorDenominator, indicatorSpi, minimumYearWithActualData,fileLog, tableName)

traitementFichierTXT(G_indicatorEurostatDenominator, G_unitDenominator, G_unitNumerator, G_nomenclature, fichiersTXTDenominator, fichierTXTNumerator, G_spiIndicator, fileLog, G_tableName)
fileLog.close()
DBConnect.closeDB()