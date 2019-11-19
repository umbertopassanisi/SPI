
def dicNace(nace,dirTXT): #nace=1|2,compteEurostat = NAMA|SBS|BD, level = 1|2 0=on prend tous les levels
	dicNace	=	{}
	fichierLecture 	=	dirTXT + '\\'+nace+'Matrix.txt'
	try:
		fichier = open(fichierLecture, 'r')
	except:
		print("le fichier ", fichierLecture, " est introuvable")
	rec1er     	= fichier.readline() #1er rec avec les meta	
	for	record in fichier:
		codeNace			=	record.strip()
		dicNace[codeNace]	=	codeNace
	fichier.close()
	return dicNace