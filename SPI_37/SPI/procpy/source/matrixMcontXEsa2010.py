# ESA2010
# MATRICE IMPORT CONTENTS OF EXPORT : MCONTX
# input : naio_cp18_r2.tsv (dom)
#       : naio_cp19_r2.tsv
# ESA2010
# input : naio_10_cp1700.tsv pour product
# input : naio_10_cp1750.tsv pour industry 
# flag (stk_flow) = DOM (cp18)
# flag (stk_flow) = IMP (cp19)

import  sys
import  glob
import  re
from    numpy import *
from    numpy.linalg import inv
from . import  libMatrix
from . import	FileAccessMatrix

dirWork         =  sys.argv[1]
IndOrPrd        =  sys.argv[2]
ext		        =  sys.argv[3]
dirUse          =  dirWork 

dirTXT			=  dirUse			+'\\Input\\txt'
dirInput        =  dirUse           +'\\Input\\tsv\\nace2'
dirOutput       =  dirUse           +'\\Output\\matrix'
dirLog          =  dirUse           +'\\Log'

if	IndOrPrd		== 'P':
	CPA_L68			=  'CPA_L68'
	CPA_L68A		=  'CPA_L68A'
	CPA_L68B		=  'CPA_L68B'
	fileNaceInput	=  'nace2CpaEsa2010'
	fichierCSV      =  dirInput         + '\\naio_10_cp1700.'+ext #DOM
	fichierP2I      =  dirInput         + '\\naio_10_cp1700.'+ext #IMP
	fileLog         =  open(dirLog      + '\\matrixMcontXEsa2010.log', 'w')
	fileMatrice     =  open(dirOutput   + '\\matrixMcontXEsa2010.csv', 'w')
	fileOutput      =  open(dirOutput   + '\\matrixMcontXAllEsa2010.csv', 'w')
	fileMatriceDB   =  open(dirOutput   + '\\matrixDBMcontXEsa2010.csv', 'w')
else:
	CPA_L68			=  'L68'
	CPA_L68A		=  'L68A'
	CPA_L68B		=  'L68B'
	fileNaceInput	=  'nace2Esa2010'
	fichierCSV      =  dirInput         + '\\naio_10_cp1750.'+ext #DOM
	fichierP2I      =  dirInput         + '\\naio_10_cp1750.'+ext #IMP
	fileLog         =  open(dirLog      + '\\matrixMcontXEsa2010I.log', 'w')
	fileMatrice     =  open(dirOutput   + '\\matrixMcontXEsa2010I.csv', 'w')
	fileOutput      =  open(dirOutput   + '\\matrixMcontXAllEsa2010I.csv', 'w')
	fileMatriceDB   =  open(dirOutput   + '\\matrixDBMcontXEsa2010I.csv', 'w')
	
fileMatrice.write('Country/Year;mContX;Total Export Vector;mContXPercent\n')

# variables globales recues en parametre, le nom du fichier input : spi_tree_indicator_(country,rev1,rev2,sector).csv
# fichier = fichier input a traiter
       
