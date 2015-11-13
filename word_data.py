import linecache
import re
from classes import word
from grammar_exceptions import exceptions
wordnetfile="wordnet/index.sense"

#dictionary defining swaps for POS inputs and the pos that will be used in
#this program
posSwaps = {"Noun": "N", "Verb" : "V", "Adj": "ADJ", "Adv": "ADV"}

#this functiom uses a binary search to look for the given word in the
#wordnet index.sense file. It returns an array in the format of [word (Pos) [count], ...]
#in a list
def searchForWord(searchword):
    searchword=searchword.replace(" ","_")
    minline=1
    maxline=206941
    found=False
    linenum=0
    words=[]
    while True:
        if linenum==(minline+maxline)/2:
            return False
        linenum=(minline+maxline)/2
        line=linecache.getline(wordnetfile,linenum).strip("\n")
        testword=re.sub("%.*","",line)
        if searchword.lower()==testword.lower():
            words.append(word(line))
            break
        if searchword.lower()<testword.lower():
            maxline=linenum
        if searchword.lower()>testword.lower():
            minline=linenum
    foundlinenum=linenum
    while True:
        linenum+=1
        line=linecache.getline(wordnetfile,linenum).strip("\n")
        testword=re.sub("%.*","",line)   
        if searchword.lower()==testword.lower():
            words.append(word(line))
        else:
            break
    linenum=foundlinenum
    while True:
        linenum-=1
        line=linecache.getline(wordnetfile,linenum).strip("\n")
        testword=re.sub("%.*","",line)   
        if searchword.lower()==testword.lower():
            words.insert(0,word(line))
        else:
            break
    return words

#functiont that takes output from searchforward and returns it in a more 
#useful format. This is the most basic version that will return a list with
#each according part of speach and the percentage change of occurance
def simpleWordData(input): #the parameter input is in the form of a list of
  if input == False:       #Word class objects
    return False

  output = []
  total = 0.0
  for e in input: #looping through all the words in the input
    foundSpot = 0
    for pos in output: #looping through all the spots in the output
      if pos[0] == e.pos:
        pos[1] += e.cnt
        total = total + e.cnt
        foundSpot = 1
    if foundSpot == 0:
      output.append([e.pos, e.cnt])
      total = total + e.cnt

  #Converting the counts to percentages
  for i in range(0, len(output)):
    output[i][1] = output[i][1]/total

  return output

def getSimpleWordData(word):
  #checking if the word is a specified grammar exception
  exception = checkExceptions(word)
  if exception != False:
    return exception
  else:
    return simpleWordData(searchForWord(word))

#function that takes a pos in and outputs the standard naming use
#part of speach for this program
def convertPos(input):
  if posSwaps.has_key(input): 
    return posSwaps[input] 
  else:
    return input

#funciton that checks the list of non standard parts of speech like the word
#the, and, on, etc.... takes a word as input and returns either false or the
#part of speech as an array, with probability of 1.0, like what returns from
#the function simpleWordData
def checkExceptions(word):
  for e in exceptions:
    pos = e[0]
    for w in e[1]:
      if w == word.lower():
        return [[pos, 1.0]]
  return False



