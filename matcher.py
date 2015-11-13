#given the pattern (grammar rule), try to match it in the strand (sentance)
#and return the interval of the pattern's occurance
#   Note: This implimentation will not be that efficient/optimized in the origional 
#   version because I am simply trying to get it to work. But ultimately
#   there are a few things that I will be able to do to make it more efficient.
#   the first that comes to mind is to group up similiar types of grammar rules (NP)
#   that all work off of the existance of Nouns, then find all of the Nouns once, then
#   use that information on all of the NP grammar rules. Also, specify in
#   the definition of the grammar rules which spots in the grammar rule is required.
def matchPattern(pattern, strand):
    #Variables to keep track of which terms are required
    #and where they are in the pattern respectively
    requiredTerms = []
    # requiredTermsPatternLocations = []

    #Variable to keep track of where in the strand the required
    #terms occur. List of lists, where the sublists are a list of
    #intervals of occurance
    requiredTermsIntervals = []

    #loop through the pattern to find which terms are required to exist
    for i, val in enumerate(pattern):
        if val[1] == "#" or  val[1] == "+":
            #this item needs to exist
            requiredTerms.append(val[0])

    #Checking if there are any required terms in this pattern.
    if len(requiredTerms) > 0: 
        requiredTermsIntervals = getRequiredInterval(pattern, strand, requiredTerms)
        intervals = getRequiredTerms(stripPattern(pattern), strand, requiredTermsIntervals)

        #List of intervals that will be returned as the final matched intervals
        finalIntervals = []

        #If any matches of the requiredTerms where found
        if intervals != None:
            #getting the optional terms before and after the main matched pattern
            leadingPattern = getLeadingOptionalTerms(pattern)
            trailingPattern = getTrailingOptionalTerms(pattern)

            #Keeps track of the End of last matched pattern
            endOfLastMatched = 0

            for term in intervals:
                optionalTermsData = getOptionalTermMatchInput(term, requiredTermsIntervals, pattern)

                #Variable to check if loop was able to match every optional 
                #Pattern section legally (so that it maintains a matched pattern)
                matchedOptionalLegally = True
                
                if optionalTermsData != None:
                    for subterm in optionalTermsData:
                       newStrand = strand[subterm[0]:subterm[1] + 1]
                       result = matchPattern(subterm[2],newStrand)

                       #verifying that the length of the result is 1 (1 match)
                       if result != None and len(result) == 1 and result[0][1] - result[0][0] == len(newStrand) - 1:
                           pass
                       else:
                           #Note: this needs to be replaced with a better failing mechanism
                           #Because if one single intermediate spot fails, the whole match fails
                           matchedOptionalLegally = False
                           break

                if matchedOptionalLegally:
                    #Matching before and after the main match
                    newStart = term[0]
                    newEnd = term[1]
                    if leadingPattern != None:
                        #Start the matching on strand from end of last matched pattern
                        startFrom = endOfLastMatched

                        #Matching the leading pattern on the part of the strand before this match
                        leadingMatch = matchPattern(leadingPattern, strand[startFrom:term[0]])

                        if leadingMatch != None and leadingMatch[-1][1] == term[0] - startFrom - 1:
                            newStart = term[0] - (leadingMatch[-1][1] - leadingMatch[-1][0] + 1)
                    if trailingPattern != None:
                        #Matching trailing pattern on part after strand
                        trailingMatch = matchPattern(trailingPattern, strand[(term[1] + 1):len(strand)])

                        if trailingMatch != None and trailingMatch[0][0] == 0:
                            newEnd = term[1] + (trailingMatch[0][1] - trailingMatch[0][0] + 1)


                    #Setting the variable to be the end of this new match
                    endOfLastMatched = newEnd + 1

                    #Appending this interval to the final intervals list
                    finalIntervals.append([newStart, newEnd])


        #Return the final list of intervals
        if len(finalIntervals) == 0:
            return None
        return finalIntervals

    else:
        return matchAllOptionalTerms(pattern, strand)


#Function that gets the pattern of optional terms that occur before the required terms
def getLeadingOptionalTerms(pattern):
    subPattern = []
    for patternTerm in pattern:
        #If loop found a required term
        if patternTerm[1] == "#" or patternTerm[1] == "+":
            #Then end the loop, which will cause function to return
            break
        else:
            subPattern.append(patternTerm)
    if len(subPattern) == 0:
        return None
    return subPattern

