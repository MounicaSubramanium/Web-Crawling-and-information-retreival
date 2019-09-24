import json
import os
import sys
import io
import traceback
import string


class stemmedDocsGenerator():
    
    def __init__(self):
        self.currentDirectory = os.getcwd()
        self.corpusDirectory = os.path.join(os.getcwd(),'corpusTask3Stemmed')

    def readStemmedFile(self):
        try:
            with open(self.currentDirectory + '/' + 'cacm_stem.txt', 'r') as f:
                for line in f:
                    line = line.strip('\n')
                    dockChecker = line.split(" ")
                    if dockChecker[0] == "#":
                        if not dockChecker[1] == "1":
                            try:
                                writeFile.close()
                            except Exception as e:
                                print traceback.format_exc()
                        docName = "CACM-{:04}.txt".format(int(dockChecker[1]))
                        if not os.path.exists(self.corpusDirectory):
                            os.makedirs(self.corpusDirectory)    
                        writeFile = open(self.corpusDirectory+ '/' + docName, "w+")
                    else:
                        writeFile.write(line + " ")
                f.close()
        except Exception as e:
            print traceback.format_exc()

if __name__ == '__main__':
    instance = stemmedDocsGenerator()
    instance.readStemmedFile()


