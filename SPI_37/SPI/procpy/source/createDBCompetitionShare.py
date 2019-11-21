import sys
from pprint import pprint

import DBConnect
import DBAccess
import spiLib
import spiLibCreateTable

nomenclature = sys.argv[1]
indicator = sys.argv[2]
path = sys.argv[3]

if indicator == 'firmbempsh' :
    indicNumerator = 'firmbemp'
    indicDenominator = 'firmactemp'
elif indicator == 'firmdempsh':
    indicNumerator = 'firmdemp'
    indicDenominator = 'firmactemp'
elif indicator == 'birth':
    indicNumerator = 'firmb'
    indicDenominator = 'firmact'
elif indicator == 'death':
    indicNumerator = 'firmd'
    indicDenominator = 'firmact'
    
def traitementFichierTXT(nomenclature, indicator, indicNumerator, indicDenominator):
    numerator = DBAccess.lectureNaceIndicatorData(indicNumerator, nomenclature, 'competition')
    denominator = DBAccess.lectureNaceIndicatorData(indicDenominator, nomenclature, 'competition')
    dicNumerator = numerator[0]
    startNumerator = numerator[1]
    dicDenominator = denominator[0]
    startDenominator = denominator[1]
    
    if startNumerator > startDenominator :
        startDefinitive = startNumerator
    else :
        startDefinitive = startDenominator 
    
    refVec = dicNumerator  
    while type(refVec) is not list:
        refVec = refVec[list(refVec.keys())[0]]
    
    endNumerator = startNumerator + len(refVec) - 1
    
    refVec = dicDenominator
    while type(refVec) is not list:
        refVec = refVec[list(refVec.keys())[0]]
    
    endDenominator = startDenominator + len(refVec) - 1
    
    if endDenominator > endNumerator :
        endDefinitive = endNumerator
    else :
        endDefinitive = endDenominator
        
    dicNumerator = spiLib.normalizeDicSize(dicNumerator, startNumerator, startDefinitive, endDefinitive)
    dicDenominator = spiLib.normalizeDicSize(dicDenominator, startDenominator, startDefinitive, endDefinitive)
    
    spiLibCreateTable.createTableOverOtherShare(dicNumerator, dicDenominator, startDefinitive, indicator, nomenclature, 'competition')
        

traitementFichierTXT(nomenclature, indicator, indicNumerator, indicDenominator)
DBConnect.closeDB()     
