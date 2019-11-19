#
# MATRICE OUTPUT MULTIPLIER DOMESTIC: OMULT
# input : naio_cp18_r2.tsv (dom)
#
import  sys
import  glob
from    numpy import *
from    numpy.linalg import inv

dirWork         =  sys.argv[1]
dirUse          =  dirWork

dirInput        =  dirUse           +'\\Input\\tsv\\nace2'
dirOutput       =  dirUse           +'\\Output\\matrix'
dirLog          =  dirUse           +'\\Log'

fichierCSV      =  dirInput         + '\\naio_cp18_r2.tsv'
fileLog         =  open(dirLog      + '\\matrixOmult.log', 'w')
fileOutput      =  open(dirOutput   + '\\matrixDBOmult.csv', 'w')

# variables globales recues en parametre, le nom du fichier input : spi_tree_indicator_(country,rev1,rev2,sector).csv
# fichier = fichier input a traiter 

#fonction qui evite les decalages :
#on regarde ce qui existe dans le vecteur P1 et pas dans celui de la matrice, 
#dans ce cas on ajoute les codes produits de P1 avec des valeurs 0 
#   
def vectorAtraiter(vectorMatrice, vectorP1):
    vectorOutput = []
    lstProdP1    = []
    lstProdMat   = []    
    for c in (range(0,len(vectorP1))):
        productLst   = vectorP1[c].split('#')
        productP1    = productLst[0]
        lstProdP1    = lstProdP1 + [productP1]
        #lstProdMat   = []        
        for p in (range(0,len(vectorMatrice))):            
            pLst             = vectorMatrice[p].split('#')
            productMatrix    = pLst[0]

            if  productMatrix == productP1:
                lstProdMat    = lstProdMat + [productMatrix]
                vectorOutput  =  vectorOutput + [vectorMatrice[p]]
    setcolP1         = set(lstProdP1)
    setcolMat        = set(lstProdMat)                    
    setColNotInMat   = setcolP1 - setcolMat
    vectorReturn     = vectorOutput
    if  (len(setColNotInMat)>0):  
        for c in setColNotInMat:
            lineProd      = c + '#0'
            vectorReturn  = vectorReturn + [lineProd]                      
    return vectorReturn

def fonctionVectorZero(vectorP1):
    vectorInput  = vectorP1    
    vectorOutput = []
    for c in (range(0,len(vectorInput))):
        productLst   = vectorInput[c].split('#')
        productOuput = productLst[0] + '#0'
        vectorOutput = vectorOutput + [productOuput]
    return vectorOutput      
#calcul de la matrice ce Leontief
def traitementMatriceA(keyP1, matriceA, dicRealP1):
    nbrEle          = len(matriceA)
    matriceIdentity = identity(nbrEle) # on cree la matrice identite tout des 1 en diagonale
    matrixIA        = matriceIdentity - matriceA  # soustraction de la matrice A de l'identite
    matriceL        = (inv(matrixIA)).astype(float64)  # on inverse la matrice IA pour obtenir la matrice de Leontief
    tabSumColL      = matriceL.sum(axis=0) #somme des colonnes par colonne de la matrice dans une table (axis=0)
    #Resultat   
    lstKeyP1         = keyP1.split("#")
    codeCountry      = lstKeyP1[0]
    yyyy             = lstKeyP1[1]      
    ligne             = 'New;Domestic Output multiplier for ;omult;'+str(codeCountry)+';'+str(yyyy)+'\n'
    fileOutput.write(ligne)
          
    #nameFile         = codeCountry+yyy
    
    #fileMatrice      = open(dirCSV + '\\matrixV' + nameFile +'.csv', 'w')
    #ligne = 'Matrix V for '+str(codeCountry)+','+str(yyyy)+'\n'
    #fileMatrice.write(ligne)
    #ligne des noms des produits par pays/annee
    #ligne       = codeCountry+","+yyyy
    
    #titre des codes CPA
    ligne   = 'Code;'
    l       = 0
    tabCode = []    
    dicRealP1[keyP1]['P1'].sort()
    for n in dicRealP1[keyP1]['P1']:
        codeProd    = n.split("#")
        ligne       = ligne+str(codeProd[0])+"," 
        tabCode.append(codeProd[0])       
    fileOutput.write(ligne[0:-1]+'\n')
     
    #corps de la matrice
    for l in range(0,nbrEle):
        ligne=tabCode[l]+';'
        for c in range(0,nbrEle):    
            ligne   = ligne+str(matriceL[l,c])+","      
        fileOutput.write(ligne[0:-1]+'\n')   


    #valeur totale
    ligne='omult;'
    for i in range(0,len(tabSumColL)):
        ligne   = ligne+str(tabSumColL[i])+","      
    fileOutput.write(ligne[0:-1]+'\n')    
                            