#Function that gets pattern of optional terms that occur after the requiredTerms
def getTrailingOptionalTerms(pattern):
    #Calls the inverse of this function on the inverse of the input, then inverses it
    result = getLeadingOptionalTerms(pattern[::-1])
    if result != None:
        return result[::-1]

#Takes in a pattern and returns a new pattern without any non required terms
def stripPattern(inputPattern):
    newPattern = []
    for term in inputPattern:
        if term[1] == "+" or term[1] == "#":
            newPattern.append(term)
    return newPattern

#Gets the strand to search on and the pattern to search with for all intervals
#of optional terms in the match
def getOptionalTermMatchInput(intervals, requiredTermsIntervals, pattern):
    #Want [[], [], [], []] where each sublist (one for each requiredTermInterval
    #[[1, 3, [PATTERN]], [7, 9, [PATTERN]], ... ] <= things to look at 
    
    #The list that will be returned, and hopefully renamed
    l = []

    #Gets an array of all intervals of optional terms with requiredTerm instance numbers
    #of the required terms that surround the optional term interval
    optionalTermIntervals = getOptionalTerms(requiredTermsIntervals, intervals[0], intervals[1])
    optionalTermsLength = len(optionalTermIntervals)
    #Variables to assit in finding the pattern terms for each optional
    #Term interval
    reqTermCounter = 0 #Counts the number of requiedTerms  
    previousTermIsBoundry = False #true if the last term is the start of the
                                #requiredTerm boundry
    workingList = []
    patterns = []

    #Looping through all of the terms in the pattern
    if optionalTermsLength > 0:
        for loc, term in enumerate(pattern):
            if term[1] == "#" or term [1] == "+":
                #if at a required term and working through a optional term interval
                if previousTermIsBoundry:
                    #adding the working list of pattern terms to the list of patterns
                    patterns.append(workingList)
                    l.append([optionalTermIntervals[0][0], optionalTermIntervals[0][1], workingList])

                    #Removing the first optionalTermInterval
                    optionalTermIntervals = optionalTermIntervals[1:]

                    #Need to terminate here or else the code below will try and look
                    #at the first eliment, which will not exist. 
                    if len(optionalTermIntervals) == 0:
                        return l

                    #resteting variables
                    previousTermIsBoundry == False
                    workingList = []
                        
                #checking if this term can be the start of the next optionalTerm interval
                if optionalTermIntervals[0][2] == reqTermCounter:
                    previousTermIsBoundry = True

                #incrementing the counter for requiredTerms
                reqTermCounter+=1
            #If currently in the middle of optionalTermInterval and is an optional term
            elif previousTermIsBoundry:
                #Add term to working list of patterns
                workingList.append(term)

    #Means something terrible has gone wrong
    if optionalTermsLength != len(patterns):
        print "Error! WTF!!?!?!?!"
    if len(l) == 0:
        return None
    return l
    
#Given a list of requiredTerms and their intervals, determine the intervals of non required terms
#Over the span of a given interval of the list of required terms
def getOptionalTerms(requiredTermsIntervals, start, end):
    #Determine where in the strand the required terms start
    #Supposed to end up with a list L that contains all of the intervals 
    #That 

    #Optional Terms list that will be returned will contain 
    #Format for one of the terms: [a,b,c,d]
    #a: start location in the input string to match against
    #b: end location in the input string to match against
    #c: leading required term boundry instance of the pattern 
    #d: terminating required term boundry instance of the pattern 
    #in other words, c and d mark the two required terms that confine the space of the pattern
    #to look at
    optionalTerms = []

    #variable to keep track of the end of the last seen interval
    lastSeen = None

    #Keeps track of number of terms before the important interval actually starts
    #(where the pattern would start counting) this is because later, when looping
    #through the pattern, it will count from the start of where the match is, which may be offset
    #of the start of the requiredTermsIntervals
    untrackedTerms = 0

    for loc, i in enumerate(requiredTermsIntervals):
        #Checking if the current location is in the given confined space. 
        if start <= i[1] and end >= i[0]:
            #checking if the last seen term, exists, and has a non required term in between
            #such that the end of the previous interval is not 1 less than the start of
            #this interval
            if lastSeen != None and lastSeen <= i[0] - 2:
                #a proper match of an optional term interval was found. adding new
                #interval to the list of intervals
                optionalTerms.append([lastSeen + 1, i[0] - 1, loc - 1 - untrackedTerms, loc - untrackedTerms])
            #updating the last seen end of interval to be the end of this interval
            lastSeen = i[1]
        elif start > i[1]:
            #Keeping track of the number of required terms seen before the matching starts
            untrackedTerms += 1

               
    return optionalTerms

