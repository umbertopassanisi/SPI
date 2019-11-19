from decimal import *
	
#liste pour la selection des code nace qui serviront pour le calcul des totaux
def defSelectLstTotal(nomenclature,compte,fileExt=''):
	if	nomenclature		==	'nace1':
		if	compte			==	'nama':#compte nationaux	
			lstTotal		= 	('G-I','J_K','L-P')		
		elif compte			==	'sbs':#compte structurel						
			lstTotal		= 	('C','D','E','F','G','H','I','K')		 
		elif compte			==	'bd':#compte BD - business data
			lstTotal		= 	('G','H','I','J','K_X_K7415')
	elif nomenclature		==	'nace2':#nace2
		if	compte			==	'nama':#compte nationaux	
			lstTotal	= 	('C17','C18','C20','C21','C26','C27','G-I','J','K','L','M_N','O-Q','R','S','T')
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
def defTotalNace(dicTotalNace='',indicatorSpi='',nace='',nomenclature='',country='',compte='',vector='',lstTotal='',size='',fileExt=''):
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
			if	('C17','C18').count(nace):
				keyNaceTotal 	=	'C17_C18'+ size
				dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if	('C20','C21').count(nace):
				keyNaceTotal 	=	'C20_C21'+ size
				dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if	('C26','C27').count(nace):
				keyNaceTotal 	=	'C26_C27'+ size
				dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if	('G-I','J','K','L','M_N').count(nace):
				keyNaceTotal 	=	'G-N'+ size
				dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
			if	('G-I','J','K','L','M_N','O-Q','R','S','T').count(nace):					
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
def defTotalNaceE(dicTotalNace='',nace='',country='',vector='',size=''):
	if		('C17','C18').count(nace):
			keyNaceTotal 	=	'C17_C18'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('C20','C21').count(nace):
			keyNaceTotal 	=	'C20_C21'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('C26','C27').count(nace):
			keyNaceTotal 	=	'C26_C27'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)		
	if		('B','C','D','E').count(nace):
			keyNaceTotal 	=	'B-E'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('G','H','I').count(nace):
			keyNaceTotal 	=	'G-I'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('M','N').count(nace):
			keyNaceTotal 	=	'M_N'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('O','P','Q').count(nace):
			keyNaceTotal 	=	'O-Q'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('R','S','T','U').count(nace):
			keyNaceTotal 	=	'R-U'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('G','H','I','J','K','L','M','N').count(nace):
			keyNaceTotal 	=	'G-N'+ size
			dicTotalNace = defCalTotalNace(dicTotalNace,country,keyNaceTotal,vector)
	if		('G','H','I','J','K','L','M','N','O','P','Q','R','S','T').count(nace):
			keyNaceTotal 	=	'G-T'+ size
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
		dicTotalNace[country][keyNaceTotal]	= {}
		for v in range(0,nbrEle):
			dicTotalNace[country][keyNaceTotal][v]	=	vector[v]
	return	dicTotalNace
  
