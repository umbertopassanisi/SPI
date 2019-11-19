from   lxml import etree
from   lxml import objectify
#from   time import localtime, strftime

#lecture fichier XML
#yr,rgCode,rtCode(converti en ISO2),ptCode(converti en ISO2),
#cmdCode(converti en CPA),TradeValue
def lectureXML(fileXML,dicCodeCPA,fileLog):
	dicXml			= {}
	fichierXml		= fileXML
	try:
		treeXml			= objectify.parse(fichierXml)
		print 'ok xml file : ', fichierXml  
	except:
		print 'problem xml file :', fichierXml, ' not read'
		return dicXml
	rootXml			= treeXml.getroot()
	#lecture du fichier XML
	for record in rootXml.iterchildren(tag='r'):
		try:
			yr 			= record.yr.text.strip()
		except:
			fileLog.write('pas de tag yr dans le fichier : '+fichierXml+'\n')
			continue
		try:
			rgCode 		= record.rgCode.text.strip() #2=export
		except:
			fileLog.write('pas de tag rgCode dans le  fichier : '+fichierXml+'\n')
			continue
		try:
			rtCode 		= record.rtCode.text.strip()
		except:
			fileLog.write('pas de tag rtCode dans le  fichier : '+fichierXml+'\n')
			continue
		try:
			ptCode 		= record.ptCode.text.strip()
		except:
			fileLog.write('pas de tag ptCode dans le  fichier : '+fichierXml+'\n')
			continue			
		try:
			cmdCode 	= record.cmdCode.text.strip()
		except:
			fileLog.write('pas de tag cmdCode dans le  fichier : '+fichierXml+'\n')
			continue		
		try:
			TradeValueTxt	= record.TradeValue.text.strip()
			TradeValueFloat	= float(TradeValueTxt)
		except:
			fileLog.write('pas de tag TradeValue dans le  fichier : '+fichierXml+'\n')
			continue
		if	dicCodeCPA.has_key(cmdCode):
			for codeCPA	in dicCodeCPA[cmdCode]:
				ratio		= float(dicCodeCPA[cmdCode][codeCPA])
				TradeValue	= TradeValueFloat * ratio
				try:
					dicXml[rgCode][codeCPA][cmdCode][yr]			= TradeValue		
				except:
					try:
						dicXml[rgCode][codeCPA][cmdCode]			= {}
						dicXml[rgCode][codeCPA][cmdCode][yr]		= TradeValue
					except:
						try:
							dicXml[rgCode][codeCPA]					= {}
							dicXml[rgCode][codeCPA][cmdCode]		= {}
							dicXml[rgCode][codeCPA][cmdCode][yr]	= TradeValue
						except:
								dicXml[rgCode]						= {}
								dicXml[rgCode][codeCPA]				= {}
								dicXml[rgCode][codeCPA][cmdCode]	= {}
								dicXml[rgCode][codeCPA][cmdCode][yr]= TradeValue				
	return dicXml

def lectureXMLBec(fileXML,dicCodeBEC,fileLog):
	fichierXml		= fileXML
	treeXml			= objectify.parse(fichierXml)
	rootXml			= treeXml.getroot()
	dicXml			= {}
	#lecture du fichier XML
	for record in rootXml.iterchildren(tag='r'):
		try:
			yr 			= record.yr.text.strip()
		except:
			fileLog.write('pas de tag yr dans le fichier : '+fichierXml+'\n')
			continue
		try:
			rgCode 		= record.rgCode.text.strip() #2=export
		except:
			fileLog.write('pas de tag rgCode dans le  fichier : '+fichierXml+'\n')
			continue
		try:
			rtCode 		= record.rtCode.text.strip()
		except:
			fileLog.write('pas de tag rtCode dans le  fichier : '+fichierXml+'\n')
			continue
		try:
			ptCode 		= record.ptCode.text.strip()
		except:
			fileLog.write('pas de tag ptCode dans le  fichier : '+fichierXml+'\n')
			continue			
		try:
			cmdCode 	= record.cmdCode.text.strip()
		except:
			fileLog.write('pas de tag cmdCode dans le  fichier : '+fichierXml+'\n')
			continue		
		try:
			TradeValue 	= record.TradeValue.text.strip()
		except:
			fileLog.write('pas de tag TradeValue dans le  fichier : '+fichierXml+'\n')
			continue
		if	dicCodeBEC.has_key(cmdCode):
			codeBEC									= dicCodeBEC[cmdCode]						
			try:
				dicXml[rgCode][codeBEC][yr]			= TradeValue		
			except:
				try:
					dicXml[rgCode][codeBEC]			= {}
					dicXml[rgCode][codeBEC][yr]		= TradeValue
				except:
					dicXml[rgCode]					= {}
					dicXml[rgCode][codeBEC]			= {}
					dicXml[rgCode][codeBEC][yr]		= TradeValue				
	return dicXml	