def getRequiredInterval(pattern, strand, requiredTerms):
    #getting a list of intervals of required terms [start, end, 'NAME']
    l = []
    lastTerm = None
    startInterval = -1
    endInterval = -1
    for i, word in enumerate(strand):
        if word in requiredTerms:
            if lastTerm == None:
                startInterval = i
                endInterval = i
                lastTerm = word
            elif lastTerm == word:
                endInterval += 1
            else:
                l.append([startInterval, endInterval, lastTerm])
                startInterval = i
                endInterval = i
                lastTerm = word
    
    #Adding the last interval to the list
    l.append([startInterval, endInterval, lastTerm])

    return l

def getRequiredTerms(oldPattern, strand, termsIntervals):
    #Here we will iterate through the list of required terms that have occured
    #and try to find a match of required terms in an order that satisfies the pattern.
   
    #Looping through the termsIntervals
    #Important Notes to make this thing completely work:
    #If I see ['N', '*'], ['N', '#'] => ['N', '+'] 
    #I can simplify other things like this
    i = 0
    val = None
    patternIntervalLocation = 0
    startInterval = -1
    endInterval = -1
    patternClone = list(oldPattern)
    searchResult = None
    intervals = []
    while i < len(termsIntervals):
        searchResult = False
        val = termsIntervals[i]
        
        #checking if this term in the pattern is a * term, if it is, remove it.
        #while len(patternClone) > 0 and patternClone[0][1] == "*":
        #   patternClone = patternClone[1:len(patternClone)]

        #checking if the match has started at all
        if startInterval == -1: #Match has not started
            #if the current term is the first term in the pattern
            if len(patternClone) == 0:
                searchResult = None
            elif val[2] == patternClone[0][0]:
                #Checking to see if the patterns match up properly
                #If at least one Item required:
                if patternClone[0][1] == "+":
                    #Gaurenteed to match pattern
                    startInterval = val[0]
                    endInterval = val[0]
                    patternClone = patternClone[1:len(patternClone)]
                #Checking if one term required, and one term in interval
                elif patternClone[0][1] == '#' and val[0] == val[1]:
                    #One instance of this term, with 1 term needed. Matches
                    startInterval = val[1]
                    endInterval = val[1]
                    patternClone = patternClone[1:len(patternClone)]
                #Checking if one term required, yet matched a range
                elif patternClone[0][1] == '#' and val[0] < val[1]:
                    #A '#' term was matched with an interval of that term.
                    #Use the last of that term.
                    startInterval = val[1]
                    endInterval = val[1]
                    patternClone = patternClone[1:len(patternClone)]
                else:
                    #This should not come up.
                    print "Error! Why is this case happening?!?!?!"

        #Partway through an interval
        else:
            #Checking if it matched the proper term
            if len(patternClone) == 0:
                #Standard Finish
                searchResult = [startInterval, endInterval]
            elif val[2] == patternClone[0][0]:
                #Checking if this term only needs atleast one to match
                if patternClone[0][1] == "+":
                    endInterval = val[1]
                    patternClone = patternClone[1:len(patternClone)]
                #Checking if needs exactly one term and matched one term long
                elif patternClone[0][1] == "#" and val[0] == val[1]:
                    #Matched another term successfully
                    endInterval = val[1]
                    patternClone = patternClone[1:len(patternClone)]
                #needs exactly one term, yet more than one of that item occured
                elif patternClone[0][1] == "#" and val[0] != val[1]:
                    #At this point it could succeed or fail 
                    #If this is the last term in pattern => Succeed
                    if len(patternClone) == 1:
                        #Returning the interval
                        searchResult = [startInterval, val[0]]

                    #If this is not the last term in the pattern => Fail
                    else:
                        #More terms in pattern to match => Fail
                        searchResult = None
            else:
                #Did not match the right term. Match Fails
                searchResult = None #Note: In the future, this will try to 

        #Adding succesful Intervals to the list of intervals, and reseting the search
        #To the appropriate locaiton

        #If the last search failed
        if searchResult != None and searchResult != False:
            #Adding the seach interval to the list of intervals
            intervals.append(searchResult)

        if searchResult != False:
            #Reseting the search at a new location
            newLocation = i - 1     #Starts location from same point (offsets loop incrementation
                                #Below). This section will be replaced by a more complex
                                #system where it will go to the earliest possible
                                #starting position to search from
            #Reseting all of the variables used in the loop to the origional state
            #they were in at the start of the loop
            patternIntervalLocation = 0
            startInterval = -1
            endInterval = -1
            patternClone = list(oldPattern)

            #Setting i to the new loop location
            i = newLocation

        #Incrementing i for the loop
        i+=1

    #End of loop. Checking if an interval was found succesfully at end of input
    if len(patternClone) == 0 and startInterval != -1 and endInterval != -1:
        intervals.append([startInterval, endInterval])

    if len(intervals) > 0:
        return intervals
    else:
        return None


