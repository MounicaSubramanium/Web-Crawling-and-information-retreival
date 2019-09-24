import os
import traceback
from os.path import exists
import re
import string

currentDirectory = os.getcwd()

def removePunctuation(token):
    if (token[len(token) - 1:] == ","  or token[len(token) - 1:] == "." or token[len(token) - 1:] == "-"):
        token = token[:len(token)-1]
    
    return removeLeft(token)

def removeLeft(token):
    while(token[:1] == "-" or token[:1] == "." or token[:1] == ","):
        if token[:1] == "-" or token[:1] == "." or token[:1] == ",":
            token = token[1:]
    
    return token

def processedQuery(queriesToBeProcessed, commonWords):
    try:
        tempQueryList = []

        query = queriesToBeProcessed[queriesToBeProcessed.find('</DOCNO>')+8 : queriesToBeProcessed.find('</DOC>')]        
        
        queryPattern = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
        
        query = queryPattern.sub(' ',query)
        
        for terms in query.split():
            if terms not in commonWords:
                tempQueryList.append(removePunctuation(terms))
        
        while '' in tempQueryList:
            del tempQueryList[tempQueryList.index('')]
        query = " ".join(tempQueryList)
        queriesToBeProcessed = queriesToBeProcessed[queriesToBeProcessed.find('</DOC>') + 6:]
        
        return queriesToBeProcessed,query
    
    except Exception as e:
        print(traceback.format_exc())

def processQueries():
    try:
        if exists(currentDirectory+ '/' + "stoppedQuery.txt"):
            os.remove(currentDirectory+ '/' + "stoppedQuery.txt")

        with open(currentDirectory+ '/' + "cacm.query.txt",'r') as f:
            queriesToBeProcessed = f.read()

        queryFile = open(currentDirectory+ '/' + "stoppedQuery.txt",'a')

        commonWords = readCommonWordFile('common_words')

        while queriesToBeProcessed.find('<DOC>')!=-1:
            queriesToBeProcessed, singleQuery = processedQuery(queriesToBeProcessed, commonWords)
            if(queriesToBeProcessed.find('<DOC>') == -1):
                queryFile.write(singleQuery.lower())
            else:
                queryFile.write(singleQuery.lower() + "\n")

    except Exception as e:
        print(traceback.format_exc())

def readCommonWordFile(fileName):
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




processQueries()