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
import spiLibComext

G_spiIndicator = sys.argv[1]
#parametre NACE1 ou NACE2
G_nomenclature = sys.argv[2].lower()
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
G_path = sys.argv[3]

G_startYear = 1900 # annee de debut minimum par defaut pour tous les vecteurs
G_tableName = 'external'

if G_spiIndicator == 'xsh': #1 pour import et 2 pour export dans la notation comext
    G_eurostatIndicator = '2'
elif G_spiIndicator == 'msh':
    G_eurostatIndicator = '1'
else :
    sys.exit()
    
dirUse = G_path
dirLog = dirUse + '\\Log'
fichierTXTLabel = dirUse + '\\Input\\tsv\\' + G_nomenclature + '\\label.tsv'
fichierTXTData = dirUse + '\\Input\\tsv\\' + G_nomenclature + '\\data.tsv'
fileLog = open(dirLog + '\\createDBExternalShare' + G_nomenclature + G_spiIndicator + '.log', 'w')

def traitementFichierTxt(spiIndicator, eurostatIndicator, nomenclature, fileData, fileLabel, tableName, fileLog):
    listNation = DBAccess.defListNationIso2()
    if nomenclature == 'bec':
        listCpa = DBAccess.lectureBecEurostat()
    else:
        listCpa = DBAccess.lectureCpaSimple(nomenclature)
    uselessNation = {}
    uselessCpa = {}
    dicIndicator = {}
    
    file = open(fileData, 'r')
    line1st = file.readline()
    list1st = line1st.split('\t')
    dicComext = spiLib.defDicComext(list1st)
    iReporter = dicComext['reporter']
    iPartner  = dicComext['partner']
    iProduct  = dicComext['product']
    iFlow     = dicComext['flow']
    iPeriod   = dicComext['period']
    iValue    = dicComext['value']

    minYear = 999999
    maxYear = 0
        
    for line in file :
        list = line.split('\t')
        reporter = list[iReporter].strip()
        partner  = list[iPartner].strip().strip('"')
        product  = list[iProduct].strip()
        if product[0] == '0' :
            product = product[1:]
        flow     = list[iFlow].strip()
        period   = int(list[iPeriod].strip()[0:4])
        value    = list[iValue].strip()
        
        if reporter in listNation:
            if product in listCpa:
                if flow == eurostatIndicator:
                    try:
                        dicIndicator[reporter][product][partner][period] = value
                    except:
                        try:
                            dicIndicator[reporter][product][partner] = {}
                            dicIndicator[reporter][product][partner][period] = value
                        except:
                            try:
                                dicIndicator[reporter][product] = {}
                                dicIndicator[reporter][product][partner] = {}
                                dicIndicator[reporter][product][partner][period] = value
                            except:
                                dicIndicator[reporter] = {}
                                dicIndicator[reporter][product] = {}
                                dicIndicator[reporter][product][partner] = {}
                                dicIndicator[reporter][product][partner][period] = value
                    if period > maxYear:
                        maxYear = period
                    if period < minYear:
                        minYear = period      
            else:
                uselessCpa[product] = product
        else:
            uselessNation[reporter] = reporter
    
    file.close()
    
    spiLib.defnoCountry(uselessNation,fileLog)
    del uselessNation
    spiLib.defUselessCode(uselessCpa, fileLog)
    del uselessCpa
    
    dicIndicator = spiLibComext.convertSingleValueToVector(dicIndicator, minYear, maxYear)
    dicIndicator = spiLibComext.mergePartners(dicIndicator)
    if nomenclature == 'bec':
        dicIndicator = spiLibComext.formatBecEurostatDic(dicIndicator)
    dicIndicator = spiLibTotal.calcNaceAggregates(dicIndicator, nomenclature, 'manufacturing')
    
    
    dicIndicator = spiLibTotal.calcNaceAggregates(dicIndicator, nomenclature, 'comext')
    
    spiLibCreateTable.createTableExternalXMShare(spiIndicator, nomenclature, minYear, dicIndicator, tableName, fileLog)
    
traitementFichierTxt(G_spiIndicator, G_eurostatIndicator, G_nomenclature, fichierTXTData, fichierTXTLabel, G_tableName, fileLog)
fileLog.close()
DBConnect.closeDB()