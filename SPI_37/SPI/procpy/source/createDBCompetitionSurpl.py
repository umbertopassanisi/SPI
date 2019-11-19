import sys
import csv
import re
from glob import glob
from pprint import pprint
import spiLib
import spiLibTotal
import spiLibCreateTable
import DBConnect
import DBAccess

nomenclature = sys.argv[1]
path = sys.argv[2]

if nomenclature == 'nace2' :
    filePaths = glob(path +'\\Input\\tsv\\nace2\\sbs_na*.tsv')
elif nomenclature == 'nace1' :
    filePaths = glob(path +'\\Input\\tsv\\nace1\\sbs_sc*.tsv')
filePaths.reverse()#last file sbs_na_sca_r2 has less data available

indicNumerator = 'V12170'
indicDenominator = 'V12110'

def traitementFichierTXT(nomenclature, indicNumerator, indicDenominator, filePaths):
    dicNumerator = {}
    dicDenominator = {}
    
    dicNace = spiLib.defSelectdicNace(nomenclature, 'sbs')
    dicNation = DBAccess.lectureNationEurostat({})
    
    maxEndYear = -1
    minStartYear = 9999
    
    for filePath in filePaths :
        with open(filePath, 'r') as file :
            csvFile = csv.reader(file, delimiter = '\t')
            firstLine = csvFile.next()
            metaLabel = firstLine[0].split(',')
            dicEurostat = spiLib.defDicEurostat(metaLabel)
            iNace = dicEurostat['nace']
            iIndic = dicEurostat['indic']
            iGeoTime = dicEurostat['geotime']
            iSize = dicEurostat['size']
            
            endYear        = firstLine[1].strip()
            startYear      = firstLine[-1].strip()
            
            if int(endYear) > maxEndYear :
                maxEndYear = int(endYear)
            if int(startYear) < minStartYear :
                minStartYear = int(startYear)
            
            for line in csvFile :
                meta = line[0].split(',')
                code = meta[iNace]
                country = meta[iGeoTime]
                indic = meta[iIndic]
                if nomenclature == 'nace2' :
                    size = 'TOTAL'
                else :
                    size = meta[iSize]
                
                if code in dicNace and country in dicNation and size == 'TOTAL' :
                    if indic == indicNumerator or indic == indicDenominator :
                        vector = []
                        vector.append(endYear)
                        vector.extend([re.sub('[" ",a-z]','',element) for element in line[1:]])
                        vector.append(startYear)
                        if indic == indicNumerator :
                            dicNumerator = spiLib.defDicIndicator(country,code,vector,dicNumerator)
                        else :
                            dicDenominator = spiLib.defDicIndicator(country,code,vector,dicDenominator)
                            
    dicNumerator = spiLib.reverseAndNormalizeDic(dicNumerator, minStartYear, maxEndYear)
    dicDenominator = spiLib.reverseAndNormalizeDic(dicDenominator, minStartYear, maxEndYear)
    
    dicNumerator = spiLibTotal.calcNaceAggregates(dicNumerator, nomenclature, 'sbs')
    dicDenominator = spiLibTotal.calcNaceAggregates(dicDenominator, nomenclature, 'sbs')
        
    spiLibCreateTable.createTableOverOtherShare(dicNumerator, dicDenominator, minStartYear, 'surpl', nomenclature, 'competition')
    
    
traitementFichierTXT(nomenclature, indicNumerator, indicDenominator, filePaths)
DBConnect.closeDB()     