import sys
import fileManagement
from pprint import pprint

G_folderPath = sys.argv[1]

def main(folderPath):
    fileManagement.cleanFolderFromFilesBasedOnExt(folderPath, 'xml')

main(G_folderPath)