#calcul de la matrice ce Leontief
def traitementMatriceA(keyP1, matriceA, dicRealP1, mVector):
	nbrEle          = len(matriceA)
	matriceIdentity = identity(nbrEle) # on cree la matrice identite tout des 1 en diagonale
	matrixIA        = matriceIdentity - matriceA  # soustraction de la matrice A de l'identite
	matriceL        = inv(matrixIA)  # on inverse la matrice IA pour obtenir la matrice de Leontief
	mmult           = dot(mVector,matriceL)#on multiplie le vectorM par la matriceL
	#mmult           = matriceL.dot(mVector)
	#diagM           = diag( mmult,k=0) #on diagonalise le resultat 
	colP1           = dicRealP1[keyP1]['P1']
	colP6           = dicRealP1[keyP1]['P6']
	#la fonction fait un vecteur avec TOUTES les colonnes 
	#MAIS on ne CONSERVE QUE LES VALEURS DE P6 (exportation)     
	colExport       = libMatrix.vectorCol(colP1,colP6) 
	xVector         = libMatrix.createExportVector(colExport)
	fileDetail      = open(dirOutput + '\\matrixMContXDetail_' + str(keyP1) +IndOrPrd+'.csv', 'w')    
	try:
		mContX		= dot(mmult,xVector)
	except:
		fileLog.write('dimension matrice '+str(keyP1)+' len matrice : '+nbrEle+'\n') 
		mContX		= 0
	totExportVector = sum(xVector)
	mContXPercent   = (mContX/totExportVector) * 100
	#print keyP1, '; mContX=', mContX, '; Total Export Vector=',totExportVector, '; mContXPercent=', mContXPercent
	ligne =  str(keyP1)+';'+str(mContX)+';'+str(totExportVector)+';'+str(mContXPercent)
	fileMatrice.write(ligne+'\n')
	#fichier globale des matrices
	lstKeyP1          = keyP1.split("#")
	codeCountry       = lstKeyP1[0]
	yyyy              = lstKeyP1[1]         
	ligne             = 'New;Import contents of exports for ;mcontx;'+str(codeCountry)+';'+str(yyyy)+'\n'
	fileOutput.write(ligne)
	fileMatriceDB.write(ligne)
	ligne             = 'Code;default\n'
	fileMatriceDB.write(ligne)
	ligne =  'default;'+str(mContXPercent)
	fileMatriceDB.write(ligne+'\n')
            
	fileDetail.write(str(keyP1)+ ' Matrix Leontief '+'\n')
	#ligne titre avec les codes produits
	ligne   = 'Code;'
	l       = 0
	tabCode = []
	dicRealP1[keyP1]['P1'].sort()
	for n in dicRealP1[keyP1]['P1']:
		codeProd    = n.split("#")
		ligne       = ligne+str(codeProd[0])+","
		tabCode.append(codeProd[0])
	fileDetail.write(ligne[0:-1]+'\n')
	fileOutput.write(ligne[0:-1]+'\n')
	#corps de la matrice    
	ligne = ''    
	for l in range(0,nbrEle):
		ligne=tabCode[l]+';'
	for c in range(0,nbrEle):  
		ligne   = ligne+str(matriceL[l,c])+","      
	fileDetail.write(ligne[0:-1]+'\n')
	fileOutput.write(ligne[0:-1]+'\n')        
	#ligne multiplicateurs            
	ligne = 'mVector;'
	for i in range(0,len(mVector)):
		try:
			mVecteur  = mVector[i]
		except:
			mVecteur  = '0.0'
		ligne   = ligne+str(mVecteur)+","
	fileDetail.write(ligne[0:-1]+'\n')
	fileOutput.write(ligne[0:-1]+'\n')
    
	ligne = 'xVector;'
	for i in range(0,len(xVector)):
		try:
			xVecteur  = xVector[i]
		except:
			xVecteur  = '0.0'
		ligne   = ligne+str(xVecteur)+","
	fileDetail.write(ligne[0:-1]+'\n')
	fileOutput.write(ligne[0:-1]+'\n')  
                   
	ligne = 'mmultmcontx;'
	#corps de la matrice calcul en pourcent des importations provoquees par les exportations par produit
	#quel sont les produits que l'on doit importer quand on exporte un produit
	for i in range(0,len(dicRealP1[keyP1]['P1'])):
		try:
			importOFExportProd  = mmult[i]*100
		except:
			importOFExportProd  = 0
		ligne   = ligne+str(importOFExportProd)+","
	fileDetail.write(ligne[0:-1]+'\n')
	fileOutput.write(ligne[0:-1]+'\n')
        
	#ligne = str(mContXPercent)
                        
def traitementMatrice(dicRealP1, dicMatrice, dicNoProduct):
	codeP1        = list(dicRealP1.keys())
	codeP1.sort()
	mVector       = []
	for keyP1 in codeP1: #key = country,year
		nbrEleP1      = len(dicRealP1[keyP1]['P1'])
		matriceA      = zeros((nbrEleP1,nbrEleP1), dtype=float)
		ligne         = 0
		col           = 0
		dicRealP1[keyP1]['P1'].sort()
		dicRealP1[keyP1]['P2I'].sort()
		vectorP1      = dicRealP1[keyP1]['P1']
		vectorZero    = libMatrix.fonctionVectorZero(vectorP1)
		mVector       = list(map(libMatrix.divide, dicRealP1[keyP1]['P2I'], dicRealP1[keyP1]['P1']))
		for productLst  in dicRealP1[keyP1]['P1']:#chaque ligne est une liste avec le code produit et la valeur 
			productLst   = productLst.split('#')
			productP1    = productLst[0]
			valueP1      = float(productLst[1])
			keyMatriceP1 = keyP1 + '#' + productP1
			ligne        = 0
			if dicNoProduct.has_key(keyMatriceP1):
				fileLog.write('produit non traite keyMatriceP1='+keyMatriceP1+'\n')                            
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
				ligneAtraiter = libMatrix.vectorAtraiter(vectorMatrice, vectorP1)                                                                        
				ligneAtraiter.sort()                                   
				for ligneMatrice in     ligneAtraiter:  # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE ligne                                                        
					ligneMatrice        = ligneMatrice.split('#')
					product             = ligneMatrice[0]                
					value               = float(ligneMatrice[1])
					keyNoProduct        = keyP1 + "#" + product
					if keyNoProduct in dicNoProduct:
						#fileLog.write('produit non traite keyMatriceP1='+keyMatriceP1+' keyNoProduct='+keyNoProduct+'\n')
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
		traitementMatriceA(keyP1, matriceA, dicRealP1, mVector)
                     
