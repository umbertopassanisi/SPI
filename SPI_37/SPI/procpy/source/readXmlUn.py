#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#SPI
#lecture des fichiers XML UN
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
#parametre cpa2002, cpa2008, BEC
G_typeProduit 	=  sys.argv[1]
Path 			=  sys.argv[2]

G_typeProduit.lower()

dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
dirCSV          =  dirUse           +'\\Input\\csv'
fichiersXML     =  glob.glob(dirUse +'\\Input\\xml\\*.xml')
fileLog         =  open(dirLog      +'\\readXmlUn'+G_typeProduit+'.log', 'w')
fileOutput		=  open(dirUse      +'\\Output\\comtrade\\tradeingoodsRCA'+G_typeProduit+'.txt', 'w+')
	
# lecture et traitement fichier xml
def traitementXML(fichiersXml,G_typeProduit,fileOutput):
	typeProduit		= G_typeProduit #cpa2002 ou cpa2008
	fileOutput.write('0000,0000\n')#1er ligne qui sera remplacee avec les dates min et max	
	dicCodeCPA			= {}
	if	typeProduit		== 'cpa2002':
		dicCodeCPA		= FileAccess.lectureHS1992toCPA2002(dirCSV)#fichier : hs1992tocpa2002ratio.csv
	else:	
		dicCodeCPA		= FileAccess.lectureHS1992toCPA2008(dirCSV,fileLog)#fichier : hs1992tocpa2008un.csv	
	minStartYear        = 99999
	maxEndYear          = -1
	dicWorld			= {}
	dicCountryNoValue	= {}
	#on a deja selectionne les bons pays lors du download
	#cf gethttpUN.py
	for fichierXml in fichiersXml:
		dicXml			=	{}
		dicXml			= 	XmlAccess.lectureXML(fichierXml,dicCodeCPA,fileLog)
		lstfichierXml	=	fichierXml.split('.')
		base			=	os.path.basename(fichierXml)
		country			=	os.path.splitext(base)[0]
		#print country
		paystraiter		=	0
		for	rgCode		in 	dicXml:
			codeCPASort	=   list(dicXml[rgCode].keys())
			codeCPASort.sort()
			for	codeCPA	in	codeCPASort:
				codeHSSort		=  list(dicXml[rgCode][codeCPA].keys())
				codeHSSort.sort()
				dicTotalYearHS	=	{}
				minStartYearHS  = 99999
				maxEndYearHS    = -1				
				if	codeCPA in dicWorld:
					pass #on continue a l'instruction suivante
				else: 
					dicWorld[codeCPA] = {}
				for	codeHS	in	codeHSSort:
					yearSort    =   list(dicXml[rgCode][codeCPA][codeHS].keys())
					yearSort.sort()	
					startYear		=	yearSort[0]
					endYear			=	yearSort[-1]
					#print country, rgCode, codeCPA, codeHS, startYear, endYear, dicXml[rgCode][codeCPA][codeHS]
					minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear)
					minStartYearHS,maxEndYearHS = spiLib.defMinMaxYear(startYear,minStartYearHS,endYear,maxEndYearHS)
					for year in yearSort:
						paystraiter	=	1
						valYear	= int(dicXml[rgCode][codeCPA][codeHS][year]) #la valeur est tj numerique
						try:#la 1er valeur du dic est vide
							dicTotalYearHS[year]=dicTotalYearHS[year] + valYear
						except:#alors on initialise avec la 1er valeur du code HS
							dicTotalYearHS[year]=valYear
						#pour le total WLD si on ne tient pas compte des valeurs inexistantes
						try:
							dicWorld[codeCPA][year]=dicWorld[codeCPA][year] + valYear
						except:
							dicWorld[codeCPA][year]=valYear
						
				#traitement du total des annees par code CPA
				#le record de sortie par pays
				lstValue  = spiLibTrade.vectorYear(dicTotalYearHS)
				recordOut =	country+','+codeCPA+','+str(minStartYearHS)+','+lstValue+'\n'
				fileOutput.write(recordOut)
				#calcul du total WLD, on ne tient plus compte des valeurs inexistantes
				#(on fait le calcul apres la normalisation du vecteur)
				#on va lister uniquement les pays manquants
				lstVector =	lstValue.split('!')
				for i in range(len(lstVector)):
					year 	= minStartYearHS +i
					'''
					try:
						dicWorld[codeCPA][year] = dicWorld[codeCPA][year] + 0
					except:
						dicWorld[codeCPA][year] = 0
					'''
					try:
						valeur					= int(lstVector[i])
						#dicWorld[codeCPA][year] = dicWorld[codeCPA][year] + valeur
					except:#dans ce cas on initialise l'annee avec la valeur
						#dicWorld[codeCPA][year] = ':'
						keyNoValue						=	country  + ',' +codeCPA+ ',' + str(year)
						dicCountryNoValue[keyNoValue]	=	keyNoValue
				
		if	paystraiter == 0:
			recordOut= 'unprocessed country :'+country+'\n'
			fileLog.write(recordOut)

	countryNoValueSort	=   list(dicCountryNoValue.keys())
	countryNoValueSort.sort()
	for countryNoValue in countryNoValueSort:
		recordOut= 'no value for country, cpa, year :'+countryNoValue+'\n'
		fileLog.write(recordOut)
	#traitement world
	codeCPASort	=   list(dicWorld.keys())
	codeCPASort.sort()
	for	codeCPA	in	codeCPASort:
		keyYear			= list(dicWorld[codeCPA].keys())
		keyYear.sort()
		startYear		=	keyYear[0]
		endYear			=	keyYear[-1]		
		#minStartYear,maxEndYear = spiLib.defMinMaxYear(startYear,minStartYear,endYear,maxEndYear)
		lstValue  		= 	spiLibTrade.vectorYear(dicWorld[codeCPA])
		recordOut 		=	'WLD,'+codeCPA+','+str(startYear)+','+lstValue+'\n'
		fileOutput.write(recordOut)
	#ecriture au debut du fichier des dates min et max
	fileOutput.flush() #on vide le cache
	os.fsync(fileOutput.fileno()) #on force a ecrire sur le disque
	fileOutput.seek(0, 0)#on se positionne sur le 1er caractere de la 1er ligne
	fileOutput.write(str(minStartYear)+','+str(maxEndYear)+'\n')	
#------------------------------------------------------------------------------------

traitementXML(fichiersXML,G_typeProduit,fileOutput)
fileOutput.close()
fileLog.close()	   