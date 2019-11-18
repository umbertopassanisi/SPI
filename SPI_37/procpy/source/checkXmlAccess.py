from   lxml import etree
from   lxml import objectify
from datetime import datetime
#from   time import localtime, strftime

#lecture fichier XML
def lectureXML(fileXML,fileLog):
    fichierXml        = fileXML
    try:
        treeXml            = objectify.parse(fichierXml)
        fileLog.write('ok xml file : '+fichierXml+'\n')
    except:
        fileLog.write('--------------problem xml file----------- : '+fichierXml+' CANNOT READ\n')
        print 'problem xml file :', fichierXml, ' not read'
        return
    rootXml            = treeXml.getroot()
    #lecture du fichier XML
    for record in rootXml.iterchildren(tag='r'):
        try:
            yr             = record.yr.text.strip()
        except:
            fileLog.write('pas de tag yr dans le fichier : '+fichierXml+'\n')
            continue
        try:
            rgCode         = record.rgCode.text.strip() #2=export
        except:
            fileLog.write('pas de tag rgCode dans le  fichier : '+fichierXml+'\n')
            continue
        try:
            rtCode         = record.rtCode.text.strip()
        except:
            fileLog.write('pas de tag rtCode dans le  fichier : '+fichierXml+'\n')
            continue
        try:
            ptCode         = record.ptCode.text.strip()
        except:
            fileLog.write('pas de tag ptCode dans le  fichier : '+fichierXml+'\n')
            continue            
        try:
            cmdCode     = record.cmdCode.text.strip()
        except:
            fileLog.write('pas de tag cmdCode dans le  fichier : '+fichierXml+'\n')
            continue        
        try:
            TradeValueTxt    = record.TradeValue.text.strip()
            TradeValueFloat    = float(TradeValueTxt)
        except:
            fileLog.write('pas de tag TradeValue dans le  fichier : '+fichierXml+'\n')
            continue            
    return 

def simpleCheckXML(file):
    try:
        treeXml = objectify.parse(file)
    except:
        print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'The following file is corrupted : ' + file)
        return False
        
    rootXml = treeXml.getroot()
    
    for record in rootXml.iterchildren(tag='r'):
        try:
            yr             = record.yr.text.strip()
            rgCode         = record.rgCode.text.strip() #2=export
            rtCode         = record.rtCode.text.strip()
            ptCode         = record.ptCode.text.strip()
            cmdCode     = record.cmdCode.text.strip()
            TradeValueTxt    = record.TradeValue.text.strip()
            TradeValueFloat    = float(TradeValueTxt)
        except:
            print(datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S') + '\t' + 'Encountered an unexpected structure in the following file : ' + file)
            return False
    
    return True