def readFileP2I(dicMatriceP1Row,dicNace):
	fichierInput      = open(fichierP2I,'r')
	rec1er            = fichierInput.readline() #1er rec avec les meta
	recMeta           = rec1er.split(',')
	recGeoTime        = recMeta[4].strip('\n').split('\t')    
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
		if (flow == 'IMP' and unit == 'MIO_EUR' and row == 'TOTAL' and col in dicNace):
			for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
				yy            = recGeoTime[i].strip() #record des metas
				keyGeoYY      = geo + '#' + yy
				value         = col + '#' + ligneGeoTime[i].strip()
				keyProd       = 'P2I'
				if keyGeoYY in dicMatriceP1Row:
					if keyProd in dicMatriceP1Row[keyGeoYY]:
						dicMatriceP1Row[keyGeoYY][keyProd] = dicMatriceP1Row[keyGeoYY][keyProd] + [value]                              
					else:                          
						dicMatriceP1Row[keyGeoYY][keyProd] = [value]
				else:
					dicMatriceP1Row[keyGeoYY] = {} #on cree un nouveau dictionnaire pour le couple valeur, produit par ligne de produit
					dicMatriceP1Row[keyGeoYY][keyProd]     = [value] 
	fichierInput.close()
	return dicMatriceP1Row
	
