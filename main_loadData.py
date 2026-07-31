import src.dataColect.makeCSV as makeCSV
import pickle
import os

def main():
    makeCSV.makeFilesCsv('.\\DataAPIJira\\')
    #makeCSV.test_execution_csv('.\\DataAPIJira\\')

if __name__=="__main__":
    main()