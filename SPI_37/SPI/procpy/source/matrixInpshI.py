#
# MATRICE COST STRUCTURE OF INDUSTRIES : INPSH
# input : naio_cp17i_r2.tsv (siot)
import sys
import  glob
import  re
from    numpy import *
from    numpy.linalg import inv
#import  DBAccess
import	FileAccessMatrix

dirWork         =  sys.argv[1]
dirUse          =  dirWork 

dirInput        =  dirUse           +'\\Input\\tsv\\nace2'
dirOutput       =  dirUse           +'\\Output\\matrix'
dirLog          =  dirUse           +'\\Log'
dirTXT			=  dirUse			+'\\Input\\txt'
fichierCSV      =  dirInput         + '\\naio_cp17i_r2.tsv'
fileLog         =  open(dirLog      + '\\matrixIInpsh.log', 'w')
fileOutput      =  open(dirOutput   + '\\matrixIDBInpsh.csv', 'w')
# variables globales recues en parametre, le nom du fichier input : spi_tree_indicator_(country,rev1,rev2,sector).csv
# fichier = fichier input a traiter 

def vectorCol(currentLst,setLstCol):
    lstColValue      = currentLst
    if  (len(setLstCol)>len(currentLst)):   
        lstColInput      = []
        for c in (range(0,len(lstColValue))):
            lineProd     = lstColValue[c].split('#')
            lstColInput  = lstColInput + [lineProd[0]]
        setColInput      =  set(lstColInput)
        setColNotInAll   =  setLstCol - setColInput
        for c in setColNotInAll:
            lineProd        = c + '#0'
            lstColValue     = lstColValue + [lineProd]
    return lstColValue
    
def fonctionVectorZero(vectorP1):
    vectorInput  = vectorP1    
    vectorOutput = []
    for c in (range(0,len(vectorInput))):
        productLst   = vectorInput[c].split('#')
        productOuput = productLst[0] + '#0'
        vectorOutput = vectorOutput + [productOuput]
    return vectorOutput
               
def addP1(cleMatriceP1, currentValue, oldValue):
    vecAdd  = []
    lstProdX        = currentValue
    lstProdY        = oldValue
    lstProdX.sort()
    lstProdY.sort()
    for p in range(0,len(lstProdX)):
        X                   = lstProdX[p]
        x                   = X.split('#')
        produitX            = x[0]                          
        xf                  = float(x[1])            
        Y           = lstProdY[p]
        y           = Y.split('#')
        yf          = float(y[1])
        produitY    = y[0]
        if  (produitX != produitY):
             fileLog.write('catastrophe nom produit different matrice ='+cleMatriceP1+' produitX='+produitX+' produitY='+produitY+'\n')            
        totAdd          = xf+yf
        eleVec          = produitX+'#'+str(totAdd)
        vecAdd          = vecAdd + [eleVec]
    return vecAdd

#calcul de la matrice ce Leontief
def traitementMatriceA(keyP1, dicRealP1, dicCodeRow, dicResult):
    #Resultat   
    lstKeyP1          = keyP1.split("#")
    codeCountry       = lstKeyP1[0]
    yyyy              = lstKeyP1[1]    
    dicRealP1[keyP1].sort()
    nameFile          = codeCountry+yyyy
    #fileMatriceA      = open(dirCSV + '\\matrixInpsh' + nameFile +'.csv', 'w')
    ligne             = 'New;Cost structure of industries for ;inpsh;'+str(codeCountry)+';'+str(yyyy)+'\n'
    fileOutput.write(ligne)
    #ligne des noms des produits par pays/annee
    #ligne       = codeCountry+","+yyyy
    #titre des codes CPA
    ligne   = 'Code;'
    for n in dicRealP1[keyP1]:
        codeProd    = n.split("#")
        ligne       = ligne+str(codeProd[0])+","       
    fileOutput.write(ligne[0:-1]+'\n')
    #corps de la matrice
    keyCodeRow        = dicCodeRow.keys()    
    keyCodeRow.sort()     
    for ligne in keyCodeRow:
        ligneOuput = ligne+';'  #ligne = code produit au niveau de la ligne
        for c in range(0,len(dicRealP1[keyP1])):
            colLst    = dicRealP1[keyP1][c].split('#')#colLst[0] = code produit au niveau de la colonne
            keyResult = ligne+colLst[0]
            if  dicResult.has_key(keyResult):
                valueSiot    = float(dicResult[keyResult])*100
                ligneOuput   = ligneOuput + str(valueSiot) +","
            else:
                ligneOuput   = ligneOuput+"0.0,"          
        fileOutput.write(ligneOuput[0:-1]+'\n')    
    #ligne des valeurs des produits par pays/annee 
    #ligne       = codeCountry+","+yyyy
    #valeur totale
    ligne='multinpsh;'
    for n in dicRealP1[keyP1]:
        codeProd    = n.split("#")
        ligne       = ligne + str(codeProd[1]) +","      
    fileOutput.write(ligne[0:-1]+'\n')
    
    #fileMatriceA.close()   
                            
