import sys

import urllib
class AppURLopener(urllib.FancyURLopener):
    retrieve = ('http://livedocs.adobe.com/blazeds/1/blazeds_devguide/blazeds_devguide.pdf', 'blazeds_devguide.pdf')

urllib._urlopener = AppURLopener()

#proxies = {'http': 'http://158.169.131.13:8012'}
#filehandle = urllib.urlopen('http://livedocs.adobe.com/flex/3/html/index.html', proxies=proxies)
#file=urllib.urlretrieve('http://livedocs.adobe.com/flex/3/html/index.html', 'test.html')


proxies = {'http': 'http://158.169.131.13:8012/'}
opener = urllib.FancyURLopener(proxies)
#opener = urllib._urlopener(proxies)
#f = opener.open("http://livedocs.adobe.com")
#f.read()
for file in urllib._urlopener:
		print file

