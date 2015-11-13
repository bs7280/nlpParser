import re

class word:
    def __init__(self,line):
        self.text=re.sub("%.*","",line)
        posdict={"1":"N","2":"V","3":"ADJ","4":"ADV","5":"ADJ"}
        self.pos=posdict[re.sub(":.*","",re.sub(".*%","",line))]
        self.cnt=int(re.sub(".* ","",line))+1
    def __repr__(self):
        return str(self)
    def __str__(self):
        return self.text+" ("+self.pos+") ["+str(self.cnt)+"]"
class phrase:
    def __init__(self,text,type):
        self.text=re.sub("%.*","",text,type)
        self.type=type
    def __repr__(self):
        return str(self)
    def __str__(self):
        return self.text+" ("+self.type+")"
