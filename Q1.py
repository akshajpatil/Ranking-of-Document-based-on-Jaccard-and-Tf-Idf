
# coding: utf-8

# In[37]:

import glob
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from num2words import num2words
lemmatizer=WordNetLemmatizer()
globalVocabulary=[]
dictWords={}
dictIdf={}
RdictIdf={}
direct = [f for f in glob.glob("E:/E/IIIT Delhi/IR/Assign 2/stories/stories/*", recursive=True)]
j=1
for files in direct:
    fileName=""
    listTokens=[]
    fileName=files[44:]
    #print(fileName)
    tokenizer = RegexpTokenizer(r'\w+')
    fileRead = open(files, "r",encoding="latin-1")
    input_string=fileRead.read().translate(str.maketrans("","",string.punctuation))
    input_str=word_tokenize(input_string.lower())
    stop_words = set(stopwords.words('english'))
    result = [i for i in input_str if not i in stop_words]
    result=[word.strip(string.punctuation) for word in result]
    
    
    for word in result:
        word=lemmatizer.lemmatize(word)
        if word.isdecimal():
            #print(fileName," ",word)
            listTokens.append(num2words(word))
            
        else:
            listTokens.append(word)
        globalVocabulary.append(word)
    
    
    tempListTokens=set(listTokens)
    for word in tempListTokens:
        if word not in RdictIdf:
            RdictIdf[word]=1
        else:
            RdictIdf[word]=RdictIdf[word]+1
    dictWords[fileName]=listTokens
    
    if j%20 == 0:
        print(j)
    j=j+1
#print(dictWords[fileName])
globalVocabulary=list(set(globalVocabulary))
print(len(globalVocabulary))


# In[38]:

import math
choiceIdf=input("Enter variation number 1/2: ")
#dictIdf=RdictIdf
dictIdf={}
for keys in RdictIdf:
    if choiceIdf == '1':
        dictIdf[keys]=len(direct)/(1+RdictIdf[keys])
    else:
        dictIdf[keys]=len(direct)/(1+RdictIdf[keys])
        dictIdf[keys]=math.log(dictIdf[keys],10)
print(len(dictIdf))
print(len(dictWords))


# In[39]:

fileTitle=open("E:/E/IIIT Delhi/IR/Assign 2/stories/stories/index.txt","r")
dictTitle={}
titleString=fileTitle.readlines()
print(titleString[0])
i=0
while i < (len(titleString)-1):
    titleTokensHead=titleString[i].lower().split("\t")
    #print(titleTokensHead)
    title_string=titleString[i+1].translate(str.maketrans("","",string.punctuation))
    titleTokens=tokenizer.tokenize(title_string.lower())
    #print(titleTokens)
    result = [i for i in titleTokens if not i in stop_words]
    titleList=[]    
    for word in result:
        titleList.append(lemmatizer.lemmatize(word))
    dictTitle[titleTokensHead[0]]=titleList
    i=i+2
print(len(dictTitle))


# In[40]:

import operator
def calculateJaccardScore():
    dictScoreJaccard={}
    keyList=dictWords.keys()
    for keys in keyList:
        lengthUnion=len(list(set(queryList) | set(dictWords[keys]) ))
        lengthIntersection=len(list(set(queryList) & set(dictWords[keys]) ))
        score=float(lengthIntersection/lengthUnion)
        dictScoreJaccard[keys]=score
    dictScoreJaccard = dict( sorted(dictScoreJaccard.items(), key=operator.itemgetter(1),reverse=True))  
    
    k=0
    for keys in dictScoreJaccard:
        if(k==15):
            break
        print(keys,": and Score= ",dictScoreJaccard[keys])
        k=k+1
        

def calculateTfIdf():
    dictScoreTfIdf={}
    choiceTf=input("Enter Varation of TF 1/2/3")
    for keys in dictWords:
        score=0
        for terms in queryList:
            if terms not in dictIdf.keys():
                dictIdf[terms]=0
            if choiceTf=='1':
                score=score+float(dictWords[keys].count(terms))*dictIdf[terms]
            elif choiceTf=='2':
                score=score+float((1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]
            else:
                score=score+float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]
            
        dictScoreTfIdf[keys]=score
        
    dictScoreTfIdf=dict( sorted(dictScoreTfIdf.items(), key=operator.itemgetter(1),reverse=True))
    
    k=0
    for keys in dictScoreTfIdf:
        if(k==15):
            break
        print(keys,": and Score= ",dictScoreTfIdf[keys])
        k=k+1

        
        
        
