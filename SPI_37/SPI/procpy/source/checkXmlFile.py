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
import checkXmlAccess

#parametres application
#parametre path le drive et le chemin jusqu'a spi: 'C:\\Users\\gomezrv\\Documents\\Projets\\Spi'
Path             =  sys.argv[1]
G_xmlType        =  sys.argv[2]

dirUse          =  Path    
dirLog          =  dirUse           +'\\Log'
if    G_xmlType    == 'bec':
    fichiersXML     =  glob.glob(dirUse +'\\Input\\xml\\'+G_xmlType+'\\*.xml')
    fileLog         =  open(dirLog      +'\\checkXmlFile'+G_xmlType+'.log', 'w')
else:
    fichiersXML     =  glob.glob(dirUse +'\\Input\\xml\\*.xml')
    fileLog         =  open(dirLog      +'\\checkXmlFile.log', 'w')
    
# lecture et traitement fichier xml
def traitementXML(fichiersXml):
    for fichierXml in fichiersXml:
        checkXmlAccess.lectureXML(fichierXml,fileLog)
#------------------------------------------------------------------------------------
traitementXML(fichiersXML)
fileLog.close()       