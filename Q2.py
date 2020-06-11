
# coding: utf-8

# In[3]:

file=open("E:/E/IIIT Delhi/IR/Assign 2/english2/english2.txt")
dictionaryWords=file.read().split("\n")

print(len(dictionaryWords))


# In[4]:

import operator
def correctWords():
#     queryWord="variet"
#     dicWord="variety"

    for queryWord in missSpelledWords:
        dictNearWords={}
        total=0
        for dicWord in dictionaryWords:
            dp={}
#             i=-1
#             for letters in queryWord:
#                 dp[-1,i]=i
#                 i=i+1
#             i=-1
#             for letters in dicWord:
#                 dp[i,-1]=i
#                 i=i+1
#             i=0
#             j=0
            for i in range(len(queryWord)+1):
                for j in range(len(dicWord)+1):

                    if i==0:
                        dp[i,j]=j*2
                    elif j==0:
                        dp[i,j]=i*1

                    elif queryWord[i-1]==dicWord[j-1]:
                        dp[i,j]=dp[i-1,j-1]
                    else:
                        dp[i,j]=min(1+dp[i-1,j],2+dp[i,j-1],3+dp[i-1,j-1])
            #print(dicWord,"::")
            #print(dp[i,j])
            dictNearWords[dicWord]=dp[i,j]
        dictNearWords = dict( sorted(dictNearWords.items(), key=operator.itemgetter(1)))
        print("\nK nearest words of ",queryWord," are\n")
        k=0
        for words in dictNearWords.keys():
            print(words,": ",dictNearWords[words])
            if k==5:
                break
            k=k+1


# In[5]:

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
stop_words = set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()
#query=input("Enter query")
query="bello varietyy of flowers"
query=input("Enter Query")
query=query.translate(str.maketrans("","",string.punctuation))
query=word_tokenize(query.lower())
result = [i for i in query if not i in stop_words]

#result=query   
queryList=[]    
for word in result:
    queryList.append(lemmatizer.lemmatize(word))
missSpelledWords=[]
for words in queryList:
    if words not in dictionaryWords:
        missSpelledWords.append(words)
print(missSpelledWords)

correctWords()


# In[ ]:

# darray=[[0 for i in range(6)]for j in range(5)]
# print(darray[0][5])


# In[ ]:



