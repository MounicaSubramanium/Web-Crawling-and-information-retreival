import os
import traceback
from os.path import exists
import re

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

def processedQuery(queriesToBeProcessed):
    try:
        tempQueryList = []

        query = queriesToBeProcessed[queriesToBeProcessed.find('</DOCNO>')+8 : queriesToBeProcessed.find('</DOC>')]        
        
        queryPattern = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
        
        query = queryPattern.sub(' ',query)
        
        for terms in query.split():
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
        if exists(currentDirectory+ '/' + "originalQuery.txt"):
            os.remove(currentDirectory+ '/' + "originalQuery.txt")

        with open(currentDirectory+ '/' + "cacm.query.txt",'r') as f:
            queriesToBeProcessed = f.read()

        queryFile = open(currentDirectory+ '/' + "originalQuery.txt",'a')

        while queriesToBeProcessed.find('<DOC>')!=-1:

            queriesToBeProcessed, singleQuery = processedQuery(queriesToBeProcessed)

            if(queriesToBeProcessed.find('<DOC>') == -1):
                queryFile.write(singleQuery.lower())
            else:
                queryFile.write(singleQuery.lower() + "\n")

    except Exception as e:
        print(traceback.format_exc())




processQueries()