import sys
import httplib
import urllib
import urllib2
import fileDownloader

values = {'username' : 'gomezrv',
          'password' : '$go12rv$'}
data = urllib.urlencode(values)

#downloader = fileDownloader.DownloadFile('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_p.tsv.gz', "C:\Users\gomezrv\Downloads\nama_nace06_p.tsv.gz",('gomezrv','$go12rv$'))
#downloader.download()

httplib.HTTPConnection.debuglevel = 1

#auth_handler = urllib2.HTTPBasicAuthHandler()
#auth_handler.add_password(realm=None,
#                          uri='https://mahler:8092/site-updates.py',
#                          user='klem',
#                          passwd='kadidd!ehopper')
#opener = urllib2.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
#proxies = {'http': 'http://158.169.131.13:8012/'}


#proxy_handler = urllib2.ProxyHandler({'http': 'http://158.169.131.13:8012/'})
#proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
#proxy_auth_handler.add_password(None, 'http://158.169.131.13:8012/', 'gomezrv', '$go12rv$')

#opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
# This time, rather than install the OpenerDirector, we use it directly:
#opener.open('http://158.169.131.13:8012/')

#urllib2.install_opener(opener)
#urllib2.urlopen('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_p.tsv.gz')

url = 'epp.eurostat.ec.europa.eu'
username = 'gomezrv'
password = '$go12rv$'
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
# None, with the "WithDefaultRealm" password manager means
# that the user/pass will be used for any realm (where
# there isn't a more specific match).
#password_mgr.add_password(None, url, username, password)
#auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
#opener = urllib2.build_opener(auth_handler)
#urllib2.install_opener(opener)
#print urllib2.urlopen("http://www.example.com/folder/page.html")

proxy = urllib2.ProxyHandler({'http': 'http://gomezrv:$go12rv$@158.169.131.13:8012'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

conn = urllib2.urlopen('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_p.tsv.gz')
x=conn.geturl()
print   x

#---------------------------------------------------------
#request = urllib2.Request('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_p.tsv.gz')
#opener = urllib2.build_opener()
#feeddata = opener.open(request).read()