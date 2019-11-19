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

#parametre NACE1 ou NACE2
NaceInput = sys.argv[1]
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path = sys.argv[2]

G_Nomenclature = NaceInput.lower()
G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'skilltech'

G_IndicatorEurostat = 'B1G'

dirUse = Path     
dirLog = dirUse + '\\Log'
dirTXT = dirUse + '\\Output'

if G_Nomenclature == "nace2" :
    G_Unit = 'CP_MEUR' 
    G_File = '\\nama_10_a??.tsv'  
    sbsFile = dirUse + '\\Input\\tsv\\nace2\\sbs_na_sca_r2.tsv'
else :
    G_Unit = 'MIO_EUR' 
    G_File = '\\nama_nace*_c.tsv'  
    sbsFile = dirUse + ''

fichiersTXT = glob.glob(dirUse + '\\Input\\tsv\\' + G_Nomenclature + G_File)
fileLog = open(dirLog + '\\createDBSkillTech' + G_Nomenclature + '.log', 'w')
    
def traitementFichierTXT(indicatorInputEurostat, unitEurostat, nomenclature, sbsFile = ''):
    startIndice         = 0
    dicIndicator        = {}
    dicIndicatorTotal   = {}
    dicNoCountry        = {}    
    dicNaceCheck        = {}
    dicNace             = {}
    dicNation           = {}
    indicatorEurostat   = indicatorInputEurostat
    dicNace             = spiLib.defSelectdicNaceSkillTech(nomenclature)
    dicNation           = DBAccess.lectureNationEurostat(dicNation)
    dicStartValue       = dict(startIndice=1,startCountry='',startNace='',startIndicator='',startValeur=0)
    
    minStartYear        = 99999
    maxEndYear          = -1
    
    for txt in fichiersTXT:
        fichierTXT     = open(txt,'r')
        rec1er         = fichierTXT.readline() #1er rec avec les meta
        lstrec         = rec1er.split(',')
        #on selectionne les colonne de l'input d'Eurostat        
        dicEurostat    = spiLib.defDicEurostat(lstrec)
        iUnit          = dicEurostat['unit']
        iNace          = dicEurostat['nace']
        iIndic         = dicEurostat['indic']
        iGeoTime       = dicEurostat['geotime']
        geotime        = lstrec[iGeoTime].split('\t')
        endYear        = geotime[1].strip()
        startYear      = geotime[-1].strip()
        #nace_r1,indic_sb,size_emp,geo\time
        #E,V11110,TOTAL,ES    9037     6410     3544     3311     3336     3084
        for ligneTXT in fichierTXT: 
            ligne         = ligneTXT.strip('\n').split(',') #RAPPEL strip enleve des extremites
            nace          = ligne[iNace].strip()
            indicator     = ligne[iIndic].strip()
            unit          = ligne[iUnit].strip()
            geoTime       = ligne[iGeoTime].split('\t')            
            geoEuroStat   = geoTime[0].strip()
            try:
                country = dicNation[geoEuroStat]                    
                timeSerie = geoTime[1:]

                if indicator == indicatorEurostat and dicNace.has_key(nace) and unit == unitEurostat:
                    dicNaceCheck[nace] = nace
                    vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                    dicStartValue = spiLib.defDicStartValue(timeSerie,country,nace,indicator,dicStartValue, endYear)
                    dicIndicator = spiLib.defDicIndicator(country,nace,vector,dicIndicator)
                    if int(endYear) > maxEndYear :
                        maxEndYear = int(endYear)
                    if int(startYear) < minStartYear :
                        minStartYear = int(startYear)
            except:
                dicNoCountry[geoEuroStat] = geoEuroStat   
        fichierTXT.close()
    fileLog.write('highIndice '+str(dicStartValue['startIndice'])+' highCountry '+dicStartValue['startCountry']+\
    ' Indicator '+dicStartValue['startIndicator']+' Nace '+dicStartValue['startNace']+' valeur '+str(dicStartValue['startValeur'])+'\n')
    spiLib.defnoCountry(dicNoCountry,fileLog)
    spiLib.defDicNaceCheck(dicNaceCheck,dicNace,fileLog)
    dicIndicator = spiLib.reverseAndNormalizeDic(dicIndicator, minStartYear, maxEndYear)
    
    if nomenclature == 'nace2' :
        dicSbs = {}
        fichierTXT     = open(sbsFile,'r')
        rec1er         = fichierTXT.readline()
        lstrec         = rec1er.split(',')
        dicEurostat    = spiLib.defDicEurostat(lstrec)
        iNace          = dicEurostat['nace']
        iIndic         = dicEurostat['indic']
        iGeoTime       = dicEurostat['geotime']
        geotime        = lstrec[iGeoTime].split('\t')
        endYear        = geotime[1].strip()
        startYear      = geotime[-1].strip()
        for ligneTXT in fichierTXT :
            ligne         = ligneTXT.strip('\n').split(',')
            nace          = ligne[iNace].strip()
            indicator     = ligne[iIndic].strip()
            geoTime       = ligne[iGeoTime].split('\t')            
            geoEuroStat   = geoTime[0].strip()
            
            try:
                country = dicNation[geoEuroStat]                    
                timeSerie = geoTime[1:]
                if indicator == 'V12150' and nace in ('N80', 'N81', 'N82') :
                    vector = spiLib.defVectorYears(timeSerie, startYear, endYear)
                    dicSbs = spiLib.defDicIndicator(country,nace,vector,dicSbs)
            except:
                continue
        fichierTXT.close()
        dicSbs = spiLib.reverseAndNormalizeDic(dicSbs, minStartYear, maxEndYear)
        dicSbs = spiLibTotal.createSkillTechNace2SbsTotal(dicSbs)
        dicRatio = spiLibTotal.createSkillTechNace2Ratio(dicSbs)
        del dicSbs
        
        dicIndicator = spiLibTotal.addSkillTechNace2RemainingCodes(dicIndicator, dicRatio)
                
    spiLibCreateTable.createTableSkillTech(nomenclature,dicIndicator,minStartYear,fileLog,G_tableName)
    
traitementFichierTXT(G_IndicatorEurostat,G_Unit,G_Nomenclature, sbsFile)
fileLog.close()
DBConnect.closeDB()       
    