def calculateTfIdfTitle():
    dictScoreTfIdf={}
    choiceTf=input("Enter Varation of TF 1/2/3")
    for keys in dictWords:
        score=0
        for terms in queryList:
            if terms not in dictIdf.keys():
                dictIdf[terms]=0
            if keys not in dictTitle.keys():
                dictTitle[keys]=[]
            if terms in dictTitle[keys]:
                if choiceTf=='1':
                    score=score+float(dictWords[keys].count(terms))*dictIdf[terms]+(float(dictWords[keys].count(terms))*dictIdf[terms])/2
                elif choiceTf=='2':
                    score=score+float((1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]+(float((1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms])/2
                else:
                    score=score+float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]+(float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms])/2
            else:
                if choiceTf=='1':
                    score=score+float(dictWords[keys].count(terms))*dictIdf[terms]
                elif choiceTf=='2':
                    score=score+float((1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]
                else:
                    score=score+float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]

        dictScoreTfIdf[keys]=score
        
    dictScoreTfIdf=dict( sorted(dictScoreTfIdf.items(), key=operator.itemgetter(1),reverse=True))
    
    k=0
    for keys in dictScoreTfIdf:
        if(k==15):
            break
        print(keys,": and Score= ",dictScoreTfIdf[keys])
        k=k+1

        
        
def calculateCosineScore(queryVectorTemp,docVectorTemp):
    cosineScore=0
    deno1=0
    deno2=0
    for i in range(len(queryVectorTemp)):
        cosineScore=cosineScore+queryVectorTemp[i]*docVectorTemp[i]
    for nums in queryVectorTemp:
        deno1=deno1+nums*nums
    deno1=math.sqrt(deno1)
    for nums in docVectorTemp:
        deno2=deno2+nums*nums
    deno2=math.sqrt(deno2)
    deno1=deno1*deno2
    
    cosineScore=cosineScore/(deno1+1)
    return cosineScore


def calculateCosine():
    #print(queryList)
    dictScoreCosine={}
    for keys in dictWords:
        queryVector=[]
        docVector=[]
        cosineScore=0
        for terms in queryList:
            if terms not in dictIdf.keys():
                dictIdf[terms]=0
            scoreQuery=0
            scoreDoc=0
            if terms in dictTitle[keys]:
                scoreDoc=float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]+(float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms])/2
                scoreQuery=float(math.log(1+queryList.count(terms))/len(queryList))*dictIdf[terms]+(float(math.log(1+queryList.count(terms))/len(queryList))*dictIdf[terms])/2
            else:
                scoreDoc=float(math.log(1+dictWords[keys].count(terms))/len(dictWords[keys]))*dictIdf[terms]
                scoreQuery=float(math.log(1+queryList.count(terms))/len(queryList))*dictIdf[terms]
                
            queryVector.append(scoreQuery)
            docVector.append(scoreDoc)
        
        cosineScore=calculateCosineScore(queryVector,docVector)
        dictScoreCosine[keys]=cosineScore
        
    dictScoreCosine=dict( sorted(dictScoreCosine.items(), key=operator.itemgetter(1),reverse=True))
    
    k=0
    for keys in dictScoreCosine:
        if(k==15):
            break
        print(keys,": and Score= ",dictScoreCosine[keys])
        k=k+1
        
        
        


# In[44]:

choice=input("Enter Choice 1:Jaccard, 2:Tf-Idf, 3:Tf-Idf Title, 4:Cosine Similarity 5:Exit")
while choice !='5':
    query="The three little pigs started to feel they needed a real home"
    query=input("Enter Query: ")
    print(query)
    query=query.translate(str.maketrans("","",string.punctuation))
    query=word_tokenize(query.lower())
    result = [i for i in query if not i in stop_words]
    #result=query   
    queryList=[]  
    #result=[word.strip(string.punctuation) for word in result]
    for word in result:
        word=lemmatizer.lemmatize(word)
        if word.isdecimal():
            queryList.append(num2words(word))
        else:
            queryList.append(word)

    print("Querylist= ",queryList)

    if choice == '1':
        print("According to jaccard")
        calculateJaccardScore()
    elif choice=='2':
        print("\nAccordng to tf-idf")
        calculateTfIdf()
    elif choice=='3':
        print("\n According to tf-idf title")
        calculateTfIdfTitle()
    elif choice=='4':
        print("\nAccording to Cosine Similarity")
        calculateCosine()
    else:
        exit(1)
    choice=input("Enter Choice 1:Jaccard, 2:Tf-Idf, 3:Tf-Idf Title, 4:Cosine Similarity 5:Exit")


# In[ ]:



