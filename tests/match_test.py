import os,sys,inspect, unittest
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import matcher
from grammarRules import simpleGrammar

def testInput(inputList):
    for i in inputList:
        print "Input: " + str(i) + "\nOutput: " + str(matcher.matchPattern(i[0][0], i[1])) + "\n\n"

def main():
    #Unit tests
    testInput( #Tests for the required Terms part
             [[simpleGrammar[4], ["DET", "N", "N", "N", "LVERB", "ADJ"]],
              [simpleGrammar[4], ["DET", "N", "LVERB", "DET", "N"]], 
              [simpleGrammar[4], ["DET", "N"]], 
              [simpleGrammar[4], ["DET", "DET", "N", "N"]],
              [simpleGrammar[4], ["N", "DET", "ADJ", "N", "N"]],
              [simpleGrammar[6], ["N", "N", "D", "N", "N", "N", "D", "N", "D", "D", "D"]],
              [simpleGrammar[7], ["A", "B", "A", "B", "A", "A", "B", "A", "B"]],

              #Testing the Base case of match function (All optional terms)
              [simpleGrammar[5], ["DET", "ADV", "ADV", "ADJ", "ADJ"]], 
              [simpleGrammar[5], ["DET", "ADV", "ADV", "ADJ", "ADJ", "N", "ADV", "ADV", "N", "ADJ", "ADV", "ADJ", "ADJ"]], 

              #Testing the recursive part of the matching (using both the required terms and the optional terms)
              [simpleGrammar[8], ["DET", "ADV", "ADV", "ADJ", "N", "N", "LVERB", "DET", "ADJ", "N"]],  
              [simpleGrammar[9], ["DET", "ADV", "N", "ADJ", "ADJ", "DET", "LVERB", "DET", "ADJ", "N"]], 
              
              #These should fail
              [simpleGrammar[8], ["DET", "ADJ", "ADV", "N", "N", "LVERB", "DET", "ADJ", "N"]], #ADV and ADJ are switch and backward
              [simpleGrammar[9], ["DET", "CAT", "N", "ADJ", "ADJ", "DET", "LVERB", "DET", "ADJ", "N"]], #And occurance of optional
                                                                                                    #term does not happen
              [simpleGrammar[8], ["DET", "DET", "ADV", "ADJ", "ADV", "ADJ", "N", "N", "LVERB", "DET", "ADJ", "N"]],  
              [simpleGrammar[9], ["DET", "ADV", "N", "ADJ", "ADV", "DET", "LVERB", "DET", "ADJ", "N"]], 

              #Testing for optional terms before and after the required terms
              [simpleGrammar[11], ["DET", "N", "ADJ", "ADJ", "DET", "N", "LVERB", "ADJ", "ADJ", "DET", "N"]],
              [simpleGrammar[10], ["DET", "N", "ADJ", "ADJ", "DET", "N", "LVERB", "ADJ", "ADJ", "DET", "N", "ADJ"]],

              [simpleGrammar[12], ["A", "B", "NP", "D"]]
              

              ])

if __name__ == '__main__':
    main()
