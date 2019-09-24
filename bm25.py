#!/usr/bin/python

import json
import sys
import os
import traceback
import math
import operator
from math import log

queryID = 0

class bm25():
    
    def __init__(self, outputFolder):
        self.outputFolder = outputFolder
        self.indexDirectory = os.path.join(os.getcwd(),'InvertedIndex')
        self.outputDirectory = os.path.join(os.getcwd(), str(outputFolder))
        self.invertedIndex = {}
        self.documentLength = {}
        self.avdl = 0
        self.N = 0
        self.docScore = {}


    def calculateParams(self, invertedIndex):

        totalTokens = 0

        for term in invertedIndex:
            listofDocFreq = invertedIndex[term]
            for pair in listofDocFreq:
                documentID = pair[0]
                termFreq = pair[1]
                if documentID in self.documentLength:
                    self.documentLength[documentID] += termFreq        
                else:
                    self.documentLength[documentID] = termFreq
                totalTokens += termFreq

        self.N = len(self.documentLength.keys())
        numDocuments = len(self.documentLength.keys())
        self.avdl = (totalTokens / numDocuments)
        print (totalTokens)

    def calculateScore(self, n, f, qf, r, N, dl,R):
        try:
            k1 = 1.2
            k2 = 100
            b = 0.75
            K = k1 * ((1 - b) + b * (float(dl) / float(self.avdl)))
            print ((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5))
            part1 = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
            part2 = ((k1 + 1) * f) / (K + f)
            part3 = ((k2 + 1) * qf) / (k2 + qf)
            return part1 * part2 * part3
        except Exception as e:
            print(traceback.format_exc())

    def processBM25(self, query, queryID):

        self.docScore = {}
        try:
            queryTermList = query.split()
            for term in queryTermList:
                if term in self.invertedIndex:
                    listForTerm = self.invertedIndex[term]
                    dfTerm = len(listForTerm)
                    termFreqInQuery = queryTermList.count(term)
                    for pair in listForTerm:
                        documentID = pair[0]
                        documentName = str(documentID)
                        documentLength = self.documentLength[documentID]
                        documentTf = pair[1]
                        termScore =  self.calculateScore(dfTerm, documentTf, termFreqInQuery , 0 , self.N, documentLength, 0)
                        if documentName in self.docScore:
                            self.docScore[documentName] += termScore
                        else:
                            self.docScore[documentName] = termScore
        
        except Exception as e:
            print(traceback.format_exc())

    def writeToFile(self, queryID):

        try:
            if not os.path.exists(self.outputDirectory):
                os.makedirs(self.outputDirectory)      
            score_per_query = sorted(self.docScore.items(),key=operator.itemgetter(1),reverse=True)[:100]
            rank = 1  
            file = open(self.outputDirectory + "/" + "query" + str(queryID) + ".txt", 'w')
            for doc in score_per_query:
                file.write(str(queryID)+ " "+ "Q0 " +doc[0]+ " " +str(rank).zfill(2)+ " " +str(doc[1])+ " " + str(self.outputFolder) +"\n")
                rank += 1
            file.close()
        except Exception as e:
            print(traceback.format_exc())


    def readInvertedIndex(self, indexFile, queryFile):
        try:
            with open (self.indexDirectory+ '/' + str(indexFile)) as f:
                self.invertedIndex = json.load(f)
                f.close()
        except Exception as e:
            print traceback.format_exc()

        self.calculateParams(self.invertedIndex)
        count = 1
        queryFile = open(queryFile, 'r')
        for line in queryFile:
            global queryID
            queryID += 1
            self.processBM25(line, queryID)
            self.writeToFile(queryID)
        queryFile.close()

if __name__ == '__main__':
    indexFile = sys.argv[1]
    queryFile = sys.argv[2]
    outputFolder = sys.argv[3]
    instance =  bm25(outputFolder)
    instance.readInvertedIndex(indexFile, queryFile)

