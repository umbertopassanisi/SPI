#this file is only used for the nace2 nomenclature but could be extended to other nomenclature if needed 
import sys
from . import DBConnect
from . import DBAccess
from . import spiLibCreateTable

indicator = sys.argv[1]
nomenclature = sys.argv[2]
path = sys.argv[3]
tableName = 'structure'

if indicator == 'vash' :
    refIndicator = 'va'
elif indicator == 'emplsh' :
    refIndicator = 'emp'
else :
    sys.exit()

fileLog = open(path+'\\Log\\createDBStructureShare'+indicator+nomenclature+'.log','w')

refData, startYear = DBAccess.lectureNaceIndicatorData(refIndicator, nomenclature, tableName)

spiLibCreateTable.createTableTotalShare(refData, startYear, indicator, nomenclature, fileLog, tableName)

fileLog.close()
DBConnect.closeDB()