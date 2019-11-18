'''
 MATRICE COST STRUCTURE OF INDUSTRIES : INPSH
 ESA2010
 input : naio_10_cp1700.csv (siot)
 qui est le naio_10_cp1700.tsv standardise par le matrixEsa2010Naio.py 
 afin d'y ajouter les caracteres manquants dans les codes agregats
 flag (stk_flow) = TOTAL
'''
import  sys
import  glob
import  re
from    numpy import *
from    numpy.linalg import inv
import  libMatrix
import	FileAccessMatrix

dirWork         =  sys.argv[1]
IndOrPrd        =  sys.argv[2]
ext		        =  sys.argv[3]
dirUse          =  dirWork 

dirTXT			=  dirUse			+'\\Input\\txt'
dirInput        =  dirUse           +'\\Input\\tsv\\nace2'
dirOutput       =  dirUse           +'\\Output\\matrix'
dirLog          =  dirUse           +'\\Log'
fileNaceRow		=  'nace2CpaEsa2010Row'

if	IndOrPrd		== 'P':
	CPA_L68			=  'CPA_L68'
	CPA_L68A		=  'CPA_L68A'
	CPA_L68B		=  'CPA_L68B'
	fileNaceInput	=  'nace2CpaEsa2010'
	fichierCSV      =  dirInput         + '\\naio_10_cp1700.'+ext
	fileLog         =  open(dirLog      + '\\matrixInpshEsa2010.log', 'w')
	fileOutput      =  open(dirOutput   + '\\matrixDBInpshEsa2010.csv', 'w')
else:
	CPA_L68			=  'L68'
	CPA_L68A		=  'L68A'
	CPA_L68B		=  'L68B'
	fileNaceInput	=  'nace2Esa2010'
	fichierCSV      =  dirInput         + '\\naio_10_cp1750.'+ext
	fileLog         =  open(dirLog      + '\\matrixInpshEsa2010I.log', 'w')
	fileOutput      =  open(dirOutput   + '\\matrixDBInpshEsa2010I.csv', 'w')
# variables globales recues en parametre, le nom du fichier input : spi_tree_indicator_(country,rev1,rev2,sector).csv
# fichier = fichier input a traiter
 
