#Main.py
#this is the main script of the project that is meant to be the primary interface of the sentance
#parser. The above is all from a previous version of a NLP parser that I copied over at some
#point. 

#Importing Stuff
import sys
import tagger 
import parser

#Main function takes in a sentance as a string. It is defined here as the main function so that
#command line arguments can be used. That part is implemented below. Since the main function
#has not been completely written yet, I am not sure what the final outcome of the function will be
#and what it will return, but it will likely return a parse tree of the sentance.
def main(sentance):
    #this makes a call to the tagger that will return a list of all possible
    #part of speech combos, with percentage chance of occuring.
    tagCombos = tagger.getSentanceCombos(sentance)
    if(tagCombos != False):
        parsedSentance = parser.parseSentance(tagCombos[0][0], tagCombos[0][1])
    else:
        return False

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        main(" ".join(sys.argv[1:]))

