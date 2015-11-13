#This is a python file that is ultimately responsible for taking in a sentance,
#and getting all of the word information from the wordnet.py module then returning
# a list of all of the possible sentance combinations with the different combinations
#of parts of speach.

import word_data

#function that takes in a sentance as a string and returnd all the possible 
#combinations of sentances for all of the differnt combinations of Parts of speech
#in order of probablity
def getSentanceCombos(sentance):
  #Splitting up the sentance into different base sentances by splitting at
  #some spaces and not splitting at others. gives a list of sentances in the form
  #where each item in the list is a list of words

  #for now I will just assume every space is a seperator
  sentance_combinations = [sentance.split(" ")]

  #loop through all of the words and split each possible sentance into 
  #a list of combinations of possible parts of speach
  tag_combos = [[[], 1.0]]
  for sentance in sentance_combinations:
    for word in sentance:
      #getting a list of all the possible parts of speech for the given word
      tags = word_data.getSimpleWordData(word)
    
      #checking if the word returned with data
      #if not, then no data on the word, so we can quit the sentance
      if tags == False:
        return False 

      #list to store the new tag combos
      new_tag_combos = []
      

      #loop through possible tags
      for tag in tags:
        #for each of those, loop though all of the already existing tag combos
        tmp_tag_combos = tag_combos[:]
        for combo in tmp_tag_combos:
            a = [combo[0]+[tag[0]], combo[1]*tag[1]]

            new_tag_combos.append(a)
      tag_combos = new_tag_combos

  #Sort the list of tag_combos
  if(tag_combos != False): #checks if the tag combos are not false
    return sortTagCombos(tag_combos)

  return tag_combos
  sentance_combinations
  
#Function to sort the tag combos on probablility
def sortTagCombos(inputCombos):
    newList = []

    #variables for implementing the selection sort
    for n in range(0, len(inputCombos)):
        largestValue = 0.0
        largestComboLocation = -1
        for combo_loc in range(0, len(inputCombos)):
            combo = inputCombos[combo_loc]
            if combo[1] > largestValue:
                largestValue = combo[1]
                largestComboLocation = combo_loc
        newList.append(inputCombos[largestComboLocation])
        inputCombos.remove(inputCombos[largestComboLocation])
    return newList
        
