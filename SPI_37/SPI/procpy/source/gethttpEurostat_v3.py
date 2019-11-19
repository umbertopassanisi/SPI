import sys
import urllib.request
inputEurostat           =  sys.argv[1]
dirFile        =  '.\\Input'
fichierLecture =  dirFile + '\\Txt\\'+inputEurostat+'.txt'
try:
	fichier = open(fichierLecture, 'r')
except:
	print ("le fichier ", fichierLecture, " est introuvable")
for	record in fichier:
	fileHttp    = record.strip()
	print (fileHttp)
	#              https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data%2Fprc_hicp_midx.tsv.gz
	urlHttp     = 'http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/'+fileHttp+'.tsv.gz'
	print (urlHttp)
	#targetFile  = dirFile + '\zip\\'+ fileHttp+'.zip' 
	targetFile  = dirFile + '\zip\\'+ fileHttp+'3.zip'
	urllib.request.urlretrieve(urlHttp,targetFile)                                                                           
    