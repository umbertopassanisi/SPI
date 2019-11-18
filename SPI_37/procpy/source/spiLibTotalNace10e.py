from decimal import *

#liste pour la selection des code nace qui serviront pour le calcul des totaux
def defSelectLstTotal(nomenclature,compte):
	if	nomenclature==		'nace1':
		if	compte			==	'nama':#compte nationaux	
			lstTotal		= 	('G-I','J_K','L-P')		
		elif compte			==	'sbs':#compte structurel						
			lstTotal		= 	('C','D','E','F','G','H','I','K')		 
		elif compte			==	'bd':#compte BD - business data
			lstTotal		= 	('G','H','I','J','K_X_K7415')
	elif nomenclature		==	'nace2':#nace2
		if	compte			==	'nama':#compte nationaux	
			lstTotal		= 	('C17','C18','C20','C21','C26','C27','G-I','J','K','L','M-N','O-Q','R','S','T')
		elif compte			==	'sbs':#compte structurel	
			lstTotal		= 	('B','C','D','E','F','G','H','I','J','L','M','N','S95',\
			'C10','C11','C12','C13','C14','C15','C16','C17','C18','C20','C21','C22','C23','C24','C25','C26','C27','C29',\
			'C30','C31','C32','C33','E37','E38','E39','J58','J59','J60','J62','J63','M69','M70','M71','M73',\
			'M74','M75','N80','N81','N82')
		elif compte			==	'bd':#compte BD - business data
			lstTotal		= 	('G','H','I','M','N',\
			'C13_C14','C15','C16','C17_C18','C22','C23','K_X_K7415',\
			'C31_C32','C33','J58','J59','J60','J62','J63','M69','M70','M71','M73',\
			'M74','M75','N80','N81','N82','Q87','Q88','R90','R91','R92')		
	return	lstTotal
	
