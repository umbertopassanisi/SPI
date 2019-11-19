#-------------------------------------------------------------------------------------------------
# GENERATION DE LA TABLE infoDB
# -----------------------------
# parametres : argv[]
# sys.argv[0] = nom du programme
# sys.argv[1] = nom du fichier input
# attention : les parametres sont en string, il est parfois necessaire de les convertir en integer
# r@g 19/6/2006
# ajout des nations par defauts dans un fichier input\\nationsDefaut.txt
# r@g 30/4/2010
#-------------------------------------------------------------------------------------------------

import sys
import cx_Oracle
import os
import argparse
from   time     import localtime, strftime
import DBConnect

#gestion des variables, elles seront recues sous options.dest (options.fileinput, options.login ...)

parser = argparse.ArgumentParser()
parser.add_argument("s",help="year_start")
parser.add_argument("e",help="year_end")
parser.add_argument("d",help="domain")
parser.add_argument("-u",help="updating",default='0')
args = parser.parse_args()

cursor 			= 	DBConnect.connection.cursor()

def truncateDbTable():
	# Table Oracle, on ouvre et on vide la table    
	truncateTable		=		"truncate table indicatorsvalue"        
	cursor.execute(truncateTable)
	#return cursor
def updateTableInfo(year_start, year_end, domain, updating):
	last_update     =   strftime("%d/%m/%Y-%H:%M", localtime())    
	user_id         =   os.getenv('USERNAME')
	yearStart       =   year_start        #zone numerique 
	yearEnd         =   year_end          #zone numerique
	domain      	=   domain
	updating      	=   updating
	if	updating 	!= '1':	updating = '0'
	updateTableDC	= "update info  set domain='"+domain+"'\
	,start_year="+yearStart+",end_year="+yearEnd+",updating="+updating+"\
	,userid='"+user_id+"',last_update='"+last_update+"'"
	cursor.execute(updateTableDC)
def closeDbTable():
	DBConnect.connection.commit()
	DBConnect.connection.close()				    
#-------------------------------------------------------------------------------------------------

truncateDbTable()
updateTableInfo(year_start=args.s, year_end=args.e,domain=args.d,updating=args.u)
closeDbTable()