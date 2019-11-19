#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#SPI
#lecture des fichiers XML UN pour les BEC
#
#ON ECRIT LA SORTIE DANS ..\output\comtrade\tradeingoods.txt
#ramiro DG Ecfin : 15/09/2014

import sys
import glob
import os
import spiLib
import spiLibTrade
import FileAccess
import XmlAccess

#parametres application
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 			=  sys.argv[1]

dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
dirCSV          =  dirUse           +'\\Input\\csv'
fichiersXML     =  glob.glob(dirUse +'\\Input\\xml\\bec\\*.xml')
fileLog         =  open(dirLog      +'\\readXmlUnBec.log', 'w')
fileOutput		=  open(dirUse      +'\\Output\\comtrade\\tradeingoodsRCAbec.txt', 'w+')
	
# lecture et traitement fichier xml
def traitementXML(fichiersXml,fileOutput):
	fileOutput.write('0000,0000\n')#1er ligne qui sera remplacee avec les dates min et max	
	dicCodeBEC			= {}
	dicCodeBEC			= FileAccess.lectureBEC(dirCSV)#fichier : BECCodeOnly.csv
	minStartYear        = 99999
	maxEndYear          = -1
	dicWorld			= {}
	#on a deja selectionne les bons pays lors du download
	#cf gethttpUN.py
	for fichierXml in fichiersXml:
		dicXml			=	{}
		dicXml			= 	XmlAccess.lectureXMLBec(fichierXml,dicCodeBEC,fileLog)
		lstfichierXml	=	fichierXml.split('.')
		base			=	os.path.basename(fichierXml)
		country			=	os.path.splitext(base)[0]
		for	rgCode		in 	dicXml:
			codeBECSort	=   dicXml[rgCode].keys()
			try:
				codeBECSort.remove('TOTAL')
			except:
				fileLog.write('no TOTAL for XML file '+fichierXml+'\n')
			codeBECSort.sort()
			for	codeBEC	in	codeBECSort:	
				if	dicWorld.has_key(codeBEC): 
					pass
				else: 
					dicWorld[codeBEC] = {}
				dicTotalYear	=	{}					
				yearSort    	=   dicXml[rgCode][codeBEC].keys()
				yearSort.sort()	
				startYear		=	yearSort[0]
				endYear			=	yearSort[-1]		
				minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear)
				for year in yearSort:
					valYear				= int(dicXml[rgCode][codeBEC][year])
					try:
						dicTotalYear[year]=dicTotalYear[year] + valYear
					except:
						dicTotalYear[year]=valYear					
					try:
						dicWorld[codeBEC][year]=dicWorld[codeBEC][year] + valYear
					except:
						dicWorld[codeBEC][year]=valYear						
				#traitement du total des annees par code BEC
				#le record de sortie par pays
				lstValue  = spiLibTrade.vectorYear(dicTotalYear)
				recordOut =	country+','+codeBEC+','+str(startYear)+','+lstValue+'\n'
				fileOutput.write(recordOut)		
	#traitement world
	codeBECSort	=   dicWorld.keys()
	codeBECSort.sort()
	for	codeBEC	in	codeBECSort:
		keyYear			=	dicWorld[codeBEC].keys()
		keyYear.sort()
		startYear		=	keyYear[0]
		endYear			=	keyYear[-1]		
		minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear)
		lstValue  		= 	spiLibTrade.vectorYear(dicWorld[codeBEC])
		recordOut 		=	'WLD,'+codeBEC+','+startYear+','+lstValue+'\n'
		fileOutput.write(recordOut)		
	#ecriture au debut du fichier des dates min et max
	fileOutput.flush() #on vide le cache
	os.fsync(fileOutput.fileno()) #on force a ecrire sur le disque
	fileOutput.seek(0, 0)#on se positionne sur le 1er caractere de la 1er ligne
	fileOutput.write(str(minStartYear)+','+str(maxEndYear)+'\n')	
#------------------------------------------------------------------------------------

traitementXML(fichiersXML,fileOutput)
fileOutput.close()
fileLog.close()	   