#calcul du total des codes naces 
#on cree la cle et ensuite on agrege
def defTotalNace(dicTotalNace='',indicatorSpi='',nace='',nomenclature='',country='',compte='',vector='',lstTotal='',size=''):
	if	nomenclature== 'nace1':
		if	compte	== 'nama':
			if		('G-I','J_K').count(nace):
					keyNaceTotal 	=	'G-K'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('G-I','J_K','L-P').count(nace):
					keyNaceTotal 	=	'G-P'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
		elif compte	== 'sbs':#compte structurel
			if		('C','D','E').count(nace):
					keyNaceTotal 	=	'C-E' + size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('G','H','I').count(nace):
					keyNaceTotal 	=	'G-I' + size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C','D','E','F','G','H','I','K').count(nace):
					keyNaceTotal 	=	'C-K_X_J' + size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
		elif compte	== 'bd':#compte BD - business data
			if		('G','H','I').count(nace):
					keyNaceTotal 	=	'G-I' + size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J','K_X_K7415').count(nace):
					keyNaceTotal 	=	'J_K_X_K7415' + size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	elif nomenclature==	'nace2':#nace2
		if	compte	== 'nama':
			if		('C17','C18').count(nace):
					keyNaceTotal 	=	'C17_C18'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C20','C21').count(nace):
					keyNaceTotal 	=	'C20_C21'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C26','C27').count(nace):
					keyNaceTotal 	=	'C26_C27'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)					
			if		('G-I','J','K','L','M-N').count(nace):
					keyNaceTotal 	=	'G-N'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('G-I','J','K','L','M-N','O-Q','R','S','T').count(nace):					
					keyNaceTotal 	=	'G-T'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
		elif compte	==	'sbs':#compte structurel
			if		('B','C','D','E').count(nace):
					keyNaceTotal 	=	'B-E'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C10','C11','C12').count(nace):
					keyNaceTotal 	=	'C10-C12'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C13','C14','C15').count(nace):
					keyNaceTotal 	=	'C13-C15'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C16','C17','C18').count(nace):
					keyNaceTotal 	=	'C16-C18'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C17','C18').count(nace):
					keyNaceTotal 	=	'C17_C18'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C20','C21').count(nace):
					keyNaceTotal 	=	'C20_C21'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)					
			if		('C22','C23').count(nace):
					keyNaceTotal 	=	'C22_C23'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C24','C25').count(nace):
					keyNaceTotal 	=	'C24_C25'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C26','C27').count(nace):
					keyNaceTotal 	=	'C26_C27'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)					
			if		('C29','C30').count(nace):
					keyNaceTotal 	=	'C29_C30'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C31','C32').count(nace):
					keyNaceTotal 	=	'C31_C32'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C31','C32','C33').count(nace):
					keyNaceTotal 	=	'C31-C33'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)		
			if		('E37','E38','E39').count(nace):
					keyNaceTotal 	=	'E37-E39'+ size							
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('G','H','I').count(nace):
					keyNaceTotal 	=	'G-I'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J58','J59','J60').count(nace):
					keyNaceTotal 	=	'J58-J60'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J59','J60').count(nace):
					keyNaceTotal 	=	'J59_J60'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J62','J63').count(nace):
					keyNaceTotal 	=	'J62_J63'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M','N').count(nace):
					keyNaceTotal 	=	'M_N'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M69','M70').count(nace):
					keyNaceTotal 	=	'M69_M70'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M69','M70','M71').count(nace):
					keyNaceTotal 	=	'M69-M71'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M73','M74','M75').count(nace):
					keyNaceTotal 	=	'M73-M75'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M74','M75').count(nace):
					keyNaceTotal 	=	'M74_M75'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('N80','N81','N82').count(nace):
					keyNaceTotal 	=	'N80-N82'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('B','C','D','E','F','G','H','I','J','L','M','N').count(nace):
					keyNaceTotal 	=	'B-N_X_K'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('B','C','D','E','F','G','H','I','J','L','M','N','S95').count(nace):
					keyNaceTotal 	=	'B-N_S95_X_K'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
		elif compte	==	'bd':#compte BD - business data
			if		('C13_C14','C15').count(nace):
					keyNaceTotal 	=	'C13-C15'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C16','C17_C18').count(nace):
					keyNaceTotal 	=	'C16-C18'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C22','C23').count(nace):
					keyNaceTotal 	=	'C22_C23'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('C31_C32','C33').count(nace):
					keyNaceTotal 	=	'C31-C33'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)		
			if		('G','H','I').count(nace):
					keyNaceTotal 	=	'G-I'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J58','J59','J60').count(nace):
					keyNaceTotal 	=	'J58-J60'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J59','J60').count(nace):
					keyNaceTotal 	=	'J59_J60'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('J62','J63').count(nace):
					keyNaceTotal 	=	'J62_J63'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M','N').count(nace):
					keyNaceTotal 	=	'M_N'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M69','M70').count(nace):
					keyNaceTotal 	=	'M69_M70'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M69','M70','M71').count(nace):
					keyNaceTotal 	=	'M69-M71'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M73','M74','M75').count(nace):
					keyNaceTotal 	=	'M73-M75'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('M74','M75').count(nace):
					keyNaceTotal 	=	'M74_M75'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('N80','N81','N82').count(nace):
					keyNaceTotal 	=	'N80-N82'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('Q87','Q88').count(nace):
					keyNaceTotal 	=	'Q87_Q88'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if		('R90','R91','R92').count(nace):
					keyNaceTotal 	=	'R90-R92'+ size
					dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)					
	return	dicTotalNace
	
def defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector):	
	nbrEle			=	len(vector)
	try:
		for v in range(0,nbrEle):
			try:
				dicTotalNace[country][keyNaceTotal][v]	=	dicTotalNace[country][keyNaceTotal][v] + vector[v]
			except:
				dicTotalNace[country][keyNaceTotal][v]	=	':'
	except:
		try:
			dicTotalNace[country][keyNaceTotal] 		= 	[':']*nbrEle
		except:
			dicTotalNace[country]						=	{}
			dicTotalNace[country][keyNaceTotal] 		= 	[':']*nbrEle
		for v in range(0,nbrEle):
			try:
				dicTotalNace[country][keyNaceTotal][v]	=	vector[v]
			except:
				dicTotalNace[country][keyNaceTotal][v]	=	':'
	return	dicTotalNace		
