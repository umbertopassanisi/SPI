import sys
import urllib2
import cx_Oracle
from bs4 import BeautifulSoup
from DBConnect import connection
from pprint import pprint

response = urllib2.urlopen('http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?dir=data&sort=1&sort=2&start=all')
html = response.read()
soup = BeautifulSoup(html)

cursor = connection.cursor()
fileList = []

try:
    cursor.execute("select id_file from files")
    
    for rec in cursor.fetchall() :
        fileList.append(rec[0])        
except:
    print('Error on file name selection')
    connection.close()
    sys.exit()

for line in soup.find_all('tr'):
    cell = line.find_all('td')
    try:
        curFile = cell[0].a.get_text()[0:-7]
    except:
        continue
    
    if curFile in fileList :
        try :
            cursor.execute("update files set available_update=to_date('" + cell[3].get_text()[2:] + "', 'DD/MM/YYYY HH24:MI:SS') where id_file='" + cell[0].a.get_text()[0:-7] + "'")
        except :
            print("Error executing update query.")

connection.commit()
connection.close()


