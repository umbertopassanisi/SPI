import sys
import urllib
import urllib2

HTTP_PROXIES = {'http': 'http://158.169.131.13:8012/'}
HTTP_LOGIN = 'gomezrv'
HTTP_PASSWORD = '$go12rv$'
realm = 'PROXY_INTERNET'
#class UrlOpener(urllib.FancyURLopener):
class UrlOpener(urllib.FancyURLopener):
    def __init__(self, *args):
        urllib.FancyURLopener.__init__(self, *args)

    def prompt_user_passwd(self, host, realm):    
        return ('gomezrv', '$go12rv$')
          
#http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?sort=1&file=table_of_contents_fr.pdf  
#http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?sort=1&file=data%2Fnama_nace06_k.tsv.gz         
proxies = {'http': 'http://158.169.131.13:8012/'}
opener = UrlOpener(proxies)
try:
  f=opener.retrieve('http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?sort=1&file=data%2Fnama_nace06_c.tsv.gz', 'nama_nace06_c.zip')
except IOError:
  print f  
#x=opener.geturl()


#print f
#x=opener('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.dft.gz')
