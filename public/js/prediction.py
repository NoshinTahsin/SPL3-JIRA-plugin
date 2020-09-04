import json
import nltk
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#stemming
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
 
#for word in input_str:
 #   print(lemmatizer.lemmatize(word))

with open('G:/jumble-jira/issue-data-jumble.json') as f:
  data = json.load(f)

num_of_projects=len(data["projects"])
print(num_of_projects)

for i in range(0,num_of_projects):
    print(data["projects"][i]['name'])
    print(len(data["projects"][i]['issues']))
    #print(data["projects"][i]['description'])
    #print(data["projects"][i]['type'])
    #print(data["projects"][i]['components'])
    
import re
import string 
def remove_punctuation(text):
    no_punc = "".join([c for c in text if c not in string.punctuation])
    return no_punc.lower()

def tokenize(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    porter_stemmer= PorterStemmer()
    lemmatizer=WordNetLemmatizer()

    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    terms_list = []
    #stemmed_sentence = []

    #Stemming is a little more aggressive. It cuts off prefixes and/or endings of words
    #based on common ones. It can sometimes be helpful, but not always because often times 
    #the new word is so much a root that it loses its actual meaning. 
    #Lemmatizing, on the other hand, maps common words into one base. 
    #Unlike stemming though, it always still returns a proper word that can be found in the dictionary.
    for w in word_tokens:
        if w not in stop_words:
            #w=porter_stemmer.stem(w)
            w=lemmatizer.lemmatize(w)
            terms_list.append(w)

    #print(word_tokens)
    #print("terms list")
    #print(terms_list)
    
    return terms_list

cnt=0
assignee_terms_map={}
terms_assignee_map={}
terms_assignee_list=[]

for i in range(0,num_of_projects):
    num_of_issues=len(data["projects"][i]['issues'])
    for j in range(0,num_of_issues):
        #if i!=0 or j!=14:
        issue = data["projects"][i]['issues'][j]
            
        if 'assignee' in issue and issue['assignee']!=None:
            print(cnt)
            cnt+=1
            i_id = issue['externalId']
            summary = issue['summary']
            des = issue['description']
            assignee = issue['assignee']
        
            des=remove_punctuation(des)
 
            bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
            des = ''.join(i for i in des if not i in bad_chars)
            #print(des)
            tokenized_des=tokenize(des)
        
            summary=remove_punctuation(summary)
 
            bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
            summary = ''.join(i for i in summary if not i in bad_chars)
            #print(summary)
            tokenized_summary=tokenize(summary)
            #print(i_id)
            #print(tokenized_des)
            #print(tokenized_summary)
            
            #list of all terms existing in an issue
            dupli_terms=tokenized_des+tokenized_summary
            #print(dupli_terms)
            
            terms = list(dict.fromkeys(dupli_terms))
            print(terms) 
            
            #print(assignee)
            #print(terms)
            if assignee in assignee_terms_map:
                assignee_terms_map[assignee]=assignee_terms_map[assignee]+terms
            else:
                assignee_terms_map[assignee]=terms
    
            terms_assignee_list.append(assignee)
        
            for term in terms:
                if term in terms_assignee_map:
                    terms_assignee_map[term]=terms_assignee_map[term]+terms_assignee_list
                else:
                    terms_assignee_map[term]=terms_assignee_list  
                    
            terms_assignee_list=[]

print(assignee_terms_map)
#print(terms_assignee_map)

print(len(assignee_terms_map))
available_devlist=[]

for key,val in assignee_terms_map.items():
    available_devlist.append(key)
print(available_devlist) 
#del assignee_terms_map["None"]
for key,val in  assignee_terms_map.items():
    print(key, "=>", val)
    #print(key)
    #print(len(val))   

#now i have mapped the assignee ans terms
#now need to map term => dev
print(len(terms_assignee_map))
add=0
for key,val in  terms_assignee_map.items():
    print(key, "=>", val)
    print(len(val))
    #add=add+len(val)
    #print(add)
    
#1347 unique terms??

#did nothing for sparse terms - that occur less frequently
#nltk.download('wordnet')
print(len(terms_assignee_map['driver']))
for i in range (0,10):
    print(terms_assignee_map['driver'][i])

#d={}
#d['a']='b'
#d['a']= 
#d['a']=[d['a'],'d']
#print(d)
#print(data["projects"][0]['issues'][14]['assignee'])
#print(data["projects"][0]['issues'][14]['externalId'])
#print(data["projects"][0]['issues'][14]['summary'])
#print(data["projects"][0]['issues'][14]['description'])

#tokenizing the new issue
new_des=data["projects"][0]['issues'][14]['description']
new_des=remove_punctuation(new_des)
bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
new_des = ''.join(i for i in new_des if not i in bad_chars)
tokenized_new_des=tokenize(new_des)

new_summary=data["projects"][0]['issues'][14]['description']
new_summary=remove_punctuation(new_summary)
bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
new_summary = ''.join(i for i in new_summary if not i in bad_chars)
tokenized_new_summary=tokenize(new_summary)

new_terms=tokenized_new_des+tokenized_new_summary
print(new_terms)

#now i have the new issue terms

#now calculate score for developer suggestion
print(len(new_terms))
newterm_dev_map={}
#def getDevTermUsageInfo():
cnt=0
for newterm in new_terms:
    if newterm in terms_assignee_map:
        print(cnt)
        cnt=cnt+1
        print(newterm)
        print(terms_assignee_map[newterm])
        newterm_dev_map[newterm]=terms_assignee_map[newterm]
        #returns a devlist for a single newterm
        #developers who has previously worked on that term
        #one dev name can occur multiple times
        #which implies he has worked on that term multiple times-more experienced!

#print(newterm_dev_map['everything'])
    
dev_termInfo={}

for dev in available_devlist:
    #print(dev)
    term_info={}
    #check if he has used a newterm and get the newterm
    for key in newterm_dev_map:
        if dev in newterm_dev_map[key]:
            #now i need the key-key is the newterm
            #calculate term info for the key
            #just need the fixfrequency
            #how many times dev is in newterm_dev_map[key]
            devnames=newterm_dev_map[key]
            #print(devnames)
            dev_count=devnames.count(dev)
            #print(key)
            #print(dev_count)
            term_info[key]=dev_count
            
    dev_termInfo[dev]=term_info

for key,value in dev_termInfo.items():
    print(key," => ",value)
    
#now i have the complex map of dev term term-info

prediction_list=[]

def devFixFreq(term):
    dev_use_count=0
    for dev in assignee_terms_map:
        terms_used=assignee_terms_map[dev]
        if term in terms_used:
            dev_use_count=dev_use_count+1
    return dev_use_count
    
dev_score={} 
for key in dev_termInfo:
    expertise=0
    termInfo=dev_termInfo[key]
    #print(termInfo)
    for info_term in termInfo:
        term_freq=termInfo[info_term]
        #print(info_term)
        #print(term_freq)
        ##dev=number of devs in the project 
        #len(available_devlist)
        
        #devfixfreq() : returns numof devs who fixed the term related bugs
        num_of_devs=len(available_devlist)
        tfIdf=term_freq*math.log(num_of_devs/devFixFreq(info_term))
        expertise+=tfIdf
    #end of for
    dev_score[key]=expertise
#end of for
print(dev_score)
    
sorted_dev_score = sorted(dev_score.items() , reverse=True, key=lambda x: x[1])
# Iterate over the sorted sequence
for elem in sorted_dev_score :
    print(elem[0] , " ::" , elem[1] )

for i in range (0,5):
    print(sorted_dev_score[i][0])