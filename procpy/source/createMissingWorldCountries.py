import sys
from DBConnect import connection
from pprint import pprint

filePath = sys.argv[1]
nomenclature = sys.argv[2].upper()

file = open(filePath, 'r')
cursor = connection.cursor()

for line in file :
    if('no value for country, cpa, year :' in line):
        key = line[-11:].strip()
        key = key.split(',')  
        cursor.execute("insert into info_world(year, country, code, source, nomenclature) values(" + key[2] + ", '" + key[0] + "', '" + key[1] + "', 'UN', '" + nomenclature + "')")

file.close()
connection.commit()
connection.close()
