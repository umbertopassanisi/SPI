import sys
import urllib
import urllib2


#urllib.urlretrieve = AppURLopener()
#prompt_user_passwd={'gomezrv':'$go12rv$'}
#opener = urllib.FancyURLopener(prompt_user_passwd)
#f = opener.open('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz', 'nama_nace06_k.tsv.gz')
values = {'username' : 'gomezrv',
          'password' : '$go12rv$'}
data = urllib.urlencode(values)
#urllib.urlopen('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz',data)
#f=urllib.urlretrieve('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz','nama_nace06_k.tsv.gz',data=data)
#
#f = urllib.urlretrieve('http://appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_p.tsv.gz', 'nama_nace06_p.tsv.gz')
#f=urllib.urlopener
#theurl = 'appsso.eurostat.ec.europa.eu/NavTree_prod/commission/BulkDownloadListing?file=data/nama_nace06_k.tsv.gz'
#username = 'gomezrv'
#password = '$go12rv$'
proxies = {'http': 'http://gomezrv:$go12rv$@158.169.131.13:8012'}
url = "http://download.thinkbroadband.com/10MB.zip"

file_name = url.split('/')[-1]
u = urllib2.urlopen(url,proxies)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()