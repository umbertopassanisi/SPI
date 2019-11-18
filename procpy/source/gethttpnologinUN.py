import sys
import urllib
dirFile        =  '.\Input'
fichierLecture =  dirFile + '\Txt\eurostatFileInput.txt'
#fichierLecture = 'eurostatFileInput.txt'
try:
    fichier = open(fichierLecture, 'r')
except:
    print "le fichier ", fichierLecture, " est introuvable"
for	record in fichier:
    fileHttp    = record.split(';')[0]
    print fileHttp
    urlHttp     = 'http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=data/'+fileHttp+'.tsv.gz'
    targetFile  = dirFile + '\zip\\' + fileHttp+'.zip'    
    urllib.urlretrieve(urlHttp,targetFile)                                                                           
    