def defDicSkillTech(nomenclature, dicAggr):
	dicAggr['tech']			= {}
	dicAggr['skill']		= {}
		
	if nomenclature == 'nace1' :
		
		dicAggr['tech']['ht']   = ('DL30','DL32','DL33')
		dicAggr['tech']['mht']  = ('DG','DK','DL31','DM34','DM35')
		dicAggr['tech']['mlt']  = ('DF','DH','DI','DJ')
		dicAggr['tech']['ml']   = ('DA','DB','DC','DD','DE','DN')
		dicAggr['tech']['kis']  = ('I61','I62','I64','J','K','M','N','O92')
		dicAggr['tech']['lkis'] = ('G','H','I60','I63','L','O90','O91','O93','P','Q')
		
		dicAggr['skill']['hs']  = ('DF','DG','DL30','DL32','J','K70','K72','K73','K74','L','M')
		dicAggr['skill']['his'] = ('DL33','DM35','E','I62','I63','I64','K71','N')
		dicAggr['skill']['lis'] = ('DD','DE','DJ28','DK','DL31','F','G','I60','I61')
		dicAggr['skill']['ls']  = ('A','B','C','DA','DB','DC','DH','DI','DJ27','DM34','DN','H','O')
		
	elif nomenclature == 'nace2' :
		
		dicAggr['tech']['ht']   = ('C21','C26')
		dicAggr['tech']['mht']  = ('C20','C27','C28','C29','C30')
		dicAggr['tech']['mlt']  = ('C19','C22','C23','C24','C25','C33')
		dicAggr['tech']['ml']   = ('C10-C12','C13-C15','C16','C17','C18','C31_C32')
		dicAggr['tech']['kis']  = ('H50','H51','J58','J59_J60','J61','J62_J63','K64','K65','K66','M69_M70','M71','M72','M73','M74_M75','N78','N80','O','P','Q86','Q87_Q88','R90-R92','R93')
		dicAggr['tech']['lkis'] = ('G45','G46','G47','H49','H52','H53','I','L','N77','N79','N81','N82','S94','S95','S96','T','U')
		
		dicAggr['skill']['hs']  = ('C19','C20','C21','C26','J58','J62_J63','K64','K65','K66','L','M69_M70','M71','M72','M73','M74_M75','N78','N80-N82','O','P')
		dicAggr['skill']['his'] = ('C30','D','E36','H51','H52','H53','J61','N77','Q86','Q87_Q88')
		dicAggr['skill']['lis'] = ('C16','C17','C18','C25','C27','C28','C33','F','G45','G46','G47','H49','H50')
		dicAggr['skill']['ls']  = ('A01','A02','A03','B','C10-C12','C13-C15','C22','C23','C24','C29','C31_C32','E37-E39','I','J59_J60','N79','R90-R92','R93','S94','S95','S96')
	
	return dicAggr
  
