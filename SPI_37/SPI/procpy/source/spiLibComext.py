import DBAccess
import pprint

def convertSingleValueToVector(dicIndicator, startYear, endYear):
    res = []
    dicRes = {}
    for country in dicIndicator:
        for code in dicIndicator[country]:
            for partner in dicIndicator[country][code]:
                res = []
                for i in range(startYear, endYear+1):
                    try:
                        res.append(dicIndicator[country][code][partner][i])
                    except:
                        res.append(':')
                dicIndicator[country][code][partner] = res
    
    return dicIndicator

def mergePartners(dicIndicator):
    res = []
    refIntra = {}
    refExtra = {}
    dicTotal = {}
    
    for country in dicIndicator:
        for code in dicIndicator[country]:
            res = []
            refIntra = {}
            refExtra = {}
            
            try :
                refIntra = dicIndicator[country][code]['EU27_INTRA']
            except: 
                fileLog.write('Missing intra EU27 reference for country ' + country + ' and code ' + code + '.\n')
                continue
            
            try :
                refExtra = dicIndicator[country][code]['EU27_EXTRA']
            except: 
                fileLog.write('Missing extra EU27 reference for country ' + country + ' and code ' + code + '.\n')
                continue
            
            for i in range(0, len(refIntra)):
                if refIntra[i] == ':' :
                    res.append(refExtra[i])
                elif refExtra[i] == ':' :
                    res.append(refIntra[i])
                else:
                    res.append(str((int(refIntra[i]) + int(refExtra[i]))))
            dicIndicator[country][code] = res
            
    return dicIndicator

def removeUselessCpa(dicIndicator, cpaList):
    codeList = []
    for country in dicIndicator:
        for code in dicIndicator[country]:
            if code not in cpaList:
                codeList.append(code)
    
    for country in dicIndicator:
        for code in codeList:
            try:
                del dicIndicator[country][code]
            except:
                pass
            
    return dicIndicator

def formatBecEurostatDic(dicIndicator):
    becDic = DBAccess.buildBecCorrespondance()
    for country in dicIndicator:
        for code in becDic:
            if code != becDic[code]:
                dicIndicator[country][becDic[code]] = dicIndicator[country][code]
                del dicIndicator[country][code]
    
    return dicIndicator