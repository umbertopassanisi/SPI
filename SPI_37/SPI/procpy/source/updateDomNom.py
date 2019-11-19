import sys
import datetime
from pprint import pprint
import DBAccessUtility

def main():
    endYear = datetime.date.today().year
    domNomList = DBAccessUtility.getDomNomList()
    
    for domNom in domNomList:   
        startYear = DBAccessUtility.getDomNomMinYear(domNom[0], domNom[1]) 
        DBAccessUtility.updateDomNomDates(domNom[0], domNom[1], startYear, endYear)
main()