def defDicNaceAggregates(nomenclature, account):
	dicAggr = {}
	
	if nomenclature == 'nace1' :
		if account == 'nama' :
			dicAggr['G-K'] 			= ['G-I', 'J_K']
			dicAggr['G-P'] 			= ['G-I', 'J_K', 'L-P']
		elif account == 'sbs' :
			dicAggr['C-E'] 			= ['C', 'D', 'E']
			dicAggr['G-I'] 			= ['G', 'H', 'I']
			dicAggr['C-K_X_J'] 		= ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'K']
	elif nomenclature == 'nace2' :
		if account == 'nama' :
			dicAggr['C17_C18'] 		= ['C17', 'C18']
			dicAggr['C20_C21'] 		= ['C20', 'C21']
			dicAggr['C26_C27'] 		= ['C26', 'C27']
			dicAggr['G-N'] 			= ['G-I', 'J', 'K', 'L', 'M_N']
			dicAggr['G-T'] 			= ['G-I','J','K','L','M_N','O-Q','R','S','T']
		elif account == 'sbs' :
			dicAggr['B-E']          = ['B','C','D','E']
			dicAggr['C10-C12'] 		= ['C10','C11','C12']
			dicAggr['C13-C15'] 		= ['C13','C14','C15']
			dicAggr['C16-C18'] 		= ['C16','C17','C18']
			dicAggr['C17_C18'] 		= ['C17', 'C18']
			dicAggr['C20_C21'] 		= ['C20', 'C21']
			dicAggr['C22_C23'] 		= ['C22','C23']
			dicAggr['C24_C25'] 		= ['C24','C25']
			dicAggr['C26_C27'] 		= ['C26', 'C27']
			dicAggr['C29_C30'] 		= ['C29','C30']
			dicAggr['C31_C32'] 		= ['C31','C32']
			dicAggr['C31-C33'] 		= ['C31','C32','C33']
			dicAggr['E37-E39'] 		= ['E37','E38','E39']
			dicAggr['G-I'] 			= ['G','H','I']
			dicAggr['J58-J60'] 		= ['J58','J59','J60']
			dicAggr['J59_J60'] 		= ['J59','J60']
			dicAggr['J62_J63'] 		= ['J62','J63']
			dicAggr['M_N'] 			= ['M','N']
			dicAggr['M69_M70'] 		= ['M69','M70']
			dicAggr['M69-M71'] 		= ['M69','M70','M71']
			dicAggr['M73-M75'] 		= ['M73','M74','M75']
			dicAggr['M74_M75'] 		= ['M74','M75']
			dicAggr['N80-N82'] 		= ['N80','N81','N82']
			dicAggr['B-N_X_K'] 		= ['B','C','D','E','F','G','H','I','J','L','M','N']
			dicAggr['B-N_S95_X_K'] 	= ['B','C','D','E','F','G','H','I','J','L','M','N','S95']
	elif nomenclature == 'cpa2002':
		if account == 'manufacturing':
			dicAggr['TOTAL']		= ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
		elif account == 'comext':
			dicAggr['D']            = ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
			dicAggr['DA']           = ['15', '16']
			dicAggr['DB']           = ['17', '18']
			dicAggr['DC']           = ['19']
			dicAggr['DD']           = ['20']
			dicAggr['DE']           = ['21', '22']
			dicAggr['DF']           = ['23']
			dicAggr['DG']           = ['24']
			dicAggr['DH']           = ['25']
			dicAggr['DI']           = ['26']
			dicAggr['DJ']           = ['27', '28']
			dicAggr['DK']           = ['29']
			dicAggr['DL']           = ['30', '31', '32', '33']
			dicAggr['DM']           = ['34', '35']
			dicAggr['DN']           = ['36', '37']
	elif nomenclature == 'cpa2008':
		if account == 'manufacturing':
			dicAggr['TOTAL']		= ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
		elif account == 'comext':
			dicAggr['C']            = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
			dicAggr['CA']           = ['10', '11', '12']
			dicAggr['CB']           = ['13', '14', '15']
			dicAggr['CC']           = ['16', '17', '18']
			dicAggr['CD']           = ['19']
			dicAggr['CE']           = ['20']
			dicAggr['CF']           = ['21']
			dicAggr['CG']           = ['22', '23']
			dicAggr['CH']           = ['24', '25']
			dicAggr['CI']           = ['26']
			dicAggr['CJ']           = ['27']
			dicAggr['CK']           = ['28']
			dicAggr['CL']           = ['29', '30']
			dicAggr['CM']           = ['31', '32']
	elif nomenclature == 'bec':
		if account == 'manufacturing':
			dicAggr['TOTAL']		= ['111', '112', '121', '122', '21', '22', '31', '321', '322', '41', '42', '51', '521', '522', '53', '61', '62', '63', '7']
		elif account == 'comext':
			dicAggr['1']            = ['111', '112', '121', '122']
			dicAggr['11']           = ['111', '112']
			dicAggr['12']           = ['121', '122']
			dicAggr['2']            = ['21', '22']
			dicAggr['3']            = ['31', '321', '322']
			dicAggr['32']           = ['321', '322']
			dicAggr['4']            = ['41', '42']
			dicAggr['5']            = ['51', '521', '522', '53']
			dicAggr['52']           = ['521', '522']
			dicAggr['6']            = ['61', '62', '63']

	return dicAggr
  
def calcNaceAggregates(dicIndicator, nomenclature, account):
	dicAggr = defDicNaceAggregates(nomenclature, account)

	for country in dicIndicator :
		for aggr in dicAggr :
			res = []
			for nace in dicAggr[aggr] :
				try :
					ref = dicIndicator[country][nace]
				except :
					res = []
					break
				if len(res) == 0 :
					for i in range(0, len(ref)) :
						res.append(ref[i].split(';')[0])
				else :
					for i in range(0, len(ref)) :
						if res[i] == ':' or ref[i].split(';')[0] == ':' :
							res[i] = ':'
						else :
							res[i] = str(float(res[i]) + float(ref[i].split(';')[0]))
			if len(res) > 0 :
				dicIndicator[country][aggr] = res
	
	return dicIndicator

