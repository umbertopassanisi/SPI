import sys
import urllib
import urllib2


#class AppURLopener(urllib.FancyURLopener):    retrieve = ('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz', 'nama_nace06_k.tsv.gz')

#urllib.urlretrieve = AppURLopener()
#prompt_user_passwd={'gomezrv':'$go12rv$'}
#opener = urllib.FancyURLopener(prompt_user_passwd)
#f = opener.open('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz', 'nama_nace06_k.tsv.gz')

#f = urllib.urlretrieve('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz', 'nama_nace06_k.tsv.gz')
#f=urllib.urlopener
#theurl = 'appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz'
username = 'gomezrv'
password = '$go12rv$'

#passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
# this creates a password manager
#passman.add_password(None, theurl, username, password)
# because we have put None at the start it will always
# use this username/password combination for  urls
# for which `theurl` is a super-url

#authhandler = urllib2.HTTPBasicAuthHandler(passman)
# create the AuthHandler

#opener = urllib2.build_opener(authhandler)

#urllib2.install_opener(opener)
# All calls to urllib2.urlopen will now use our handler
# Make sure not to include the protocol in with the URL, or
# HTTPPasswordMgrWithDefaultRealm will be very confused.
# You must (of course) use it when fetching the page though.

#pagehandle = urllib2.urlopen(theurl)
#f = urllib.urlretrieve('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz', 'nama_nace06_k.tsv.gz')
# authentication is now handled automatically for us

#----------------------------------------------------------------------------
top_level_url = "appsso.eurostat.ec.europa.eu"

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
# creer un password manager

password_mgr.add_password(None,top_level_url, username, password)
# ajoute le username et password
# si on connaissait le domaine, on pourrait l'utiliser au lieu de ``None``
proxy = urllib2.ProxyHandler({'http': 'http://gomezrv:$go12rv$@158.169.131.13:8012'})
auth = urllib2.HTTPBasicAuthHandler(password_mgr)

opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
myopen=urllib2.install_opener(opener)

#handler = urllib2.HTTPBasicAuthHandler(password_mgr)
# creer le handler

#opener = urllib2.build_opener(handler)
# du handler vers  l'opener

#opener.open('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz')
# utilise l'opener pour ramener un URL

#pagehandle = urllib2.urlopen('http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=Bulkdownload_Guidelines.pdf').info()
pagehandle = opener.open('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz')
#req = urllib2.Request('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz')
#req = urllib2.Request('http://epp.eurostat.ec.europa.eu/NavTree_prod/everybody/BulkDownloadListing?file=Bulkdownload_Guidelines.pdf')
#f=urllib2.FileHandler()
print pagehandle

#response = urllib2.urlopen(req).info()
#print response


#f.file_open(req)
#f=urllib2.FileHandler.file_open('appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz', 'nama_nace06_k.tsv.gz')
# installe l'opener
# maintenant tous les appels a urllib2.urlopen vont utiliser notre opener