'''
fonction qui fait un seul vecteur avec les deux listes
la liste de reference est la P1 mais les VALEURS sont celle de P6
si des vecteurs existent en P1 et pas en P6 
on rajoute les vecteurs dans la liste de retour avec la valeur ZERO
si des vecteurs existent en P6 et pas en P1 : on IGNORE le code et la valeur
'''
# utiliser dans
# matrixMmultEsa2010.py
# matrixLmultEsa2010.py
# matrixMcontXEsa2010.py
def vectorCol(colP1,colP6):
	lstProdExport	= []
	dicProdP1		= {}
	dicProdP6		= {}
	lineProd		= ''
	for c in (range(0,len(colP1))):
		prod				= colP1[c].split('#')
		dicProdP1[prod[0]]	= '0'
	for c in (range(0,len(colP6))):
		prod				= colP6[c].split('#')
		dicProdP6[prod[0]]	= prod[1]
	codeP1        = dicProdP1.keys()    
	codeP1.sort()
	for keyP1 in codeP1: 
		try:
			lineProd		= keyP1 + '#'+dicProdP6[keyP1]
		except:
			lineProd		= keyP1 + '#0'
		lstProdExport		= lstProdExport + [lineProd]
	return lstProdExport
# utiliser dans
# matrixInpshEsa2010.py
def vectorSetCol(currentLst,setLstCol):
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
# utiliser dans
# matrixInpshEsa2010.py
def addP1(cleMatriceP1, currentValue, oldValue):
	vecAdd  = []
	lstProdX        = currentValue
	lstProdY        = oldValue
	lstProdX.sort()
	lstProdY.sort()
	for p in range(0,len(lstProdX)):
		X			= lstProdX[p]
		x			= X.split('#')
		produitX	= x[0]
		try:
			xf		= float(x[1])
		except:
			print 'no num',cleMatriceP1,x[1]
			xf		= 0
		Y			= lstProdY[p]
		y			= Y.split('#')
		try:
			yf		= float(y[1])
		except:
			print 'no num',cleMatriceP1,x[1]
			yf		= 0
		produitY	= y[0]
		if  (produitX != produitY):
			 fileLog.write('catastrophe nom produit different matrice ='+cleMatriceP1+' produitX='+produitX+' produitY='+produitY+'\n')            
		totAdd		= xf+yf
		eleVec		= produitX+'#'+str(totAdd)
		vecAdd		= vecAdd + [eleVec]
	return vecAdd
# utiliser dans
# matrixInpshEsa2010.py 
# matrixOmultEsa2010.py
# matrixVamultEsa2010.py
# matrixMmultEsa2010.py
# matrixLmultEsa2010.py
# matrixMcontXEsa2010.py
def fonctionVectorZero(vectorP1):
	vectorInput  = vectorP1    
	vectorOutput = []
	for c in (range(0,len(vectorInput))):
		productLst   = vectorInput[c].split('#')
		productOuput = productLst[0] + '#0'
		vectorOutput = vectorOutput + [productOuput]
	return vectorOutput
# utiliser dans
# matrixOmultEsa2010.py
# matrixVamultEsa2010.py
# matrixMmultEsa2010.py
# matrixLmultEsa2010.py
# matrixMcontXEsa2010.py
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
#utiliser dans
#matrixVamultEsa2010.py
#matrixMmultEsa2010.py
#matrixLmultEsa2010.py
#matrixMcontXEsa2010.py
def divide(x, y):
	if  (x == None):
		x=0
	else:
		x = x.split('#')
		xf= float(x[1])
		p = x[0]
	if  (y == None):
		y=0
	else:
		y = y.split('#')
		yf= float(y[1])
		p = y[0]
	try:    
		tot=xf/yf
	except:
		tot=0
	valR = p+'#'+str(tot) 
	valR = tot    
	return valR	
#utiliser dans
#matrixMcontXEsa2010.py
def createExportVector(colExport):
	colExport.sort()
	vectorOutput = []
	for p in range(0,len(colExport)):
		prodLst      =  colExport[p].split('#')
		value        =  float(prodLst[1])
		vectorOutput =  vectorOutput + [value]
	return vectorOutput
#utiliser dans
#matrixLmultEsa2010.py
def ligneProc(code,ligneInput):
	tabCode = []
	ligne =	code
	for n in ligneInput:
		codeProd    = n.split("#")
		ligne       = ligne+str(codeProd[1])+","
		tabCode.append(codeProd[0])       
	return ligne[0:-1]