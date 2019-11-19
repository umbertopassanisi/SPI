import sys
import os
import urllib2
import glob
import FileAccess
import time

Path 			=  sys.argv[1]
G_startYear 	=  sys.argv[2]
G_endYear 		=  sys.argv[3]

#proxy : http://autoproxy.cec.eu.int/proxy.pac

proxy_url = "http://gomezrv:$go12rv$@147.67.138.13:8012" #proxy BXL
proxy_urls = "http://gomezrv:$go12rv$@147.67.117.13:8012" #proxy LUX
proxy_support = urllib2.ProxyHandler({'https': proxy_urls})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Input\\txt'
fichiersXML     =  glob.glob(dirUse +'\\Input\\xml\\bec\\*.xml')
dirFile        	=  dirUse			+'\\Input'

#http://comtrade.un.org/ws/get.aspx?cc=??&px=BE&r=36&y=2000,2006&p=0&rg=2&comp=false&code=K9tEO6K2x1gJoFnXR/qcd8gwzQgyXpkLcugnAN4Wj45g2jtfyj/9S6GqzH+KozrFerR4R4igrn717EjaBxQkgJKQts61M1U+dVxcdkRPZzGxClkhvNSLyxdp5OoXJ256L6xAvOpc/jJnvP0ZzLfeDsSN8CeXx+pvnTYCJbCbU/Y=

def getFileUN(startYear,endYear):
	nbrYear	=	int(endYear)-int(startYear)+1
	code='K9tEO6K2x1gJoFnXR/qcd8gwzQgyXpkLcugnAN4Wj45g2jtfyj/9S6GqzH+KozrFerR4R4igrn717EjaBxQkgJKQts61M1U+dVxcdkRPZzGxClkhvNSLyxdp5OoXJ256L6xAvOpc/jJnvP0ZzLfeDsSN8CeXx+pvnTYCJbCbU/Y='
	cc		='all'
	px		='BE'
	y		=''
	p		='0'
	rg		='2'
	comp	='false'
	year 	= int(startYear)
	dicNationTraite		= {}
	dicNation			= {}	
	dicNation			= FileAccess.lectureNationUN(dirTXT)	
	for i in range(0,nbrYear):
		y		= y+str(year)+','
		year	= year + 1
	for fichierXml in fichiersXML:
		lstfichierXml	=	fichierXml.split('.')
		base			=	os.path.basename(fichierXml)
		country			=	os.path.splitext(base)[0]
		dicNationTraite[country]=country
	for	codeNationUN in dicNation:
		codeNationISO2  = 	dicNation[codeNationUN]
		try:
			dicNationTraite[codeNationISO2]
		except:
			r			= codeNationUN
			urlHttp     = 'https://comtrade.un.org/ws/get.aspx?cc='+cc+'&px='+px+'&r='+r+'&p='+p+'&rg='+rg+'&comp='+comp+'&code='+code
			print urlHttp
			targetFile  = dirFile + '\\xml\\bec\\'+codeNationISO2+'.xml' 
			print targetFile
			try:
				src = urllib2.urlopen(url=urlHttp,timeout=120)
				csv = open(targetFile,'w')
				csv.write(src.read())
				csv.close()
			except Exception as errrr:
				print errrr
				print (targetFile, ' not created')

getFileUN(G_startYear,G_endYear)
