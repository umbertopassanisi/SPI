import sys
import os
import glob
import urllib2
import FileAccess
import checkXmlAccess
import fileManagement
import time
from datetime import datetime
from pprint import pprint

G_path = sys.argv[1]
G_startYear = sys.argv[2]
G_endYear = sys.argv[3]

proxy_url = "http://gomezrv:$go12rv$@147.67.138.13:8012"
proxy_urls = "http://gomezrv:$go12rv$@158.169.131.13:8012"
proxy_support = urllib2.ProxyHandler({'https': proxy_urls})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

try :
    G_nomenclature = sys.argv[4]
except :
    G_nomenclature = ''

def getFiles(path, nomenclature, startYear, endYear, countryList):
    if nomenclature != '':
        filePath = path + '\\input\\xml\\' + nomenclature 
    else:
        filePath = path + '\\input\\xml' 
            
    nbrYear    =    int(endYear)-int(startYear)+1
    code='K9tEO6K2x1gJoFnXR/qcd8gwzQgyXpkLcugnAN4Wj45g2jtfyj/9S6GqzH+KozrFerR4R4igrn717EjaBxQkgJKQts61M1U+dVxcdkRPZzGxClkhvNSLyxdp5OoXJ256L6xAvOpc/jJnvP0ZzLfeDsSN8CeXx+pvnTYCJbCbU/Y='
    if nomenclature == 'bec' :
        cc = 'all'
        px = 'BE'
    else :
        cc = '??????'
        px = 'H0'
    y = ''
    p = '0'
    rg = '2'
    comp = 'false'
    year = int(startYear)
    for i in range(0,nbrYear):        
        y = y+str(year)+','
        year = year + 1
    for codeNationISO2 in countryList:
        print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Getting XML file for country ' + codeNationISO2)
        codeNationUN = countryList[codeNationISO2]
        try :
            urlHttp = 'https://comtrade.un.org/ws/get.aspx?cc='+cc+'&px='+px+'&r='+codeNationUN+'&p='+p+'&rg='+rg+'&comp='+comp+'&code='+code
            targetFile = filePath + '\\' + codeNationISO2 + '.xml'
            src = urllib2.urlopen(urlHttp)
            csv = file(targetFile,'w')
            csv.write(src.read())
            csv.close()
        except:
            print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Error getting XML file for country ' + codeNationISO2 + ' - Removing the last file created - Now waiting 60sec')
            fileManagement.removeLastFileBasedOnExt(filePath, 'xml')
            time.sleep(60)     

def getCountryList(path, nomenclature):
    dirTXT = path + '\\Input\\txt'
    countryList = FileAccess.lectureNationUNInverse(dirTXT)
    
    if nomenclature == 'bec':
        XMLFiles = glob.glob(path + '\\Input\\xml\\bec\\*.xml')
    else:
        XMLFiles = glob.glob(path + '\\Input\\xml\\*.xml')
    
    nationCheckList = []
    
    for XMLFile in XMLFiles :
        base = os.path.basename(XMLFile)
        del(countryList[base.split('.')[0]])
    
    return countryList

def checkFiles(path, nomenclature, countryList):
    
    if nomenclature == 'bec':
        XMLPath = path + '\\Input\\xml\\bec\\'
    else:
        XMLPath = path + '\\Input\\xml\\'
        
    for country in countryList:
        file = XMLPath + country + '.xml'
                
        if not checkXmlAccess.simpleCheckXML(file):
            try :
                print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Removing the following file : ' + file)
                os.remove(file)
            except :
                pass

def main(path, nomenclature, startYear, endYear):
    origStdout = sys.stdout
    origStderr = sys.stderr
    logFile = file(path + '\\log\\getInputUN' + nomenclature + '.log', 'w')
    errorLogFile = file(path + '\\log\\getInputUN' + nomenclature + '_error.log', 'w')
    sys.stdout = logFile
    sys.stderr = errorLogFile
    
    print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Starting')
    
    if nomenclature == 'bec':
        XMLPath = path + '\\Input\\xml\\bec\\'
    else:
        XMLPath = path + '\\Input\\xml\\'
    
    print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Cleaning the old folder')   
    fileManagement.cleanFilesBasedOnExt(XMLPath + '\\old', 'xml')
    print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Moving old files to the old folder')    
    fileManagement.moveFilesBasedOnExt(XMLPath, XMLPath + '\\old', 'xml')
    
    countryList = getCountryList(path, nomenclature)
    cpt = 0
    
    while countryList and cpt < 5 :
        getFiles(path, nomenclature, startYear, endYear, countryList)
        checkFiles(path, nomenclature, countryList)
        countryList = getCountryList(path, nomenclature)
        cpt += 1
    
    if cpt >= 5 :
        print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Procedure interrupted due to an excess of attempts to get the files. Removing the downloaded files...')
        
        XMLFolderPath = path + '\\input\\xml'
        
        if nomenclature != '':
            XMLFolderPath += '\\' + nomenclature
            
        fileManagement.cleanFolderFromFilesBasedOnExt(XMLFolderPath, 'xml')
        
        print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Moving old files from the old folder to the base folder')
        fileManagement.moveFilesBasedOnExt(XMLPath + '\\old', XMLPath, 'xml')
        
    print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Ending')
    
    sys.stdout = origStdout
    sys.stderr = origStderr
    logFile.close()
    errorLogFile.close()

main(G_path, G_nomenclature, G_startYear, G_endYear)