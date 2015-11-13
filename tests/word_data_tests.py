import os,sys,inspect, unittest
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import word_data

def IsOdd(a):
    return a%2 == 0

def testWords(wordList):
    for i in wordList:
        print i + " " + str(word_data.getSimpleWordData(i))

class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))
        
def main():
    #unittest.main()
    testWords(["cat", "round", "well", "skateboard", "asdasfaf", "buffalo", "alphabet",
               "the", "that", "a great deal of","22 caliber", "from", "search", "no", "and"])

if __name__ == '__main__':
    main()
