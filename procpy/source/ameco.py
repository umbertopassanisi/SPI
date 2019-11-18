def ouvrir(fichier):
    try:
        f = open(fichier, 'U')
        return f
    except:
        print "le fichier ", fichier, " est introuvable"

def ouvrir_w(fichier):
    try:
        f = open(fichier, 'w')
        return f
    except:
        print "le fichier ", fichier, " est introuvable"
        
def ouvrir_wb(fichier):
    try:
        f = open(fichier, 'wb')
        return f
    except:
        print "le fichier ", fichier, " est introuvable"
                 
def selectCle(serie, cle, attrib, chapitre, codeserie):
    if   attrib == -1:
         serie[cle[codeserie],chapitre]=chapitre
    else:
         serie[(cle[codeserie],cle[attrib])]=chapitre
    return serie

def lire(fichiersource, attrib=-1, codeserie=5):
    nbr = 0
    serie = {}
    for l in fichiersource: 
        rec = l.split(';')
        cle = rec[0].split('.')
        if len(cle) == 6:
             selectCle(serie, cle, attrib, chapitre, codeserie)
        else:
             chapitre=rec[0]
        nbr = nbr + 1
    print " nbr record = ", nbr
    return serie
    
def imprime(serie):
    trier_serie = serie.keys()
    trier_serie.sort()
    for i in trier_serie:
        if   len(i) > 1:
             print "SERIE = %s  ATTRIBUT = %s CHAPITRE = %s" % (i[0], i[1], serie[i])
        else:
             print "SERIE = %s  CHAPITRE = %s" % (i[0], serie[i])
    print "nbr serie = ", len(serie)    