def traitementMatrice(dicRealP1, dicMatrice, dicNoProduct):
    codeP1        = dicRealP1.keys()    
    codeP1.sort()                                              
    for keyP1 in codeP1: #key = country,year
        nbrEleP1      = len(dicRealP1[keyP1]['P1'])
        matriceA      = zeros((nbrEleP1,nbrEleP1), dtype=float)
        ligne         = 0
        col           = 0
        dicRealP1[keyP1]['P1'].sort()
        vectorP1      = dicRealP1[keyP1]['P1']
        vectorZero    = fonctionVectorZero(vectorP1)            
        for productLst  in dicRealP1[keyP1]['P1']:#chaque ligne est une liste avec le code produit et la valeur 
            productLst   = productLst.split('#')
            productP1    = productLst[0]
            valueP1      = float(productLst[1])
            keyMatriceP1 = keyP1 + '#' + productP1
            ligne        = 0
            if  dicNoProduct.has_key(keyMatriceP1):                
                continue
            else:
                try:# la ligne de la matrice est dans P1
                    dicMatrice[keyMatriceP1].sort()
                    vectorMatrice = dicMatrice[keyMatriceP1]
                except:#la ligne est dans P1 mais PAS dans la matrice, on met un vector avec les valeurs 0 ex: CPA_T pour EE
                    vectorMatrice = vectorZero
                    fileLog.write('le produit '+ productP1+ ' existe dans P1 mais pas dans la MATRICE = '+keyP1+'\n')            
                vectorP1      = dicRealP1[keyP1]['P1']
                #evite les decalages entre P1 et la Matrice, on peux avoir une colonne dans P1 et pas dans la matrice
                #dans ce cas on ajoute une colonne avec des zero
                ligneAtraiter = vectorAtraiter(vectorMatrice, vectorP1)                                                                        
                ligneAtraiter.sort()                
                for ligneMatrice in     ligneAtraiter:  # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE ligne
                    ligneMatrice        = ligneMatrice.split('#')
                    product             = ligneMatrice[0]                
                    value               = float(ligneMatrice[1])
                    keyNoProduct        = keyP1 + "#" + product               
                    if  dicNoProduct.has_key(keyNoProduct): 
                        continue
                    # on calcul la matrice A qui est celle des coeficient technique
                    else:
                        if  (ligne < nbrEleP1): # le nombre element dans la ligne doit etre le meme que celui de P1 
                            matriceA[ligne,col] = value/valueP1
                            ligne+=1
                        else:
                            #print keyMatriceP1, ' ',len(dicMatrice[keyMatriceP1])
                            fileLog.write('Probleme matrice: nbrLigne > nbrEleP1 '+keyMatriceP1+',Col='+str(col)+',ligne='+str(ligne)+',maxEle='+str(nbrEleP1)+' '+str(len(dicMatrice[keyMatriceP1]))+'\n')
                if  (col < nbrEleP1):                                                
                    col+=1
                else:
                    fileLog.write('Probleme matrice: nbrColonne > nbrEleP1 '+keyMatrice+',Col='+str(col)+',ligne='+str(ligne)+',maxEle='+str(nbrEleP1)+'\n')
        #print keyP1, 'len(matriceA)=',len(matriceA), ' len( dicRealP1)=' ,len(dicRealP1) , ' len( mVector)=' ,len(mVector), mVector[len(mVector)-1]                  
        traitementMatriceA(keyP1, matriceA, dicRealP1)             
            
