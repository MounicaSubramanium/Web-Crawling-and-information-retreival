import re
from glob import glob
import operator
import os
from bs4 import BeautifulSoup
import traceback

class corpusGeneratorTask1():
    
    def __init__(self):
        self.currentDirectory = os.getcwd()
        self.inputFolder = os.path.join(self.currentDirectory,'cacm')
        self.outputFolder = os.path.join(self.currentDirectory,'corpusTask1')
        self.listOfFiles = os.listdir(self.inputFolder)

    def processHTMLS(self):
        for file in self.listOfFiles:
            with open(self.inputFolder +'/' + file, 'r') as file_content:
                processTokens = self.processContent(file_content.read().lower())
                self.dumpToFile(file.replace("html" , "txt"), processTokens)
                file_content.close()

    def processContent(self, file_content):
        listofTokens = []
        try:
            soup = BeautifulSoup(file_content, "html.parser")
            soup.prettify().encode("utf-8")
            mainContent = soup.find('pre').get_text().encode("utf-8")
            mainContent = self.removeSymbols(mainContent)
            tokenizedMainContent =  mainContent.split()
            for terms in tokenizedMainContent:
                term = self.removePunctuation(terms)
                listofTokens.append(term)
            while '' in listofTokens:
                del listofTokens[listofTokens.index('')]
        except Exception as e:
            print traceback.format_exc()
        return listofTokens

    def removeSymbols(self, file_content):
        pattern = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
        file_content = pattern.sub(' ',file_content)
        return file_content

    def removeLeft(self, token):
        while(token[:1] == "-" or token[:1] == "." or token[:1] == ","):
            if token[:1] == "-" or token[:1] == "." or token[:1] == ",":
                token = token[1:]
    
        return token

    def removePunctuation(self, token):
        if (token[len(token) - 1:] == ","  or token[len(token) - 1:] == "." or token[len(token) - 1:] == "-"):
            token = token[:len(token)-1]
    
        return self.removeLeft(token)

    def dumpToFile(self, fileName, processedFileContent):
        unigramTokens = " ".join(processedFileContent)
        try:
            if not os.path.exists(self.outputFolder):
                os.makedirs(self.outputFolder)
            with open (self.outputFolder+ '/' + fileName,"w+") as f:
                f.write(unigramTokens)
                f.flush()
                f.close()
        except Exception as e:
            print traceback.format_exc()

if __name__ == '__main__':
    instance = corpusGeneratorTask1()
    instance.processHTMLS()