import sys
import DBConnect
import DBAccess
import pprint

G_domain = sys.argv[1]#domain est aussi la deuxieme partie du nom de la table (par ex : domain = structure alors table = indicatorsstructure)
try:
    G_nomenclature = sys.argv[2]
except:
    G_nomenclature = ''
    
def deleteIndicators(domain, nomenclature = ''):
    DBAccess.deleteIndicators(domain, nomenclature)
    
deleteIndicators(G_domain, G_nomenclature)
DBConnect.closeDB()