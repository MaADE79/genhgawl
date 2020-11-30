#!/usr/bin/python
#########################################################################################################
# Generator for homographic attack wordlists                                                            #
#                                                                                                       #
# Needs substutition rule as cslst-File                                                                 #
#                                                                                                       #
# Usage:                                                                                                #
#    genhgawl.py [options]                                                                              #
#                                                                                                       #
#        Options:                                                                                       #
#            -w <single word> or -f <file with words>                                                   #
#            -o <outputfile>                                                                            #
#            -cslst <substitutions to use>                                                              # 
#                                                                                                       #
# (c) by Mathias Aust, M.Sc.                                                                            #
#     contact: MaA_DE79@gmx.com                                                                         #
#                                                                                                       #
#                                                                                                       #
#########################################################################################################

from math import pow
import sys

def substitude(inString, inChar, inSubChar):
    # Indexing character
    lFound = []
    loc = -1;
    while True:
        loc = inString.find(inChar, loc + 1)
        if loc > -1:
            lFound.append(loc)
        else:
            break    
            
    # Manipulate String
    result = []
    max = int(2*(pow(2,len(lFound)-1)))
    for i in range(1, max):
        pattern = ("{0:0" + str(len(lFound)) + "b}").format(i)
        newList = list(inString)
        for j in range(0, len(pattern)): 
            if pattern[j]=="1":
                newList[lFound[j]] = inSubChar                
        result.append("".join(newList))        
    return result    
    

def generate(inList, inChar, inSubChar):
    array = []    
    if len(inList)>0:
        for string in inList:
            array += substitude(string, inChar, inSubChar)    
    return inList + array
    
    
def loadDictionary(inFile=""):    
    if len(inFile) == 0:
        dict = {"a":["4","@"], "o":["0"], "s":["5"], "i":["1"]}
    else:
        dict = {}        
        file = open(inFile,"r")
        dict = eval(file.read())
        file.close()
    return dict
    
    
def saveToFile(inArray, inFilename):
    file = open(inFilename, "w")
    for i in range(0, len(inArray)):        
        file.write(inArray[i])        
        file.write("\n")        
    file.close
    
def readFile(inFilename):
    result = []
    file = open(inFilename, "r")
    for line in file:        
        result.append(line.rstrip('\n')) 
    file.close
    return result

def generateHGAwordlist(inString="", inDictionary="", inFilename=""):    
    
    if not inFilename:
        inFilename= "{}_wordlist.txt".format(inString)
    
    dict = loadDictionary(inDictionary)
        
    print("String: {}".format(inString))
    
    array = inString;
    for key in dict:
        for word in dict[key]:
            array = generate(array, key, word)
    array.sort(reverse=True)    
    print("Created {} combinations".format(len(array)))    
    saveToFile(array, inFilename)

def getARGVValueByTag(inTag=""):
    value = ""
    if sys.argv:        
        for arg in  sys.argv:
            if arg.lower() == inTag.lower():
                value = sys.argv[sys.argv.index(arg)+1]        
                break
    return value

def main():

    print("homographic attack wordlists")
    print()    
    
    print("Given parameters")
    inFileName = getARGVValueByTag("-f")               
    print("inFileName = '{}'".format(inFileName)) 
        
    outFileName = getARGVValueByTag("-o")               
    print("outFileName = '{}'".format(outFileName)) 
    
    cslst = getARGVValueByTag("-cslst")
    if not cslst:
        cslst = "demo.cslst"
    print("cslst = '{}'".format(cslst)) 
    print() 
    
    if inFileName:
        words = readFile(inFileName)    
    else:
        words = []
        words.append("".join(getARGVValueByTag("-w")))
    
    if words[0]:
        generateHGAwordlist(words, cslst, outFileName)

if __name__ == '__main__':  
   main()