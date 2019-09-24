#!/usr/bin/python

import json
import sys
import os
import traceback
import math
import operator
from math import log
from math import sqrt

class evaluator():
    
    def __init__(self, scoreFolder, outputFolder):
        self.inputFolder = os.path.join(os.getcwd(), 'Results')
        self.inputFolder = os.path.join(self.inputFolder, str(scoreFolder))
        self.outputFolder = os.path.join(os.getcwd(), "Evaluation")
        self.outputFile = str(outputFolder)
        self.listOfFiles = os.listdir(self.inputFolder)
        self.listOfQueriesNoRelevant = []
        self.queryRelMapping = {}
        self.map = 0.0
        self.mrr = 0.0

    def evaluate(self):
        totalQueries = 0
        try:
            if not os.path.exists(self.outputFolder):
                os.makedirs(self.outputFolder)
        except Exception as e:
            print (traceback.format_exc())

        evaluationFile = open(self.outputFolder + '/' + self.outputFile+  '-Evaluation.txt', 'w+')
        precisionAtFile = open(self.outputFolder + '/' + self.outputFile+ '-PrecisionAt520.txt', 'w+')
        evaluationFile.write("Query Rank Precision Recall\n")
        precisionAtFile.write("Query Prec-5 Prec-20\n")

        for file in self.listOfFiles:
            with open(self.inputFolder +'/' + file, 'r') as file_content:
                queryNumber = file.split('.')[0]
                queryNumber = queryNumber[5:]
                findRelevantNumbers = float(self.findNumOfRelevantDocs(queryNumber))
                if findRelevantNumbers == 0:
                    self.listOfQueriesNoRelevant.append(file)
                    continue
                else:
                    totalQueries += 1
                reciprocalRank = 0.0
                avgPrecision = 0.0
                precision5 = 0.0
                precision20 = 0.0
                recall = 0.0
                relevanceTillNow = 0.0
                for line in file_content:
                    params = line.split()
                    querNo = params[0]
                    document = params[2]
                    rank = float(params[3])
                    if document in self.queryRelMapping[querNo]:
                        relevanceTillNow += 1
                        avgPrecision += (relevanceTillNow / rank)
                        if reciprocalRank == 0.0:
                            reciprocalRank = (1/rank)
                        if findRelevantNumbers > 0.0:
                            recall = (relevanceTillNow/findRelevantNumbers)
                        else:
                            pass
                    if rank == 5.0:
                        precision5 = (relevanceTillNow/rank)
                    if rank == 20.0:
                        precision20 = (relevanceTillNow/rank)

                    evaluationFile.write(querNo + " " + str(int(rank)) + " " + str(relevanceTillNow / rank) + " " + str(recall) + "\n")

                if relevanceTillNow > 0.0:
                    avgPrecision = (avgPrecision/relevanceTillNow)
                
                precisionAtFile.write(querNo + " " + str(precision5)+ " "+ str(precision20) + "\n")
                self.map += avgPrecision
                self.mrr += reciprocalRank
                file_content.close()
        self.map = self.map / float(totalQueries)
        self.mrr = self.mrr / float(totalQueries)
        evaluationFile.write("\nMAP" + " - " + str(self.map))
        evaluationFile.write("\nMRR" + " - " + str(self.mrr))
        evaluationFile.write("\nQueries with No Relevance\n")

        for item in self.listOfQueriesNoRelevant:
            evaluationFile.write(item +"\n")

        evaluationFile.close()
        precisionAtFile.close()

    def findNumOfRelevantDocs(self, queryNumber):
        totalCount = 0
        try:
            with open('cacm.rel.txt','r') as rel:
                for line in rel.readlines():
                    relParams = line.split()
                    if relParams[0] == str(queryNumber):
                        totalCount += 1
                return totalCount     
                rel.close()
        except Exception as e:
            print(traceback.format_exc())

    def findQueryRelMapping(self):
        try:
            with open ('cacm.rel.txt', 'r') as rel:
                for line in rel.readlines():
                    relParams = line.split()
                    if relParams[0] in self.queryRelMapping:
                        self.queryRelMapping[relParams[0]].append(relParams[2])
                    else:
                        self.queryRelMapping[relParams[0]] = []
                        self.queryRelMapping[relParams[0]].append(relParams[2])
                rel.close()
        except Exception as e:
            print(traceback.format_exc())


if __name__ == '__main__':
    scoreFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    instance =  evaluator(scoreFolder, outputFolder)
    instance.findQueryRelMapping()
    instance.evaluate()