def matchAllOptionalTerms(pattern, strand):
    #No required Terms given in this pattern (base case of recursive function)
    #Everything is a star matching pattern

    #Variables for keeping track of what the start terms are and according location in
    #the pattern list of where to goto if a match is found.
    #How this system works:
    #At any given point while looping through all of the words in the strand, the list
    #startTerms contains a series of strings that can occur for the pattern to still
    #be matched. the according list termLocations is an equally lengthed list of numbers
    #that correspond to a term in the startTerms list in the same spot, that gives the location
    #in the pattern array to goto if that term is matched in the strand. Note: this second
    #array is not needed until it is dealing with more complex patterns
    startTerms = []
    termLocations = []

    #loop through the pattern and figure out what all of the "starts" of each term are
    for loc, val in enumerate(pattern):
        startTerms.append(val[0])
        termLocations.append(loc)

    #Creating clones of startTerms and termLocations to be used in the loop below
    #Copies are needed so that it they can be restored part way through the loop,
    #so it can try to match multiple instances of the pattern
    workingStartTerms = list(startTerms)
    workingTermLocations = list(termLocations)

    #Variables for determining the interval of the pattern
    startLocation = -1
    endLocation = -1

    #List that contains intervals of where the pattern has been matched
    matchIntervals = []

    #Looping through the stand (input string) and determining where the pattern can be matched
    i = 0
    val = None
    while i < len(strand): #Using a while loop so that the counter i can be modified.
        val = strand[i]
    #for i, val in enumerate(strand):
        #variable where the location in the startTerms list the val is in
        loc = -1

        #Checking if this term is in the startTerms, and determining it's location
        for n in range(0, len(workingStartTerms)):
            if val == workingStartTerms[n]:
                loc = n
        #if val is in strand
        if loc != -1:
            #checking if this is the first match of the pattern
            if startLocation == -1:
                #Settin the startLocation of the interval to currentLocation
                startLocation = i
                endLocation = i
            else:
                #incrementing the endLocation of the current interval
                endLocation = i

            #Modifying the startTerms list accordingly
            workingStartTerms = workingStartTerms[loc:len(workingStartTerms)]
            workingTermLocations = workingTermLocations[loc:len(workingTermLocations)]

        #val was not in the strand
        else:
            #If no term was matched in the pattern and a pattern has started
            if startLocation != -1:
                #Pattern has ended

                #Add this interval to the list of intervals
                matchIntervals.append([startLocation, endLocation])
                
                #Reseting startLocation and endLocation
                startLocation = -1
                endLocation = -1

                #Reseting startTerms and termLocations
                workingStartTerms = list(startTerms)
                workingTermLocations = list(termLocations)

                #Decrementing i so that the matching system has a chance to start the 
                #Match over again at the same point
                i-=1

        #Incrementing the counter for the main loop
        i+=1
    #Adding the final interval to the list of intervals    
    if startLocation != -1:
        matchIntervals.append([startLocation, endLocation])

    #Returning the array of intervals if atleast one match, or None if no match
    if len(matchIntervals) > 0:
        return matchIntervals
    else:
        return None
