README

#############################
#The files and what they do:#
#############################

classes.py:
    Contains classes that are used in the word searching and tagging portion

grammar_exceptions.py:
    essetnailly contains a list of words not found in the wordnet dictionary
    that are not standard parts of speech, yet are important to forming sentaces
    examples: "the, at, to, is, etc..."

grammarRules.py:
    contains the list of grammar rules for a context free grammar. Initial grammar
    rules taken from 

main.py:
    the main file that runs everything. A sentance can be run from it by either
    calling main.py with command line arguments, or just callin main() with a
    sentance in the form of a string as the only parameter.

parser.py:
    contains the code that will take in input in the form of a list of Parts of speech
    and return a parse tree using the grammar rules in grammarRules.py

tagger.py:
    Takes in a sentance as a string, looks up the word data from wordnet, and 
    returns all of the possible combos of forming a sentance with different 
    parts of speech, with a cooresponding percent chance of likely 
    hood (based on limited wordnet data)
    
    function to call: getSentanceCombos(sentance) where sentance is a string

word_data.py
    The script responsible for taking in a string representing a word, and 
    returns data about that word from the wordnet file.

    function to call: getSimpleWordData(word)


