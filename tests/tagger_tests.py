import os,sys,inspect, unittest
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import tagger

def IsOdd(a):
    return a%2 == 0

def testSentances(sentanceList):
    for sentance in sentanceList:
        print "Sentance: " + str(sentance)
        combos = tagger.getSentanceCombos(sentance)
        if combos != False:
          for combo in combos:
              print  str(combo)
        else:
          print "Combo returned false"
        print "----------------------------------------------------------------------\n"

class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.failUnless(IsOdd(1))

    def testTwo(self):
        self.failIf(IsOdd(2))
        
def main():
    #unittest.main()
    testSentances(["The cat is very red",
               "I ran to the store",
               "I then came back on a stolen bike",
               "when is the parade",
               "walk the dog"])

if __name__ == '__main__':
    main()
