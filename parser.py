#This is the script responsible for taking in a possible sentance combination
#in the form of an array of parts of speech, then parsing it using a context
#free grammar and returning the parse tree with a probability of occurance.

#Importing the grammar model that I will be working with
from grammarRules import basicGrammar

#Importing the function that does the matching
from matcher import matchPattern
    
#Tries to find all instances of a Grammar Rule in the sentance (strand)
def matchGrammarRule(setOfRules, sentance):
    #Matching the pattern to the sentance
    #This function should loop through all of the grammar rules given
    #and decide which ones to use:
    #--If there is just one match, or if several non over lapping matches, then use
    #  All of those matches 
    #  --Need to decide on a datastructure to return with
    #--if there are conflicting matches, decide which one take precident. 
    #  Note: any over lapping matches that can occur should have a specified
    #  priority.
    #
    #Essentially this function will return with what subsitutions to make

    #Looping through all of the rules in the set. all of the rules should be in order
    #of priority.
    for grammarRule in setOfRules:
        matchResult = matchPattern(grammarRule[0], sentance)

        if matchResult != None:
            return [grammarRule[1], matchResult]
    #None of the results above found anything
    return None

#Takes in the results of matching on the grammar rule and the current sentance tree
#and returns the new sentance tree
def getNewSentanceTree(matchResults, sentanceTree):
    if matchResults == None:
        #creating a new sentance tree to start off the parsing
        newSentanceTree = []
        for i in sentanceTree: #Looping through the sentance
            newSentanceTree.append([i, None])

        return newSentanceTree
    else:
        #Already have a sentance tree
        newSentanceTree = []

        #Getting the parts before the matches
        leadingRange = matchResults[1][0][0] - 0
        
        if leadingRange > 0:
            newSentanceTree = newSentanceTree + sentanceTree[0:leadingRange]

        #Handling match results intervals
        for i in range(0, len(matchResults[1])):
            #Checking if this is after the first term
            if i > 0:
                newSentanceTree = newSentanceTree + sentanceTree[matchResults[1][i-1][1]+1:matchResults[1][i][0]]
                        

            #Replacing the interval with the new term in the parse tree    
            newSentanceTree.append([matchResults[0], sentanceTree[matchResults[1][i][0]:matchResults[1][i][1]+1]])

        #Adding the section of the parse tree after the matchResults
        endingRange = len(sentanceTree) - (matchResults[1][-1][1] + 1)
        if endingRange > 0:
            newSentanceTree = newSentanceTree + sentanceTree[matchResults[1][-1][1]+1:len(sentanceTree)+1]

        return newSentanceTree


#Returns the sentance like strand of terms at the very top level of the
#parse tree
def getTopLevelSentance(sentanceTree):
    returnSentance = []
    for term in sentanceTree:
        returnSentance.append(term[0])
    return returnSentance

#primary function of this script. Takes in an array of Parts of speech.
def parseSentance(sentance, probability):  
    #checking if this given grammar rule can be found in the sentance
    searching = True
    sentanceTree = getNewSentanceTree(None, sentance)
    currentSentance = getTopLevelSentance(sentanceTree)

    #Loop that does parsing
    while searching:
        result = matchGrammarRule(basicGrammar, currentSentance)
        if result == None:
            searching = False
        else:
            sentanceTree = getNewSentanceTree(result, sentanceTree)
            currentSentance = getTopLevelSentance(sentanceTree)
    
    #returning the parsed result
    return sentanceTree