def traitementMatrice(dicRealP1, dicMatrice, dicNoProduct, nbrRow, nbrCol):
    dicResult     = {}
    codeP1        = dicRealP1.keys()    
    codeP1.sort()                                             
    for keyP1 in codeP1: #key = country,year
        dicCodeRow    = {}
        dicRealP1[keyP1].sort()
        vectorP1      = dicRealP1[keyP1]
        vectorZero    = fonctionVectorZero(vectorP1)     
        for productLst  in dicRealP1[keyP1]:#chaque ligne est une liste avec le code produit et la valeur 
            productLst   = productLst.split('#')
            productP1    = productLst[0]
            valueP1      = float(productLst[1])
            keyMatriceP1 = keyP1 + '#' + productP1                       
            if  dicNoProduct.has_key(keyMatriceP1):                
                continue
            else:
                try:# la ligne de la matrice est dans P1
                    dicMatrice[keyMatriceP1].sort()
                    vectorMatrice = dicMatrice[keyMatriceP1]
                except:#la ligne est dans P1 mais PAS dans la matrice, on met un vector avec les valeurs 0 ex: CPA_T pour EE
                    vectorMatrice = vectorZero
                    fileLog.write('le produit '+ productP1+ ' existe dans P1 mais pas dans la MATRICE = '+keyP1+'\n')             
                #dicMatrice[keyMatriceP1].sort()
                vectorMatrice.sort()   
                for ligneMatrice in     vectorMatrice:  # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE ligne
                    ligneMatrice        = ligneMatrice.split('#')
                    product             = ligneMatrice[0]
                    if  (product == 'P1'):#on a recalcule le P1 sur base des row P1=B2G_B3G+D1+D29_M_D39+TOT_CA, dans certain cas le P1 input est vide ou zero
                        value           = valueP1
                    else:
                        value           = float(ligneMatrice[1])                    
                    keyNoProduct        = keyP1 + "#" + product               
                    if  dicNoProduct.has_key(keyNoProduct):
                        continue
                    # on calcul la matrice A qui est celle des coeficient technique
                    else:
                        dicCodeRow[product] = product
                        try:
                            keyResult = product+productP1 #la cle correspond au code produit de  la ligne et la colonne
                            coefTechnique       = value/valueP1  
                            dicResult[keyResult]= coefTechnique
                        except:
                            fileLog.write('Division par zero pour matrice '+keyMatriceP1+',Col='+str(col)+',ligne='+str(ligne)+',value='+str(value)+',valueP1='+str(valueP1)+'\n')                           
        traitementMatriceA(keyP1, dicRealP1, dicCodeRow, dicResult)
                           
