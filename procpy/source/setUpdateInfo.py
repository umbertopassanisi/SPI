import sys
import DBConnect
import DBAccess
import pprint

G_domain = sys.argv[1]#domain est aussi la deuxieme partie du nom de la table (par ex : domain = structure alors table = indicatorsstructure)

def setUpdateInfo(domain):
    DBAccess.setUpdateDate(domain)
    
setUpdateInfo(G_domain)
DBConnect.closeDB()