#!/usr/bin/python

import json
import sys
import os
import traceback
import math
import operator
from math import log
import re

queryID = 0

class snippetGenerator():
    def __init__(self, scoreFolder):
        self.inputScoreFolder = os.path.join(os.getcwd(),'Results')
        self.inputScoreFolder = os.path.join(self.inputScoreFolder, scoreFolder)
        self.corpusDirectory = os.path.join(os.getcwd(),'corpusTask1')
        self.queryIdScoredDocs = {}
        self.listDir = os.listdir(self.inputScoreFolder+'/')


    def populateDictionarty(self):
        for file in self.listDir:
            with open(self.inputScoreFolder+ '/' +file, "r") as f:
                for line in f:
                    params = line.split(" ")
                    queryId = params[0]
                    doc_id = params[2]
                    if queryId in self.queryIdScoredDocs:
                        self.queryIdScoredDocs[queryId].append(doc_id)
                    else:
                        self.queryIdScoredDocs[queryId] = []
                        self.queryIdScoredDocs[queryId].append(doc_id)
                f.close()

    def generateNgramSnippet(self, queryList, docID, grams):
        
        corpusDoc = open(self.corpusDirectory + '/' + docID + '.txt', 'r+')    # Read the document.
        corpusText = corpusDoc.read()
        
        snippet = "Nothing Interesting Found in the Document"
        
        for term in range(len(queryList) - grams):
        
            if grams > 0:
                ngramterms = queryList[term:(term + (grams + 1))]
                ngramstring = " ".join(ngramterms) 
            else:
                ngramstring = queryList[term]

            if corpusText.find(ngramstring) != -1 and bool(re.findall('\\b'+ngramstring + '\\b', corpusText)):
                matchingNgram = re.findall('\\b'+ ngramstring+ '\\b', corpusText)
                startOfTerm = re.search('\\b'+ ngramstring+ '\\b', corpusText)
                startMatchIndex = startOfTerm.start()
                termsBeforeGramsIndex = max(startMatchIndex - 30, 0)

                if termsBeforeGramsIndex != 0:
                    while termsBeforeGramsIndex > 0:
                        if corpusText[(termsBeforeGramsIndex - 1) : termsBeforeGramsIndex] not in [" ", "\n"]:
                            termsBeforeGramsIndex -= 1
                        else:
                            break

                termsAfterGramsIndex = min(corpusText.index(ngramstring) +  len(matchingNgram[0]) + 30, len(corpusText))

                if termsAfterGramsIndex != len(corpusText):
                    while termsAfterGramsIndex < len(corpusText):
                        if corpusText[termsAfterGramsIndex:termsAfterGramsIndex + 1] not in [" ", "\n"]:
                            termsAfterGramsIndex += 1
                        else:
                            break

                listOfBeforeQueryTerms = corpusText[termsBeforeGramsIndex : startMatchIndex]
                
                importantTerms = corpusText[startMatchIndex : (startMatchIndex + len(matchingNgram[0]))]

                importantTerms = '<mark>{}</mark>'.format(importantTerms)

                listOfAfterQueryTerms = corpusText[(startMatchIndex + len(matchingNgram[0])):termsAfterGramsIndex]

                sentence = listOfBeforeQueryTerms + importantTerms + listOfAfterQueryTerms

        return sentence

        corpusDoc.close()


    def genSnippetForQuery(self):
        
        self.populateDictionarty()

        queryFile = open('originalQuery.txt', 'r')
        resultsFile = open('snippet-results.html', 'w+')
        resultsFile.write("<!DOCTYPE html>")
        c = 0
        
        for line in queryFile:
            c = 0
            global queryID
            queryID += 1
            resultsFile.write("===============================================================================<br/>")
            resultsFile.write("Query " +str(queryID)+ " : "+line + " <br />")
            for docs in self.queryIdScoredDocs[str(queryID)]:
                resultsFile.write("Document : " + docs + "<br />")
                sentence = self.generateNgramSnippet(line.split(), docs, 0)
                resultsFile.write(str(sentence) +"<br />")
                resultsFile.write("_____________________________________________________________________________<br/>")
                resultsFile.write("<br \>")
                c += 1
                if c > 10:
                    break
            resultsFile.write("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@<br/>")
    
        
        queryFile.close() 
        resultsFile.close()


if __name__ == '__main__':
    scoreFolder = sys.argv[1]
    instance = snippetGenerator(scoreFolder)
    instance.genSnippetForQuery()