def traitementFichierCSV():
	dicMatrice        = {}
	dicP1             = {}
	dicMatriceP1Row   = {}
	dicSelectP2I      = {}
	dicP2I            = {}    
	dicRealP1         = {}
	dicGeo            = {}
	dicNoProduct      = {}
	dicNace		      = {}
	#dicNace		  =	DBAccess.dicNace('nace2','NAMA','0')
	dicNace			  =	FileAccessMatrix.dicNace(fileNaceInput,dirTXT)	
	fichierInput      = open(fichierCSV,'r')
	rec1er            = fichierInput.readline() #1er rec avec les meta
	recMeta           = rec1er.split(',')
	recGeoTime        = recMeta[4].strip('\n').split('\t')
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
		dicGeo[geo]     = geo        
		if  (flow == 'DOM' and unit == 'MIO_EUR'):
			#on  met chaque ligne de produits dans un dictionnnaire
			if	col in dicNace and row in dicNace: #pas prendre cpa_total
				for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
					yy            = recGeoTime[i].strip() #record des metas 
					keyMatrice    = geo + '#' + yy + '#' + col
					value         = row + '#' + ligneGeoTime[i].strip()
					if keyMatrice in dicMatrice:  # ATTENTION CHAQUE LIGNE CORRESPOND AUX ELEMENTS D'UNE COLONNE
						dicMatrice[keyMatrice]  = dicMatrice[keyMatrice] + [value]
					else:
						dicMatrice[keyMatrice]  = [value]
			if (row == 'P1') and (col in dicNace):
				for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
					yy            = recGeoTime[i].strip() #record des metas
					keyGeoYY      = geo + '#' + yy                    
					value         = col + '#' + ligneGeoTime[i].strip()
					keyProd       = row
					if keyGeoYY in dicMatriceP1Row:
						if keyProd in dicMatriceP1Row[keyGeoYY]:
							dicMatriceP1Row[keyGeoYY][keyProd] = dicMatriceP1Row[keyGeoYY][keyProd] + [value]                              
						else:                          
							dicMatriceP1Row[keyGeoYY][keyProd] = [value]
					else:
						dicMatriceP1Row[keyGeoYY] = {} #on cree un nouveau dictionnaire pour le couple valeur, produit par ligne de produit
						dicMatriceP1Row[keyGeoYY][keyProd] = [value]
			#pour le vecteur P6 des exportations
			if (col == 'P6') and (row in dicNace):  # pas prendre cpa_total
				for i in  range(1,len(recGeoTime)): #record des metas, on boucle sur les annees
					yy            = recGeoTime[i].strip() #record des metas
					keyGeoYY      = geo + '#' + yy
					value         = row + '#' + ligneGeoTime[i].strip()
					keyProd       = col
					if keyGeoYY in dicMatriceP1Row:
						if keyProd in dicMatriceP1Row[keyGeoYY]:
							dicMatriceP1Row[keyGeoYY][keyProd] = dicMatriceP1Row[keyGeoYY][keyProd] + [value]                              
						else:                          
							dicMatriceP1Row[keyGeoYY][keyProd] = [value]
					else:
						dicMatriceP1Row[keyGeoYY] = {} #on cree un nouveau dictionnaire pour le couple valeur, produit par ligne de produit
						dicMatriceP1Row[keyGeoYY][keyProd]     = [value]
                                                                                                                                                                              
	fichierInput.close()
	#on complete le dictionnaire P1 avec la partie P2I qui vient des IMPORTATIONS    
	dicMatriceP1Row = readFileP2I(dicMatriceP1Row,dicNace)
	dicKeyP1Row     = list(dicMatriceP1Row.keys())
	dicKeyP1Row.sort() 
	#SELECTION DES MATRICES A TRAITER                                         
	for keyP1 in dicKeyP1Row: #key = country,year
		matriceVide      = 1  # on considere que la matrice est vide au depart
		L68_test         = 0
		entryL68P2I      = 'CPA_L68#0'
		entryL68AP2I     = 'CPA_L68A#0' 
		entryL68BP2I     = 'CPA_L68B#0'
		entryL68P1       = 'CPA_L68#0'
		entryL68AP1      = 'CPA_L68A#0' 
		entryL68BP1      = 'CPA_L68B#0'
		entryL68P6       = 'CPA_L68#0'
		entryL68AP6      = 'CPA_L68A#0' 
		entryL68BP6      = 'CPA_L68B#0'                
		#on s'assure que la liste P1 est dans le bon ordre        
		keyRow           = 'P1'
		try:
			dicMatriceP1Row[keyP1][keyRow]
			dicRealP1[keyP1] = {} # dictionnaire avec les matrices P1 a traiter                    
			dicRealP1[keyP1][keyRow] = []
		except:
			fileLog.write('delete de '+keyP1+' pas de P1\n')
			del dicMatriceP1Row[keyP1]
			continue
		for productLst  in dicMatriceP1Row[keyP1][keyRow]:#chaque ligne est une liste avec le code produit et la valeur 
			productLst   = productLst.split('#')
			product      = productLst[0]
			value        = productLst[1]
			if  (value != '0.0')and(value != '0'):
				matriceVide         = 0    #la matrice ne sera pas vide,il y a au moins une col de remplie
				if (product == CPA_L68):
					entryL68P1      = product + '#' + value                 
					continue
				if (product == CPA_L68A):
					entryL68AP1     = product + '#' + value                 
					continue 
				if (product == CPA_L68B):
					entryL68BP1     = product + '#' + value                 
					continue
				entryP1                         = product + '#' + value
				dicRealP1[keyP1][keyRow]        = dicRealP1[keyP1][keyRow] + [entryP1]                
			else:
				if  (matriceVide == 0): #si la matrice n'est pas vide alors on enleve les col/row qui n'ont pas de valeur
										#on fait le test pour eviter que le logfile soit aussi rempli avec toutes les col
										#vide d'une matrice vide
					keyNoProduct               = keyP1 + "#" + product 
					dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
					fileLog.write('Colonne vide pour matrice = ' + keyNoProduct +' keyRow='+keyRow +'\n')
                    
		keyRow           = 'P6'
		dicMatriceP1Row[keyP1][keyRow].sort()#on tri la liste des produits P6 
		dicRealP1[keyP1][keyRow] = []

		for productLst  in dicMatriceP1Row[keyP1][keyRow]:#chaque ligne est une liste avec le code produit et la valeur 
			productLst   = productLst.split('#')
			product      = productLst[0]
			value        = productLst[1]
			if  (value != '0.0')and(value != '0'):
				matriceVide         = 0    #la matrice ne sera pas vide,il y a au moins une col de remplie
				if (product == CPA_L68):
					entryL68P6        = product + '#' + value                 
					continue
				if (product == CPA_L68A):
					entryL68AP6       = product + '#' + value                 
					continue 
				if (product == CPA_L68B):
					entryL68BP6       = product + '#' + value                 
					continue
				entryP1                         = product + '#' + value
				dicRealP1[keyP1][keyRow]        = dicRealP1[keyP1][keyRow] + [entryP1]                
		#-----------------------------FAIRE CE TEST POUR LE P1 et pas P2I----------------                                 
		#on traite les matrices uniquement pour celles qui ont une ligne P2I                           
		keyRow           = 'P2I'
		dicMatriceP1Row[keyP1][keyRow].sort()             
		dicRealP1[keyP1][keyRow] = []
		for productLst  in dicMatriceP1Row[keyP1][keyRow]:#chaque ligne est une liste avec le code produit et la valeur 
			productLst   = productLst.split('#')
			product      = productLst[0]
			value        = productLst[1]
			if  (value != '0.0')and(value != '0'):    
				if (product == CPA_L68): 
					L68_test        = 100
					entryL68P2I     = product + '#' + value
					continue
				if (product == CPA_L68A): 
					L68_test        = L68_test + 10
					entryL68AP2I    = product + '#' + value
					continue 
				if (product == CPA_L68B): 
					L68_test        = L68_test + 1
					entryL68BP2I    = product + '#' + value
					continue
				entryP1                        = product + '#' + value
				dicRealP1[keyP1][keyRow]        = dicRealP1[keyP1][keyRow] + [entryP1]                
			else:
				if  (matriceVide == 0): #si la matrice n'est pas vide alors on enleve les col/row qui n'ont pas de valeur
										#on fait le test pour eviter que le logfile soit aussi rempli avec toutes les col
										#vide d'une matrice vide
					keyNoProduct               = keyP1 + "#" + product 
					dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
					fileLog.write('Colonne vide pour matrice = ' + keyNoProduct +' keyRow='+keyRow +'\n')                                         
		#traitement des cas de L68
		if  (L68_test == 111):
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68AP1] + [entryL68BP1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68AP6] + [entryL68BP6]
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68AP2I] + [entryL68BP2I]             
			keyNoProduct               = keyP1 + "#"+CPA_L68 
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
			fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')                                  
		if  (L68_test == 110):
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68P1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68P6]           
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68P2I]  
			keyNoProduct               = keyP1 + "#"+CPA_L68A
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
			fileLog.write('Colonne CPA_L68A enleve pour matrice = ' + keyP1 +'\n')            
		if  (L68_test == 101):
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68BP1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68BP6]            
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68BP2I]        
			keyNoProduct               = keyP1 + "#"+CPA_L68
			dicNoProduct[keyNoProduct] = product #on ne va pas traiter la ligne avec la valeur zero                                       
			fileLog.write('Colonne CPA_L68 enleve pour matrice = ' + keyP1 +'\n')
		if  (L68_test == 100):                             
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68P1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68P6]           
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68P2I]                        
		if  (L68_test == 11):
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68AP1] + [entryL68BP1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68AP6] + [entryL68BP6]            
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68AP2I] + [entryL68BP2I]          
		if  (L68_test == 10):
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68AP1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68AP6]          
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68AP2I]             
		if  (L68_test == 1):
			dicRealP1[keyP1]['P1']     = dicRealP1[keyP1]['P1']  + [entryL68BP1]
			dicRealP1[keyP1]['P6']     = dicRealP1[keyP1]['P6']  + [entryL68BP6]            
			dicRealP1[keyP1]['P2I']    = dicRealP1[keyP1]['P2I'] + [entryL68BP2I]                                                                
		if  (matriceVide): #la matrice est vide si toute les valeurs de P1 sont vides
			matriceVide   = 0
			del dicRealP1[keyP1] #on supprime les reference inutiles aux matrices vide partie P2I     
			fileLog.write('Matrice Vide = ' + keyP1 + '\n')                   
	#TRAITEMENT DES MATRICES
	traitementMatrice(dicRealP1, dicMatrice, dicNoProduct)
  
traitementFichierCSV()
fileMatrice.close()
fileOutput.close()
fileLog.close()             