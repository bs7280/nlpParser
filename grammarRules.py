#GrammarRules.py


#Format for grammar rules:
#[Rule to match,Replacement]
#rule to match: (is a list of lists)
#   [[], [], [], []]
#   In each list: 
#       Either two strings: ["DET", "*"]
#       where the first string is the term to match, and the second is 
#       an indicator of how to match it (in this case it means any number of DET
#       or a list and a string [[], "*"]
#       where the contents of the list is another pattern to match
#
#what the indicator symbols mean:
#   *     Any number of
#   #     Exactly One
#   +     One or more

#A list of grammar rules, each item in the list contains a list with two strings:
#the first being the pattern to match, the second being the thing to replace it with.
simpleGrammar = [    #This simple grammar is only for declarative sentances
    ["SUBJECT PREDICATE", "S"],
    ["NP", "SUBJECT"],
    ["VP NP", "PREDICATE"],
    [[["DET","#"], [[["ADV", "*"], ["ADJ", "#"]],"*"], ["N", "+"]], "NP"],
    [[["DET", "#"], ["ADJ", "*"], ["N", "+"]], "NP"],
    [[["ADV", "*"], ["ADJ", "*"]], "TEST"],
    [[["N", "+"], ["D", "#"], ['N', '#'], ['D', '+' ]], "NP"],
    [[["A", "#"], ["B", "#"], ["A", "+"], ["B", "#"], ["A", "#"], ["B", "#"]], "NP"],
    [[["DET", "#"], ["ADV", "*"], ["ADJ", "*"], ["N", "+"]], "NP"],
    [[["DET", "#"], ["ADV", "*"], ["N", "#"], ["ADJ", "*"], ["DET", "#"]], "NP"], 
    [[["ADJ", "*"], ["DET", "#"], ["N", "#"], ["ADJ", "*"]], "NP"], 
    [[["ADJ", "*"], ["ADV", "*"], ["DET", "#"], ["N", "#"], ["ADV", "*"], ["ADJ", "*"]], "NP"], 
    [[["NP", "#"], ["Z", "*"]], "SUBJ"],
    ["(V|LVERB) COMPLIMENT", "VP"]
        ]

#The first grammar model for actual use with the parser
basicGrammar = [
        [[["Subject", "#"], ["Predicate", "#"]], "Sentance"],
        [[["VP", "#"], ["NP", "#"]], "Predicate"],
        [[["LVERB", "#"]], "VP"],
        [[["NP", "#"]], "Subject"],
        [[["DET", "#"], ["ADJ", "*"], ["N", "+"]], "NP"]
        ]
#######################################################
#####Establishing the parts of the complex grammar#####
#######################################################

#Grammar rules for the noun phrase
nounPhrase = [
            [[["DET", "#"], ["ADJ", "*"], ["N", "+"]], "NP"]
        ]

verbPhrase = [
            [[["LVERB", "#"]], "VP"]
        ]

metaSentance = [
            [[["Subject", "#"], ["Predicate", "#"]], "Declarative Sentance"],
            [[["VP", "#"], ["NP", "#"]], "Predicate"],
            [[["NP", "#"]], "Subject"]
        ]

sentance = [
            [[["Declarative Sentance", "#"]], "Sentance"]
        ]

complexGrammar = [
        [nounPhrase, verbPhrase, metaSentance, sentance]
        ]
