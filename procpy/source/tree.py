#-------------------------------------------------------------------------------------------------
# GENERATION DE LA TABLE ARBRE Nouvelle version 2.0 pour addin vers Oracle
# ------------------------------------------------------------------------
# parametres : argv[]
# sys.argv[0] = nom du programme
# sys.argv[1] = nom du fichier input
# attention : les parametres sont en string, il est parfois necessaire de les convertir en integer
# r@g 10/12/2010
#-------------------------------------------------------------------------------------------------

import sys
import ameco
import cx_Oracle
from   optparse import OptionParser
import connectDB
#gestion des variables, elles seront recues sous options.dest (options.fileinput, options.login ...)

usage   = "usage: %prog [options] arg1 arg2"
parser  = OptionParser(usage=usage)
parser.add_option("-i", "--fileinput", 	type="string", dest="fileinput", 	help="input filename")
(options, args) = parser.parse_args()

# variables globales recues en parametre
fichier = sys.argv[1]

#connection DB  DataCenter
cursorDC 	 = 	connectDB.connection.cursor()
                 
def creeArbre(fichiersource):
    truncateTable		=		"truncate table arbre"
    cursorDC.execute(truncateTable)#DataCenter   
    nbrSerie = 0
    nbrOrdre = 0
    chapitre = 0
    nbrChapitre = 0
    nbrSous_chapitre = 0
    serie = []
    record={}    
    for  rec in fichiersource: 		    		         
         rec  = rec.strip('"')
         lgn  = rec.split()		    		         
         cle  = lgn[0].strip()                 # attention le fichier excel exporte des " qu'il faut eliminer
         cle  = cle.strip('"').strip()
         nom  = rec[len(cle):].strip()         # enleve les espaces au debut et a la fin de la chaine
         nom  = nom.strip('"').strip()         # attention le fichier excel exporte des " qu'il faut eliminer 
         ligneArbre = ''  
         if   cle == 'CH':
              #----- on traite le chapitre ---------------------------#              
              # la cle est composee du code chapitre                  #
              #-------------------------------------------------------#   
              niveau = 1
              type = 'N'                          
              chapitre = chapitre + 1
              sous_chapitre = 0
              nbrSerie = 0
              nbrChapitre = chapitre * 100000
              cleArbre = chapitre
              nbrOrdre = nbrChapitre 
         elif cle == 'SC':             			     
              #----- on traite le sous-chapitre ----------------------#
              #la cle est composee du chapitre et du sous-chapitre    #
              #-------------------------------------------------------#  
              niveau = 2
              type = 'N'  
              nbrSerie = 0         
              sous_chapitre = sous_chapitre + 1
              nbrSous_chapitre = sous_chapitre * 1000
              cleArbre = sous_chapitre
              nbrOrdre = nbrChapitre + nbrSous_chapitre              
         else:
						  #----- on traite la serie ------------------------------#
              # la cle est composee du code serie                     #
              #-------------------------------------------------------# 
              niveau = 3
              type = 'E' 
              cleArbre = cle
              nbrSerie = nbrSerie + 1
              nbrOrdre = nbrChapitre + nbrSous_chapitre + nbrSerie  
             
         #print '%s~%s~%d~%s~%d~%d~' % (cleArbre, nom, niveau, type, nbrOrdre, chapitre)
         
         codeSerie    =   str(cleArbre)
         nomSerie     =   str(nom)
         nivSerie     =   str(niveau)
         nodeType     =   str(type)
         numOrdre     =   str(nbrOrdre)
         codeChap     =   str(chapitre)
         
         insertTable	= "insert into arbre (code_serie,nom_serie,niv_serie,node_type,num_ordre,code_chap) values ('"+codeSerie+"','"+nomSerie+"',"+nivSerie+",'"+nodeType+"',"+numOrdre+",'"+codeChap+"')"
         try:
    		        cursorDC.execute(insertTable)#DataCenter
         except connectDB.cx_Oracle.IntegrityError, exc:
    		        error, = exc.args
    		        print "code = ", error.code, " message = ", error.message
          
#-------------------------------------------------------------------------------------------------

fichiersource = ameco.ouvrir(options.fileinput)
creeArbre(fichiersource)
fichiersource.close()
connectDB.connection.commit()   #DataCenter
connectDB.connection.close()    #DataCenter