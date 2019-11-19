import sys
import urllib
import urllib2
#req = urllib2.Request('http://comtrade.un.org/db/dqBasicQueryResultsd.aspx?action=dcsv&cc=????&px=H3&r=56&y=2012&p=0&rg=2&so=9999&rpage=dqBasicQuery&qt=n')
#req.add_header('Referer', 'http://comtrade.un.org/db/')
#con = urllib2.urlopen('http://comtrade.un.org/db/default.aspx')
con = urllib2.urlopen('http://www.python.org/')
print con.read(100)
#con.add_header('Referer', 'http://comtrade.un.org/db/default.aspx')
#con = urllib2.urlopen('http://comtrade.un.org/db/dqBasicQueryResultsd.aspx?action=dcsv&cc=????&px=H3&r=56&y=2012&p=0&rg=2&so=9999&rpage=dqBasicQuery&qt=n')
#con.add_header('Referer', 'http://comtrade.un.org/db/default.aspx')
#x=con.geturl()
#print   x

#urlHttp     = 'http://comtrade.un.org/db/dqBasicQueryResultsd.aspx?referer=comtrade.un.org&action=dcsv&cc=????&px=H3&r=56&y=2012&p=0&rg=2&so=9999&rpage=dqBasicQuery&qt=n'
#targetFile  = 'comtrade_trade_data_BE_4d_2012.csv'    
#urllib.urlretrieve(urlHttp,targetFile) 

proxy_url = "http://gomezrv:$go12rv$@147.67.138.13:8012"
proxy_support = urllib2.ProxyHandler({'http': proxy_url})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)
urlHttp     = 'http://comtrade.un.org/ws/get.aspx?cc=all&px=BE&r=458&p=0&rg=2&comp=false&code=K9tEO6K2x1gJoFnXR/qcd8gwzQgyXpkLcugnAN4Wj45g2jtfyj/9S6GqzH+KozrFerR4R4igrn717EjaBxQkgJKQts61M1U+dVxcdkRPZzGxClkhvNSLyxdp5OoXJ256L6xAvOpc/jJnvP0ZzLfeDsSN8CeXx+pvnTYCJbCbU/Y='
src = urllib2.urlopen(urlHttp)
                                                                       
    