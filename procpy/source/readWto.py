#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#SPI
#lecture des fichiers XML UN
#
#ON ECRIT LA SORTIE DANS ..\output\comtrade\tradeingoods.txt
#ramiro DG Ecfin : 15/09/2014

import sys
import os
import spiLib
import spiLibTrade
import DBAccess
import FileAccess

#parametres application
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path 			=  sys.argv[1]

dirUse          =  Path	
dirLog          =  dirUse           +'\\Log'
dirTXT          =  dirUse           +'\\Output'
dirCSV          =  dirUse           +'\\Input\\csv'
fileLog         =  open(dirLog      +'\\readWto.log', 'w')
fileOutput		=  open(dirUse      +'\\Output\\wto\\tradeinservice.txt', 'w+')
	
# lecture et traitement fichier xml
def traitement(dirCSV):
	fileOutput.write('0000,0000\n')#1er ligne qui sera remplacee avec les dates min et max	
	dicWto				= {}
	dicNoSector			= {}
	dicSector			= {}	
	dicCountry			= {}
	dicNoCountry		= {}
	dicCountryNoValue	= {}	
	dicCountry			= DBAccess.lectureNationService()
	dicSector			= DBAccess.lectureSectorWto(eurostat=0)#cle est le code WTO, le contenu le code Eurostat
	dicWto,minStartYear,maxEndYear	= FileAccess.lectureFileWto(dirCSV)#on ne prend que les exports
	dicWorld			= {}
	#dicWto : [country][sector][year ] = value
	countrySort			= dicWto.keys()
	countrySort.sort()
	for	countryWto		in 	countrySort:
		sectorWtoSort	=   dicWto[countryWto].keys()
		sectorWtoSort.sort()
		try:
			country		=	dicCountry[countryWto]
			for	sectorWto	in	sectorWtoSort:
				try:
					sector			=	dicSector[sectorWto]
					if	dicWorld.has_key(sector): 
						pass
					else: 
						dicWorld[sector] = {}					
					dicTotalYear	=	{}	
					#startYear		=	yearSort[0]  #les annees sont la 3eme cle de dicWto
					year = 0
					for yearCount in range(minStartYear,maxEndYear):
						year 	= str(yearCount)
						if	dicWto[country][sectorWto].has_key(year):
							valYear				= int(dicWto[country][sectorWto][year])
							dicTotalYear[year]	= valYear
							'''
							try:
								dicTotalYear[year]	= dicTotalYear[year] + valYear
							except:
								dicTotalYear[year]	= valYear
							'''
						else:
							dicTotalYear[year]	= ':'
						'''
						try:
							dicWorld[sector][year]	= dicWorld[sector][year] + valYear
						except:
							dicWorld[sector][year]	= valYear
						'''
					#traitement du total des annees par code CPA
					#le record de sortie par pays
					lstValue  = spiLibTrade.vectorYear(dicTotalYear)
					recordOut =	country+','+sector+','+str(minStartYear)+','+lstValue+'\n'
					fileOutput.write(recordOut)
					'''
					#on fait le calcul apres la normalisation du vecteur
					lstVector =	lstValue.split('!')
					#print country,sector,startYear,lstVector
					year = 0
					for i in range(len(lstVector)):
						yearCount	=	int(minStartYear) + i
						year 	= str(yearCount)
						try:
							dicWorld[sector][year] = dicWorld[sector][year] + 0
						except:
							dicWorld[sector][year] = 0
						try:
							valeur					= int(lstVector[i])
							dicWorld[sector][year] = dicWorld[sector][year] + valeur
						except:#dans ce cas on initialise l'annee avec la valeur
							dicWorld[sector][year] = ':'
							keyNoValue						=	country  + ',' +sector+ ',' + str(year)
							dicCountryNoValue[keyNoValue]	=	keyNoValue
					#print recordOut
					#secteur qui ne sont pas defini dans la table des sectors 
					#mais existent dans les inputs de WTO
					'''
				except:
					dicNoSector[sectorWto]=sectorWto
		except:
			dicNoCountry[countryWto]=countryWto
	#traitement world
	countryNoValueSort	=   dicCountryNoValue.keys()
	countryNoValueSort.sort()
	for countryNoValue in countryNoValueSort:
		recordOut= 'no value for country, sector, year :'+countryNoValue+'\n'
		fileLog.write(recordOut)
	'''
	sectorSort	=   dicWorld.keys()
	sectorSort.sort()
	for	sector	in	sectorSort:	
		lstValue  		= 	spiLibTrade.vectorYear(dicWorld[sector])
		recordOut 		=	'WLD,'+sector+','+str(minStartYear)+','+lstValue+'\n'
		fileOutput.write(recordOut)
	'''
	fileOutput.flush() #on vide le cache
	os.fsync(fileOutput.fileno()) #on force a ecrire sur le disque
	fileOutput.seek(0, 0)#on se positionne sur le 1er caractere de la 1er ligne
	fileOutput.write(str(minStartYear)+','+str(maxEndYear)+'\n')

#------------------------------------------------------------------------------------
traitement(dirCSV)
fileOutput.close()
fileLog.close()	   