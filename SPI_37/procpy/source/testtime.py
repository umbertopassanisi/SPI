#-------------------------------------------------------------------------------------------------
# CHECK TABLE : on test la valeur de chaque meme table entre deux schema Oracle 
# par exemple entre TEST et PROD
# -----------------------------
# parametres : argv[]
# sys.argv[0] = nom du programme
# sys.argv[1] = nom du fichier input
# t (table) = nom d'une table oracle existante
# s1,s2(schema) = DEV, TEST ou PROD uniquement
# attention : les parametres sont en string, il est parfois necessaire de les convertir en integer
# r@g 19/6/2006
#-------------------------------------------------------------------------------------------------

import sys
import time



#gestion des variables, elles seront recues sous options.dest (options.fileinput, options.login ...)


def selectTime():
	td =	time.time()
	print 'time.gmtime()',time.gmtime(td)
	print 'time.localtime()', time.localtime()
	print 'time.asctime()',time.asctime() 
	print 'time.ctime()', time.ctime(td)

	print 'time.gmtime()',time.gmtime()
	print 'time.time()', time.time()
	tf =	time.time()
	print 'time.gmtime()',time.gmtime(tf)
	tdiff = 	tf-td
	print 'tdiff', tdiff
	print 'time.gmtime()',time.ctime(tdiff)
 
#-------------------------------------------------------------------------------------------------

selectTime()