#unit,t_cols2,t_rows2,geo\time	2010 	2009 	2008 	2005 	2000 	1995 
def traitementFichierCSV():
	dicMatrice        = {}
	dicMatriceP1      = {}
	dicMatriceP1Row   = {}
	dicP1             = {}
	dicRealP1         = {}
	dicGeo            = {}
	dicProductRow     = {}
	dicProductCol     = {}     
	dicNoProduct      = {}
	dicNace		      = {}
	#dicNace			  =	DBAccess.dicNace('nace2','NAMA','0')
	dicNace			  =	FileAccessMatrix.dicNace('nace2',dirTXT)	
	fichierInput      = open(fichierCSV,'r')
	rec1er            = fichierInput.readline() #1er rec avec les meta
	recMeta           = rec1er.split(',')
	recGeoTime        = recMeta[3].strip('\n').split('\t') 
	lstCol            = []
	#MIO_EUR,CPA_A01,B1G,CZ	: 	1683.15 	: 	1614.77 	1523.5 	1324.13 
	for ligneCSV in fichierInput:
		ligneCSV        = ligneCSV.replace(':','0') 
		ligne           = ligneCSV.split(',')       
		unit            = ligne[0].strip()
		col             = ligne[1].strip()
		row             = ligne[2].strip()
		ligneGeoTime    = ligne[3].strip('\n').split('\t')        
		geo             = ligneGeoTime[0].strip()
		#print geo, ' vector = ',len(vector),' ', vector     
		dicGeo[geo]        = geo
		dicProductRow[row] = row #les lignes de produits par pays varie, on les prend toutes pour l'affichage
		dicProductCol[col] = col #les colonnes de produits par pays varie, on les prend toutes pour l'affichage
  
		#print  ligneGeoTime
		#if  (unit == 'MIO_EUR')
		if  (unit == 'MIO_EUR') and (col[:3] == 'CPA') and (geo == 'FI' or geo =='NL'):        
			#on  met chaque ligne de produits dans un dictionnnaire
			for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees qui commencent a l'indice 1 
				yy            = recGeoTime[i].strip() #record des metas 
				keyMatrice    = geo + '#' + yy + '#' + col #la cle sera par pays,annee,colonne
				valeur        = ligneGeoTime[i]
				value         = row + '#' + valeur # couple ligne, valeur
				if  dicMatrice.has_key(keyMatrice): # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE ligne
					dicMatrice[keyMatrice]  = dicMatrice[keyMatrice] + [value]
				else:
					dicMatrice[keyMatrice]  = [value]
			#pour le calcul du vecteur P1
			if  (row == 'B1G')or(row == 'D21_M_D31')or(row == 'CPA_TOTAL'):  # on fera le total P1 par ligne ensuite (P1=B2G_B3G+D1+D29_M_D39+TOT_CA)                
				for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
					yy            = recGeoTime[i].strip() #record des metas
					keyGeoYY      = geo + '#' + yy
					valeur        = ligneGeoTime[i].strip()
					keyProd       = row
					value         = col + '#' +valeur #couple colonne, valeur
					if  dicMatriceP1Row.has_key(keyGeoYY):
						if  dicMatriceP1Row[keyGeoYY].has_key(keyProd):
							dicMatriceP1Row[keyGeoYY][keyProd] = dicMatriceP1Row[keyGeoYY][keyProd] + [value]                              
						else:                          
							dicMatriceP1Row[keyGeoYY][keyProd] = [value]
					else:
						dicMatriceP1Row[keyGeoYY] = {} #on cree un nouveau dictionnaire pour le couple valeur, produit par ligne de produit
						dicMatriceP1Row[keyGeoYY][keyProd] = [value]                    
	fichierInput.close()

	#on cree l'ensemble de toute les colonnes
	keyDicProductCol  = dicProductCol.keys()
	keyDicProductCol.sort()
	for p in keyDicProductCol:
		lstCol  = lstCol + [p]
	setLstCol = set(lstCol)
     
	#nbr de ligne et de colonne max pour les matrices
	nbrRow           = len(dicProductRow)
	nbrCol           = len(dicProductCol)
	#on va sommer les valeurs B1G,D21_M_D31,CPA_TOTAL dans une seule ligne P1 par pays/annee
	keyMatriceP1Row  = dicMatriceP1Row.keys()    
	keyMatriceP1Row.sort()
	for cleMatriceP1 in keyMatriceP1Row: #key = country,year,product B1G,D21_M_D31,CPA_TOTAL
		lstValue     = ''
		oldValue     = ''
		oldProd      = ''                
		dicP1[cleMatriceP1]=['']
		for cleProd  in dicMatriceP1Row[cleMatriceP1]:#on balaye les produits par ligne : B1G,D21_M_D31,CPA_TOTAL                 
			currentLst        = dicMatriceP1Row[cleMatriceP1][cleProd]
			currentValue      = vectorCol(currentLst,setLstCol) #la fonction fait un vecteur avec TOUTES les colonnes
			currentProd       = cleProd 
			if  (oldValue != ''): #on fait le test pour le 1er record
				lstValue  = addP1(cleMatriceP1, currentValue, oldValue)
				oldValue  = lstValue
			else:
				 oldValue = currentValue
		dicP1[cleMatriceP1]=lstValue
	#SELECTION DES MATRICES A TRAITER sur base de la matrice P1 (des totaux) 
	codeP1        = dicP1.keys()    
	codeP1.sort()                                                                         
	for keyP1 in codeP1: #key = country,year 
		matriceVide      = 1  # on considere que la matrice est vide au depart
		dicRealP1[keyP1] = [] # dictionnaire avec les matrices a traiter 
		L68_test         = 0
		entryL68         = ''
		entryL68A        = '' 
		entryL68B        = ''                  
		#on s'assure que la liste P1 est dans le bon ordre
		try:
		  dicP1[keyP1].sort()#on tri la liste des produits
		except:
		  logLine='probleme de tri  keyP1=' + keyP1 + ' dicP1[keyP1]='+ dicP1[keyP1]
		  fileLog.write(logLine+'\n')
		for productLst  in dicP1[keyP1]:#chaque ligne est une liste avec le code produit et la valeur 
			productLst   = productLst.split('#')
			product      = productLst[0]
			value        = productLst[1]
			if  (value != '0.0'):
				matriceVide         = 0    #la matrice ne sera pas vide,il y a au moins une col de remplie
				if (product == 'CPA_L68'): 
					L68_test        = 100
					entryL68        = product + '#' + value
					continue
				if (product == 'CPA_L68A'): 
					L68_test        = L68_test + 10
					entryL68A       = product + '#' + value
					continue 
				if (product == 'CPA_L68B'): 
					L68_test        = L68_test + 1
					entryL68B       = product + '#' + value
					continue
				entryP1             = product + '#' + value
				dicRealP1[keyP1]    = dicRealP1[keyP1] + [entryP1]
			else:
				if  (matriceVide == 0): #si la matrice n'est pas vide alors on enleve les col/row qui n'ont pas de valeur
										#on fait le test pour eviter que le logfile soit aussi remplir avec toutes les col
										#vide d'une matrice vide
					keyNoProduct               = keyP1 + "#" + product 
					dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
					fileLog.write('Colonne vide pour matrice = ' + keyNoProduct +'\n')                    
		#traitement des cas de L68
		if  (L68_test == 111):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68A] + [entryL68B]
			keyNoProduct               = keyP1 + "#CPA_L68" 
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne                                     
			fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')     
		if  (L68_test == 110):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68]
			keyNoProduct               = keyP1 + "#CPA_L68A" 
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne                                        
			fileLog.write('Colonne CPA_L68A enleve pour matrice = ' + keyP1 +'\n')            
		if  (L68_test == 101):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68B]
			keyNoProduct               = keyP1 + "#CPA_L68" 
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne                                        
			fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')
		if  (L68_test == 100):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68]            
		if  (L68_test == 11):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68A] + [entryL68B]  
		if  (L68_test == 10):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68A] 
		if  (L68_test == 1):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68B]                                                        
		if  (matriceVide): #la matrice est vide si toute les valeurs de P1 sont vides
			del dicRealP1[keyP1] #on supprime les reference inutiles aux matrices vide      
			fileLog.write('Matrice Vide = ' + keyP1 + '\n')
				
	#TRAITEMENT DES MATRICES         
	traitementMatrice(dicRealP1, dicMatrice, dicNoProduct, nbrRow, nbrCol)
  
traitementFichierCSV()
fileLog.close()
fileOutput.close()            