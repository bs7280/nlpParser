import os,sys,inspect, unittest
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import matcher
from grammarRules import simpleGrammar

def testInput(inputList):
    for i in inputList:
        print "Input: " + str(i) + "\nOutput: "  + str(matcher.getOptionalTerms(i[0], i[1], i[2])) + " \n"

def main():
    #Unit tests
    testInput( #Tests for the required Terms part
             [
                [[[0,0, "DET"], [1,3,"N"], [4,4,"ADJ"]], 0, 4],
                [[[0,3, "DET"], [5, 6, "N"], [8, 8, "ADV"]], 0, 8],
                [[[0,2, "DET"], [6, 9, "N"], [11, 12, "ADV"]], 0, 12],
                [[[1, 1, "A"], [4,5,"B"], [7,9,"C"]], 0, 8]
                ])

if __name__ == '__main__':
    main()
