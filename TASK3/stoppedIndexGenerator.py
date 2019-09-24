import json
import os
import sys
import io
import traceback
import string

class indexGen():
    
    def __init__(self):
        self.corpusDirectory = os.path.join(os.getcwd(),'corpusTask1')
        self.dirList = os.listdir(self.corpusDirectory+'/')
        self.outputFolder = os.path.join(os.getcwd(),'InvertedIndex')

        self.uniTokens = []
        self.invertedIndex = {}

    def generateAllTokens(self, text):

        self.uniTokens = text.split()
        
    def createInvertedIndexes(self, docId):
        
        commonWords = self.readCommonWordFile('common_words')
        for term in set(self.uniTokens):
            if term not in commonWords:
                if term == "":
                    continue
                elif term != " ":
                    if term not in self.invertedIndex:
                        self.invertedIndex[term] = [[docId, self.uniTokens.count(term)]]
                    else:
                        self.invertedIndex[term].append([docId, self.uniTokens.count(term)])
                else:
                    pass
            else:
                print 'Ignoring Common Term From List'
    
    def generateIndex(self):
        for file in self.dirList:
            with open(self.corpusDirectory+ '/' +file, "r") as f:
                text = f.read()
                docId = file.split('.')[0]
                self.generateAllTokens(text)
                self.createInvertedIndexes(docId)
                f.close()
            
    def writeToFile(self, file):
        try:
            if not os.path.exists(self.outputFolder):
                os.makedirs(self.outputFolder)
            
            with io.open(os.path.join(self.outputFolder, file +".txt" ), 'w', encoding='utf-8') as file:
                file.write(unicode(json.dumps(self.invertedIndex ,sort_keys=True)))
                file.close()

        except Exception as e:
            print traceback.format_exc()

    def readCommonWordFile(self, fileName):
        try:
            commonWords = []
            with open(fileName, 'r') as f:
                for commonWord in f.readlines():
                    commonWord = string.replace(commonWord, '\n', '')
                    commonWords.append(commonWord)
                f.close()
                return commonWords

        except Exception as e:
            print traceback.format_exc()

if __name__ == '__main__':
    instance = indexGen()
    instance.generateIndex()
    instance.writeToFile("invertedindexstopped")
