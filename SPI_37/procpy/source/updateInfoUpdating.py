import sys
from pprint import pprint
import DBAccessUtility

G_status = sys.argv[1]

def main(status):
   
    DBAccessUtility.setInfoUpdating(status)
        
main(G_status)
