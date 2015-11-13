import os,sys,inspect, unittest
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import parser

def IsOdd(a):
    return a%2 == 0

def testInput(inputList):
    for i in inputList:
        print "Input: " + str(i) + "\nOutput: " + str(parser.parseSentance(i, 1.0)) + "\n\n"

class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))
        
def main():
    #unittest.main()
    testInput([["DET", "N", "LVERB", "ADJ"],["DET", "N", "LVERB", "DET", "N"]])

if __name__ == '__main__':
    main()
