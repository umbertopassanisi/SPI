import sys
import urllib2
nace           =  sys.argv[1]
Path 	=  sys.argv[2]

dirFile        =  Path + '\Input'
fichierLecture =  dirFile + '\\Txt\\eurostatFileInput'+nace+'.txt'
#fichierLecture = 'eurostatFileInput.txt'

proxy_url = "http://gomezrv:$go12rv$@147.67.138.13:8012"
proxy_urls = "http://gomezrv:$go12rv$@158.169.131.13:8012"
proxy_support = urllib2.ProxyHandler({'https': proxy_urls})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

try:
	fichier = open(fichierLecture, 'r')
except:
	print "le fichier ", fichierLecture, " est introuvable"
for	record in fichier:
	fileHttp    = record.strip()
	print fileHttp
	#urlHttp     = 'http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=data/'+fileHttp+'.tsv.gz'
	urlHttp     = 'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/'+fileHttp+'.tsv.gz'
	targetFile  = dirFile + '\zip\\'+nace+'\\' + fileHttp+'.zip' 
	#traite erreur : try, except et ecriture dans logfile
	src = urllib2.urlopen(urlHttp)
	csv = file(targetFile,'wb')
	csv.write(src.read())
	csv.close()