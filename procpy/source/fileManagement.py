import os
from glob import glob
from pprint import pprint

def cleanFilesBasedOnExt(folderPath, extension) :
    fileList = glob(folderPath + '\\*.' + extension)
    removeFiles(fileList)
        
def removeFiles(fileList) :
    for file in fileList :
        os.remove(file)

def removeLastFileBasedOnExt(folderPath, extension) :
    fileList = glob(folderPath + '\\*.' + extension)
    cnt = 0
    lastfile = ''
    for file in fileList : 
        if cnt == 0 :
            lastFile = file
            lastFileTime = os.path.getmtime(file)
        else :
            if os.path.getmtime(file) > lastFileTime :
                lastFile = file
                lastFileTime = os.path.getmtime(file)
        cnt += 1
    if lastfile != '':
        os.remove(lastFile)

def moveFilesBasedOnExt(oldFolderPath, newFolderPath, extension) :
    fileList = glob(oldFolderPath + '\\*.' + extension)
    for file in fileList :
        os.rename(file, newFolderPath + '\\' + file.split('\\')[-1])