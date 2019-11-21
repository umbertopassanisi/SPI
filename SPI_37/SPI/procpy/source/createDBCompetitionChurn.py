import sys
from pprint import pprint

import DBConnect
import DBAccess
import spiLib
import spiLibCreateTable

nomenclature = sys.argv[1]
path = sys.argv[2]

def traitementFichierTXT(nomenclature):
    numeratorA = DBAccess.lectureNaceIndicatorData('firmb', nomenclature, 'competition')
    numeratorB = DBAccess.lectureNaceIndicatorData('firmd', nomenclature, 'competition')
    denominator = DBAccess.lectureNaceIndicatorData('firmact', nomenclature, 'competition')
    dicNumeratorA = numeratorA[0]
    startNumeratorA = numeratorA[1]
    dicNumeratorB = numeratorB[0]
    startNumeratorB = numeratorB[1]
    dicDenominator = denominator[0]
    startDenominator = denominator[1]
    
    if startNumeratorA > startNumeratorB :
        startDefinitive = startNumeratorA
    else :
        startDefinitive = startNumeratorB
        
    if startDenominator > startDefinitive :
        startDefinitive = startDenominator
        
    refVec = dicNumeratorA
    while type(refVec) is not list:
        refVec = refVec[list(refVec.keys())[0]]
    
    endDefinitive = startNumeratorA + len(refVec) - 1
    
    refVec = dicNumeratorB
    while type(refVec) is not list:
        refVec = refVec[list(refVec.keys())[0]]
    
    endNumeratorB = startNumeratorB + len(refVec) - 1
    
    if endNumeratorB < endDefinitive :
        endDefinitive = endNumeratorB
    
    refVec = dicDenominator
    while type(refVec) is not list:
        refVec = refVec[list(refVec.keys())[0]]
    
    endDenominator = startDenominator + len(refVec) - 1
    
    if endDenominator < endDefinitive :
        endDefinitive = endDenominator
    
    dicNumeratorA = spiLib.normalizeDicSize(dicNumeratorA, startNumeratorA, startDefinitive, endDefinitive)
    dicNumeratorB = spiLib.normalizeDicSize(dicNumeratorB, startNumeratorB, startDefinitive, endDefinitive)
    dicDenominator = spiLib.normalizeDicSize(dicDenominator, startDenominator, startDefinitive, endDefinitive) 
    
    dicNumerator = {}

    for country, countryData in list(dicNumeratorA.items()):
        dicNumerator[country] = {}
        
        for code in countryData :
            dicNumerator[country][code] = []
            
            try :
                vectorA = dicNumeratorA[country][code]
                vectorB = dicNumeratorB[country][code]
            except KeyError :
                continue
            
            for i, item in enumerate(vectorA) :
                try :
                    dicNumerator[country][code].append(str(float(vectorA[i]) + float(vectorB[i])))
                except ValueError :
                    dicNumerator[country][code].append(':')
                  
    spiLibCreateTable.createTableOverOtherShare(dicNumerator, dicDenominator, startDefinitive, 'churn', nomenclature, 'competition')
        

traitementFichierTXT(nomenclature)
DBConnect.closeDB()  