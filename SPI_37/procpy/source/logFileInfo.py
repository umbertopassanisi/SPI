import sys
import os
import time
import glob
from DBConnect import connection
import pprint

G_path = sys.argv[1]

files = glob.glob(G_path + '/input/tsv/nace1/*.tsv')

cursor = connection.cursor()

try :
    cursor.execute("delete from files")
    connection.commit()
except :
    print('Error on delete')

for file in files :
    try :
        cursor.execute("insert into files(id_file, last_update, nomenclature) values('" + os.path.splitext(os.path.basename(file))[0] + "', to_date('" + time.strftime('%d-%m-%Y', time.gmtime(os.path.getmtime(file))) + "', 'DD-MM-YYYY'), 'NACE1')")
    except :
        print('Error on NACE1 insert')
    
files = glob.glob(G_path + '/input/tsv/nace2/*.tsv')

for file in files :
    try :
        cursor.execute("insert into files(id_file, last_update, nomenclature) values('" + os.path.splitext(os.path.basename(file))[0] + "', to_date('" + time.strftime('%d-%m-%Y', time.gmtime(os.path.getmtime(file))) + "', 'DD-MM-YYYY'), 'NACE2')")
    except :
        print('Error on NACE2 insert')

files = glob.glob(G_path + '/input/tsv/nonace/*.tsv')

for file in files :
    try :
        cursor.execute("insert into files(id_file, last_update) values('" + os.path.splitext(os.path.basename(file))[0] + "', to_date('" + time.strftime('%d-%m-%Y', time.gmtime(os.path.getmtime(file))) + "', 'DD-MM-YYYY'))")
    except :
        print('Error on nonace insert')

connection.commit()
connection.close()