#calcul de la matrice ce Leontief
def traitementMatriceA(keyP1, dicRealP1, dicCodeRow, dicResult):
	#Resultat 
	dicNaceRow		= {}
	dicNaceRow		= FileAccessMatrix.dicNace(fileNaceRow,dirTXT)	
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
	keyCodeRow        = list(dicCodeRow.keys())    
	keyCodeRow.sort()     
	for ligne in keyCodeRow:
		#codeProduit = ligne.replace('CPA_','')
		if	ligne[0:4] == 'CPA_':
			codeProduit = ligne
		else:
			codeProduit = 'CPA_' + ligne
		if  (codeProduit in dicNaceRow):
			ligneOuput = codeProduit+';'  #ligne = code produit au niveau de la ligne
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
	codeP1        = list(dicRealP1.keys())    
	codeP1.sort()                                             
	for keyP1 in codeP1: #key = country,year
		dicCodeRow    = {}
		dicRealP1[keyP1].sort()
		vectorP1      = dicRealP1[keyP1]
		vectorZero    = libMatrix.fonctionVectorZero(vectorP1)     
		for productLst  in dicRealP1[keyP1]:#chaque ligne est une liste avec le code produit et la valeur 
			productLst   = productLst.split('#')
			productP1    = productLst[0]
			valueP1      = float(productLst[1])
			keyMatriceP1 = keyP1 + '#' + productP1                       
			if  list(dicRealP1.keys())                
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
					if  keyMatriceP1 in dicNoProduct:
						continue
					# on calcul la matrice A qui est celle des coeficient technique
					else:
						dicCodeRow[product] = product
						try:
							keyResult = product+productP1 #la cle correspond au code produit de  la ligne et la colonne
							coefTechnique       = value/valueP1  
							dicResult[keyResult]= coefTechnique
						except:
							fileLog.write('Division par zero pour matrice '+keyMatriceP1+',keyNoProduct='+keyNoProduct+',value='+str(value)+',valueP1='+str(valueP1)+'\n')                           
		traitementMatriceA(keyP1, dicRealP1, dicCodeRow, dicResult)

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
	#dicNace		  =	DBAccess.dicNace('nace2','NAMA','0')
	dicNace			  =	FileAccessMatrix.dicNace(fileNaceInput,dirTXT)
	fichierInput      = open(fichierCSV,'r')
	rec1er            = fichierInput.readline() #1er rec avec les meta
	recMeta           = rec1er.split(',')
	recGeoTime        = recMeta[4].strip('\n').split('\t') 
	lstCol            = []
	#unit,stk_flow,induse,prod_na,geo\time
	for ligneCSV in fichierInput: 	
		ligne           = ligneCSV.split(',')       
		unit            = ligne[0].strip()
		flow            = ligne[1].strip()
		col             = ligne[2].strip()
		row             = ligne[3].strip()
		geoTime			= ligne[4]
		geoTime			= re.sub(r'[a-z]', '', geoTime)
		geoTime			= re.sub(r'[:]', '0', geoTime)
		ligneGeoTime    = geoTime.strip('\n').split('\t')
		geo             = ligneGeoTime[0].strip()
		#print geo, ' vector = ',len(vector),' ', vector     
		dicGeo[geo]        = geo
		dicProductRow[row] = row #les lignes de produits par pays varie, on les prend toutes pour l'affichage
		dicProductCol[col] = col #les colonnes de produits par pays varie, on les prend toutes pour l'affichage
		if  (flow == 'TOTAL' and unit == 'MIO_EUR' and col in dicNace): 
			#on  met chaque ligne de produits dans un dictionnnaire
			for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees qui commencent a l'indice 1 
				yy            = recGeoTime[i].strip() #record des metas 
				keyMatrice    = geo + '#' + yy + '#' + col #la cle sera par pays,annee,colonne
				try:
					valeur		= float(ligneGeoTime[i])
				except:
					fileLog.write('valeur non num'+str(keyMatrice)+' '+str(ligneGeoTime[i])+'\n')  
					valeur		= 0
				value         = row + '#' + str(valeur) # couple ligne, valeur
				if  keyMatrice in dicMatrice: # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE ligne
					dicMatrice[keyMatrice]  = dicMatrice[keyMatrice] + [value]
				else:
					dicMatrice[keyMatrice]  = [value]
			#pour le calcul du vecteur P1
			if  (row == 'B1G' or row == 'D21X31' or row == 'TOTAL'):  # on fera le total P1 par ligne ensuite (P1=B2G_B3G+D1+D29_M_D39+TOT_CA)                
				for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
					yy            = recGeoTime[i].strip() #record des metas
					keyGeoYY      = geo + '#' + yy
					valeur        = ligneGeoTime[i].strip()
					try:
						valeur		= float(ligneGeoTime[i])
					except:
						fileLog.write('P1,valeur non num'+str(keyMatrice)+str(ligneGeoTime[i])+'\n')  
						valeur		= 0
					keyProd       = row
					value         = col + '#' +str(valeur) #couple colonne, valeur
					if  keyGeoYY in dicMatriceP1Row:
						if  keyProd in dicMatriceP1Row[keyGeoYY]:
							dicMatriceP1Row[keyGeoYY][keyProd] = dicMatriceP1Row[keyGeoYY][keyProd] + [value]                              
						else:                          
							dicMatriceP1Row[keyGeoYY][keyProd] = [value]
					else:
						dicMatriceP1Row[keyGeoYY] = {} #on cree un nouveau dictionnaire pour le couple valeur, produit par ligne de produit
						dicMatriceP1Row[keyGeoYY][keyProd] = [value]                    
	fichierInput.close()
    
	#on cree l'ensemble de toute les colonnes
	keyDicProductCol  = list(dicProductCol.keys())
	keyDicProductCol.sort()
	for p in keyDicProductCol:
		lstCol  = lstCol + [p]
	setLstCol = set(lstCol)
	#nbr de ligne et de colonne max pour les matrices
	nbrRow           = len(dicProductRow)
	nbrCol           = len(dicProductCol)
	#on va sommer les valeurs B1G,D21_M_D31,CPA_TOTAL dans une seule ligne P1 par pays/annee
	keyMatriceP1Row  = list(dicMatriceP1Row.keys())    
	keyMatriceP1Row.sort()
	for cleMatriceP1 in keyMatriceP1Row: #key = country,year,product B1G,D21_M_D31,CPA_TOTAL
		lstValue     = ''
		oldValue     = ''
		oldProd      = ''                
		dicP1[cleMatriceP1]=['']
		for cleProd  in dicMatriceP1Row[cleMatriceP1]:#on balaye les produits par ligne : B1G,D21_M_D31,CPA_TOTAL                 
			currentLst        = dicMatriceP1Row[cleMatriceP1][cleProd]
			currentValue      = libMatrix.vectorSetCol(currentLst,setLstCol) #la fonction fait un vecteur avec TOUTES les colonnes
			currentProd       = cleProd 
			if  (oldValue != ''): #on fait le test pour le 1er record
				lstValue  = libMatrix.addP1(cleMatriceP1, currentValue, oldValue)
				oldValue  = lstValue
			else:
				oldValue  = currentValue
		dicP1[cleMatriceP1]=lstValue
	#SELECTION DES MATRICES A TRAITER sur base de la matrice P1 (des totaux) 
	codeP1        = list(dicP1.keys())    
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
			if  (value != '0.0')and(value != '0') :
				matriceVide         = 0    #la matrice ne sera pas vide,il y a au moins une col de remplie
				if (product == CPA_L68): 
					L68_test        = 100
					entryL68        = product + '#' + value
					continue
				if (product == CPA_L68A): 
					L68_test        = L68_test + 10
					entryL68A       = product + '#' + value
					continue 
				if (product == CPA_L68B): 
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
			keyNoProduct               = keyP1 + "#"+CPA_L68 
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne                                     
			fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')     
		if  (L68_test == 110):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68]
			keyNoProduct               = keyP1 + "#"+CPA_L68A
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne                                        
			fileLog.write('Colonne CPA_L68A enleve pour matrice = ' + keyP1 +'\n')            
		if  (L68_test == 101):
			dicRealP1[keyP1]           = dicRealP1[keyP1] + [entryL68B]
			keyNoProduct               = keyP1 + "#"+CPA_L68
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