def calcNaceAggregatesPartner(dicIndicator, nomenclature, account):
	dicAggr = defDicNaceAggregates(nomenclature, account)

	for country in dicIndicator :
		for aggr in dicAggr :
			res = {}
			for nace in dicAggr[aggr] :
				try :
					ref_nace = dicIndicator[country][nace]
				except :
					res = {}
					break
				for partner in ref_nace:
					try:
						ref = dicIndicator[country][nace][partner]
					except:
						res[partner] = []
						continue;
					try:
						if len(res[partner]) > 0 :
							for i in range(0, len(ref)) :
								if res[partner][i] == ':' or ref[i].split(';')[0] == ':' :
									res[partner][i] = ':'
								else :
									res[partner][i] = '{0:.0f}'.format(float(res[partner][i]) + float(ref[i].split(';')[0]))
					except:
						res[partner] = []
						for i in range(0, len(ref)) :
							res[partner].append(ref[i].split(';')[0])
			for partner in res:
				if len(res[partner]) > 0 :
					try :
						dicIndicator[country][aggr][partner] = res[partner]
					except :
						dicIndicator[country][aggr] = {}
						dicIndicator[country][aggr][partner] = res[partner]
	return dicIndicator
  
def createSkillTechNace2SbsTotal(dicIndicator):
	for country in dicIndicator:
		res = []
		for nace in dicIndicator[country]:
			ref = dicIndicator[country][nace]
			if len(res) == 0 :
				for i in range(0, len(ref)) :
					res.append(ref[i])
			else :
				for i in range(0, len(ref)) :
					if res[i] == ':' or ref[i].split(';')[0] == ':' :
						res[i] = ':'
					else :
						res[i] = str(float(res[i]) + float(ref[i]))
						
		if len(res) > 0 :
			dicIndicator[country]['N80-N82'] = res
	
	return dicIndicator

def createSkillTechNace2Ratio(dicIndicator):
	dicRatio = {}
	for country in dicIndicator:
		dicRatio[country] = {}
		for nace in('N80', 'N81', 'N82'):
			dicRatio[country][nace] = []
			ref = dicIndicator[country]['N80-N82']
			for i in range(0,len(ref)) :
				val = dicIndicator[country][nace][i]
				if val == ':' or ref[i] == ':' :
					dicRatio[country][nace].append(':')
				else :
					dicRatio[country][nace].append(str(float(val)/float(ref[i])))
	
	return dicRatio
  
def addSkillTechNace2RemainingCodes(dicIndicator, dicRatio):
	for country in dicRatio:
		try:
			ref = dicIndicator[country]['N80-N82']
		except:
			continue
		for nace in dicRatio[country]:
			res = []
			ratio = dicRatio[country][nace]
			for i in range(0,len(ref)) :
				if ratio[i] == ':' or ref[i] == ':':
					res.append(':')
				else:
					res.append(str(float(ref[i])*float(ratio[i])))
			dicIndicator[country][nace] = res
	return dicIndicator

def createDicNace2EmpAggr():
	dicAggr = {}
	
	dicAggr['B-E'] = ['B', 'C', 'D', 'E']
	dicAggr['G-I'] = ['G', 'H', 'I']
	dicAggr['M_N'] = ['M', 'N']
	dicAggr['O-Q'] = ['O', 'P', 'Q']
	dicAggr['R-U'] = ['R', 'S', 'T', 'U']
	
	return dicAggr

def calcNace2EmpAggr(dicIndicator):
	dicAggr = createDicNace2EmpAggr()
	
	for country in dicIndicator :
		for aggr in dicAggr :
			res = []
			for nace in dicAggr[aggr] :
				try :
					ref = dicIndicator[country][nace]
				except :
					res = []
					break
				if len(res) == 0 :
					for i in range(0, len(ref)) :
						res.append(ref[i].split(';')[0])
				else :
					for i in range(0, len(ref)) :
						if res[i] == ':' or ref[i].split(';')[0] == ':' :
							res[i] = ':'
						else :
							res[i] = str(float(res[i]) + float(ref[i].split(';')[0]))
			if len(res) > 0 :
				dicIndicator[country][aggr] = res
	
	return dicIndicator