#unit,t_cols2,t_rows2,geo\time	2010 	2009 	2008 	2005 	2000 	1995 
def traitementFichierCSV():
    dicMatrice        = {}
    dicP1             = {}
    dicMatriceP1Row   = {}    
    dicSelectB1G      = {}
    dicB1G            = {}    
    dicRealP1         = {}
    dicGeo            = {}
    dicNoProduct      = {}
    fichierInput      = open(fichierCSV,'r')
    rec1er            = fichierInput.readline() #1er rec avec les meta
    recMeta           = rec1er.split(',')
    recGeoTime        = recMeta[3].strip('\n').split('\t')

    #MIO_EUR,CPA_A01,B1G,AT	: 	1963.57 	2455.13 	: 	: 	: 
    for ligneCSV in fichierInput:
        ligneCSV        = ligneCSV.replace(':','0') 
        ligne           = ligneCSV.split(',')       
        unit            = ligne[0].strip()
        col             = ligne[1].strip()
        row             = ligne[2].strip()
        ligneGeoTime    = ligne[3].strip('\n').split('\t')
        geo             = ligneGeoTime[0].strip()
        dicGeo[geo]     = geo
        if  (unit == 'MIO_EUR'):
            #on  met chaque ligne de produits dans un dictionnnaire
            if  ((col[:3] == 'CPA')and(col != 'CPA_TOTAL')) and ((row[:3] == 'CPA')and(row != 'CPA_TOTAL')): #pas prendre cpa_total
                for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
                    yy            = recGeoTime[i].strip() #record des metas 
                    keyMatrice    = geo + '#' + yy + '#' + col
                    value         = row + '#' + ligneGeoTime[i].strip()
                    if  dicMatrice.has_key(keyMatrice): # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE COLONNE
                        dicMatrice[keyMatrice]  = dicMatrice[keyMatrice] + [value]
                    else:
                        dicMatrice[keyMatrice]  = [value]
            #pour le vecteur P1
            if  (row == 'P1')and((col[:3] == 'CPA')and(col != 'CPA_TOTAL')):                
                for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
                    yy            = recGeoTime[i].strip() #record des metas
                    keyGeoYY      = geo + '#' + yy                    
                    value         = col + '#' + ligneGeoTime[i].strip()
                    keyProd       = row
                    if  dicMatriceP1Row.has_key(keyGeoYY):
                        if  dicMatriceP1Row[keyGeoYY].has_key(keyProd):
                            dicMatriceP1Row[keyGeoYY][keyProd] = dicMatriceP1Row[keyGeoYY][keyProd] + [value]                              
                        else:                          
                            dicMatriceP1Row[keyGeoYY][keyProd] = [value]
                    else:
                        dicMatriceP1Row[keyGeoYY] = {} #on cree un nouveau dictionnaire pour le couple valeur, produit par ligne de produit
                        dicMatriceP1Row[keyGeoYY][keyProd] = [value]                                                     
                        
    fichierInput.close()
    
    dicKeyP1Row   = dicMatriceP1Row.keys()
    dicKeyP1Row.sort()

    #SELECTION DES MATRICES A TRAITER                                         
    for keyP1 in dicKeyP1Row: #key = country,year
        matriceVide      = 1  # on considere que la matrice est vide au depart
        L68_test         = 0
        entryL68P1      = 'CPA_L68#0'
        entryL68AP1     = 'CPA_L68A#0' 
        entryL68BP1     = 'CPA_L68B#0'
        entryL68B1G     = 'CPA_L68#0'
        entryL68AB1G    = 'CPA_L68A#0' 
        entryL68BB1G    = 'CPA_L68B#0'         
        dicRealP1[keyP1] = {} # dictionnaire avec les matrices P1 a traiter                    
        #on s'assure que la liste P1 est dans le bon ordre        
        keyRow                   = 'P1'
        dicMatriceP1Row[keyP1][keyRow].sort()#on tri la liste des produits P1 
        dicRealP1[keyP1][keyRow] = []
        for productLst  in dicMatriceP1Row[keyP1][keyRow]:#chaque ligne est une liste avec le code produit et la valeur 
            productLst   = productLst.split('#')
            product      = productLst[0]
            value        = productLst[1]
            if  (value != '0'):
                matriceVide         = 0    #la matrice ne sera pas vide,il y a au moins une col de remplie
                valueP1Vide         = 0
                if (product == 'CPA_L68'):
                    entryL68P1        = product + '#' + value                 
                    continue
                if (product == 'CPA_L68A'):
                    entryL68AP1       = product + '#' + value                 
                    continue 
                if (product == 'CPA_L68B'):
                    entryL68BP1       = product + '#' + value                 
                    continue
                entryP1                         = product + '#' + value
                dicRealP1[keyP1][keyRow]        = dicRealP1[keyP1][keyRow] + [entryP1]                
            else:
                if  (matriceVide == 0): #si la matrice n'est pas vide alors on enleve les col/row qui n'ont pas de valeur
                                        #on fait le test pour eviter que le logfile soit aussi remplir avec toutes les col
                                        #vide d'une matrice vide
                    keyNoProduct               = keyP1 + "#" + product 
                    dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
                    fileLog.write('Colonne vide pour matrice = ' + keyNoProduct +' keyRow='+keyRow +'\n')            
                                        
        #traitement des cas de L68
        if  (L68_test == 111):
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68AP1] + [entryL68BP1]            
            keyNoProduct               = keyP1 + "#CPA_L68" 
            dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
            fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')                                  
        if  (L68_test == 110):
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68P1]  
            keyNoProduct               = keyP1 + "#CPA_L68A" 
            dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
            fileLog.write('Colonne CPA_L68A enleve pour matrice = ' + keyP1 +'\n')            
        if  (L68_test == 101):
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68BP1]        
            keyNoProduct               = keyP1 + "#CPA_L68" 
            dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
            fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')
        if  (L68_test == 100):                             
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68P1]                        
        if  (L68_test == 11):
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68AP1] + [entryL68BP1]          
        if  (L68_test == 10):
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68AP1]             
        if  (L68_test == 1):
            dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68BP1]                                                                
        if  (matriceVide): #la matrice est vide si toute les valeurs de P1 sont vides
            matriceVide = 0
            del dicRealP1[keyP1] #on supprime les reference inutiles aux matrices vide partie B1G     
            fileLog.write('Matrice Vide = ' + keyP1 + '\n')               

    #TRAITEMENT DES MATRICES           
    traitementMatrice(dicRealP1, dicMatrice, dicNoProduct)
  
traitementFichierCSV()
fileOutput.close()
fileLog.close()               