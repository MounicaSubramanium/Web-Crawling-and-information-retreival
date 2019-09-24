#!/usr/bin/python

import json
import sys
import os
import traceback
import math
import operator
from math import log
from itertools import combinations

queryID = 0
class extraCredit():
    def __init__(self):
        self.invertedIndex = {}
        self.corpusDirectory = os.path.join(os.getcwd(),'corpusExtraCredit')
        self.dirList = os.listdir(self.corpusDirectory+'/')
        self.uniTokens = []
        self.docIDQueryLength = {}
        self.impDocuments = []
        self.finalDocuments = []
        self.documentLength = {}
        self.termFrequencyCorpus = {}
        self.docIDUniqueTerms = {}
        self.N = 0
        self.docScore = {}
        self.typeofExecution = 0
        self.matchProxmity = 0
        self.searchMap = {0: "Exact Match", 1: "BestMatch", 2: "Proximity Match"}


    def generateAllTokens(self, text):

        self.uniTokens = text.split()

    def createInvertedIndexes(self, docId):
        for term in set(self.uniTokens):
            if term == "":
                continue
            elif term != " ":
                if term not in self.invertedIndex:
                    self.invertedIndex[term] = [[docId, self.uniTokens.count(term)]]
                else:
                    self.invertedIndex[term].append([docId, self.uniTokens.count(term)])
            else:
                pass
    def calculateScore(self, termDocumentFrequency, termFrequencyInDoc, documentLength):
        try:
            termFrequency = float(termFrequencyInDoc)/float(documentLength)
            inverseDocumentFrequency = float(math.log(float(self.N)/float(termDocumentFrequency)))
            tfIdfScore = float(termFrequency) * float(inverseDocumentFrequency)
            return tfIdfScore
        except Exception as e:
            print(traceback.format_exc())

    def generateIndex(self):
        for file in self.dirList:
            with open(self.corpusDirectory+ '/' +file, "r") as f:
                text = f.read()
                docId = file.split('.')[0]
                self.generateAllTokens(text)
                self.createInvertedIndexes(docId)
                f.close()

    def calculateParams(self):

        totalTokens = 0

        for term in self.invertedIndex:
            listofDocFreq = self.invertedIndex[term]
            termFrequencyCorpus = 0
            for pair in listofDocFreq:
                documentID = pair[0]
                termFreq = pair[1]
                if documentID in self.documentLength:
                    self.documentLength[documentID] += termFreq        
                else:
                    self.documentLength[documentID] = termFreq
                totalTokens += termFreq
                termFrequencyCorpus += termFreq
            if term in self.termFrequencyCorpus:
                self.termFrequencyCorpus[term] += termFrequencyCorpus
            else:
                self.termFrequencyCorpus[term] = termFrequencyCorpus

        self.N = len(self.documentLength.keys())


    def findDocuments(self, query):
        termsInQuery = query.split()
        for term in termsInQuery:
            if term in self.invertedIndex:
                listForTerm = self.invertedIndex[term]
                for pair in listForTerm:
                    docId = pair[0]
                    if docId in self.docIDQueryLength:
                        self.docIDQueryLength[docId] += 1
                    else:
                        self.docIDQueryLength[docId] = 1

                    if docId in self.docIDUniqueTerms:
                        self.docIDUniqueTerms[docId].append(term)
                    else:
                        self.docIDUniqueTerms[docId] = []
                        self.docIDUniqueTerms[docId].append(term)

    def generateImpDocuments(self, query):
        
        for key, value in self.docIDQueryLength.iteritems():
            if self.typeofExecution == 0:
                if value  ==  len(query.split()):
                    self.impDocuments.append(key)
            if self.typeofExecution == 1 or self.typeofExecution == 2:
                if value >= 1:
                    self.impDocuments.append(key)

        if self.typeofExecution == 0:
            for doc in self.impDocuments:
                with open(self.corpusDirectory + '/' + doc+".txt", "r") as f:
                    text = f.read()
                    if (self.findDocumentsWithExactMatch(text, query)):
                        self.finalDocuments.append(doc)
                    f.close()

        if self.typeofExecution == 1:
            self.finalDocuments = self.impDocuments

        if self.typeofExecution == 2:
            for doc in self.impDocuments:
                if self.docIDQueryLength[doc] == 1:
                    self.finalDocuments.append(doc)
                if self.docIDQueryLength[doc] > 1:
                    with open(self.corpusDirectory + '/' + doc+".txt", "r") as f:
                        text = f.read()
                        if (self.findDocumentsWithProximityMatch(doc, text)):
                            self.finalDocuments.append(doc)
                        f.close()


    def processtfidf(self, query, queryID):

        
        if len(self.finalDocuments) == 0:
            print 'No Documents Found to be ranked for Query = %d' % queryID

        self.docScore = {}

        try:
            queryTermList = query.split()
            for term in queryTermList:
                if term in self.invertedIndex:
                    listForTerm = self.invertedIndex[term]
                    dfTerm = len(listForTerm)
                    termFreqInQuery = queryTermList.count(term)
                    for pair in listForTerm:
                        if pair[0] in self.finalDocuments:
                            documentID = pair[0]
                            documentName = str(documentID)
                            documentLength = self.documentLength[documentID]
                            documentTf = pair[1]
                            termScore =  self.calculateScore(dfTerm, documentTf, documentLength)
                            if documentName in self.docScore:
                                self.docScore[documentName] += termScore
                            else:
                                self.docScore[documentName] = termScore
        
        except Exception as e:
            print(traceback.format_exc())


    def rankDocuments(self):
        self.calculateParams()
        

        queryFile = open('queriesExtraCredit.txt', 'r')
        for line in queryFile:
            global queryID
            queryID += 1
            self.findDocuments(line)
            self.generateImpDocuments(line)
            self.processtfidf(line, queryID)
            print ("Relevant Documents for Query No = %d, Search Type = %s" % (queryID, self.searchMap[self.typeofExecution]))
            print self.docScore
        
        queryFile.close()
        
    def findDocumentsWithExactMatch(self, text, query):
        docTokens = text.split()
        termsinQuery = query.split()
        firstTerm = termsinQuery[0]
        lengthOfQuery = len(termsinQuery)
        c = 0

        for term in docTokens:
            if firstTerm == term:
                if (c + lengthOfQuery <= len(docTokens) - 1):
                    if docTokens[ c+ (lengthOfQuery)]:
                        subsetList = docTokens[c : c + (lengthOfQuery)]
                else:
                    subsetList = docTokens[c : ]
                if subsetList == termsinQuery:
                    return True
                else:
                    return False

            c += 1

    def findDocumentsWithProximityMatch(self, doc, text):
        docTokens = text.split()
        proximity = False
        uniqueComboList =  [",".join(map(str, comb)) for comb in combinations(self.docIDUniqueTerms[doc], 2)]
        for termComb in uniqueComboList:
            words = termComb.split(",")
            word1 = words[0]
            word2 = words[1]
            if abs(docTokens.index(word1) - docTokens.index(word2)) <= self.matchProxmity:
                proximity = True
            else:
                return False

        return proximity

if __name__ == '__main__':
    instance =  extraCredit()
    instance.typeofExecution = int(raw_input("Please enter the Search Type, ExactMatch - 0, BestMatch - 1, Proximity Match - 2: "))
    if (instance.typeofExecution == 2):
        instance.matchProxmity = int(raw_input("Please enter match proximity: "))
    instance.generateIndex()
    instance.rankDocuments()


