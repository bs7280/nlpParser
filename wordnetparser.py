import linecache
import re
from classes import word
wordnetfile="index.sense"
def searchforword(searchword):
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
        print linenum
        print testword
        print word
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
