import DBConnect2
from pprint import pprint



def getDomNomList():
    
    token = DBConnect2.connect()
    cursor = token.cursor()
    
    queryString = 'select id_domain, id_nomenclature from dom_nom'
    result = []
    tmp = ()
    
    try:
        cursor.execute(queryString)
    except:
        DBConnect2.close(token)
        print('Error executing the database query')
        return
    
    for rec in cursor.fetchall():
        tmp = (rec[0], rec[1])
        result.append(tmp)
    
    DBConnect2.close(token)
    
    return result

def getDomNomMinYear(domain, nomenclature):
    
    token = DBConnect2.connect()
    cursor = token.cursor()
    
    queryString = "select min(yyyy) from indicators" + domain + " where upper(typeprod)=upper('" + nomenclature + "')"
    result = -1
    try:
        cursor.execute(queryString)
    except:
        DBConnect2.close(token)
        print('Error executing the database query')
        return
    
    for rec in cursor.fetchall():
        result = rec[0]
    
    DBConnect2.close(token)
    
    return result

def updateDomNomDates(domain, nomenclature, startYear, endYear):
    
    token = DBConnect2.connect()
    cursor = token.cursor()
    
    queryString = "update dom_nom set start_year=" + str(startYear) + ", end_year=" + str(endYear) + " where id_domain='" + domain + "' and id_nomenclature='" + nomenclature + "'"
    
    try:
        cursor.execute(queryString)
    except:
        DBConnect2.close(token)
        print('Error executing the database query : ' + queryString)
        return
    
    DBConnect2.commitAndClose(token)

def setInfoUpdating(status):
    
    token = DBConnect2.connect()
    cursor = token.cursor()
    
    queryString = "update info set updating=" + str(status)
    
    try:
        cursor.execute(queryString)
    except:
        DBConnect2.close(token)
        print('Error executing the database query : ' + queryString)
        return
    
    DBConnect2.commitAndClose(token)
    
    