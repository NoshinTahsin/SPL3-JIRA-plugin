from flask import jsonify,Flask,render_template,request
from flask_cors import CORS
# from flask_restful import Resource, Api;
import json
import nltk
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#stemming
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import requests
from requests.auth import HTTPBasicAuth
 
#for word in input_str:
 #   print(lemmatizer.lemmatize(word))

app = Flask(__name__)

CORS(app)

from jira import JIRA
jira = JIRA(basic_auth=('bsse0914@iit.du.ac.bd', '0EkaiQ0u0Zw5nWJkI8iG0D65'), options={'server':'https://pg-req.atlassian.net'})

projects = jira.projects()
num_of_projects=len(projects)

issueCount=0
for i in range(0,num_of_projects):
    print(projects[i])
    issues_in_proj = jira.search_issues('project='+str(projects[i]))
    print(len(issues_in_proj))
    issueCount+=len(issues_in_proj)
print(issueCount)

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


@app.route("/", methods=['GET'])
def index():
 return "Welcome to CodezUp"

#@app.route("/ask/", methods=["POST"])
#def asked():
#    if request.method == "POST":
#        req = request.form
#        print("Key is"+req)

 #   return render_template("views/activity.hbs")


def data_processing():
    global assignee_terms_map
    assignee_terms_map = {}
    global terms_assignee_map
    terms_assignee_map={}
    global terms_assignee_list
    terms_assignee_list=[]
    global account_id_map
    account_id_map={}

    cnt=0
    for p in projects:
        pro_key='project='
        pro_key+=str(p.key)
        project_key=pro_key
        size = 100
        initial = 0
        issueCount=0
        while True:
            start= initial*size
            issues = jira.search_issues(project_key,  start,size)
            issueCount+=len(issues)
            if len(issues) == 0:
                break
            initial += 1
            for issue in issues:
                if issue.fields.assignee and issue.fields.assignee!=None:
                    cnt+=1
                    summary = issue.fields.summary
                    des = issue.fields.description
                    assignee = str(issue.fields.assignee)
                    account_id = str(issue.fields.assignee.accountId)
        
                    des=remove_punctuation(des)
 
                    bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
                    des = ''.join(i for i in des if not i in bad_chars)
                    tokenized_des=tokenize(des)
        
                    summary=remove_punctuation(summary)
 
                    bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
                    summary = ''.join(i for i in summary if not i in bad_chars)
                    tokenized_summary=tokenize(summary)
               
                    #list of all terms existing in an issue
                    dupli_terms=tokenized_des+tokenized_summary
            
                    terms = list(dict.fromkeys(dupli_terms))
                
                    keylist=[]
                    for key,val in assignee_terms_map.items():
                        keylist.append(key)
                                
                    if assignee in keylist:
                        assignee_terms_map[assignee]=assignee_terms_map[assignee]+terms
                    else:
                        assignee_terms_map[assignee]=terms
                        account_id_map[assignee]=account_id
    
                    terms_assignee_list.append(assignee)
        
                    for term in terms:
                        if term in terms_assignee_map:
                            terms_assignee_map[term]=terms_assignee_map[term]+terms_assignee_list
                        else:
                            terms_assignee_map[term]=terms_assignee_list  
                    
                    terms_assignee_list=[]

    print("Final map:")
    print(assignee_terms_map)

    print("Account ID map:")
    print(account_id_map)

    print(len(assignee_terms_map))
    global available_devlist
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
    print(terms_assignee_map)


def process_new_issue(key):
    global new_terms 
    global newterm_dev_map
    newterm_dev_map={}
    global dev_termInfo
    dev_termInfo={}
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%"+str(key))

    new_issue=jira.issue('SAAJ-7')
    new_des=new_issue.fields.description

    new_des=remove_punctuation(new_des)
    bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
    new_des = ''.join(i for i in new_des if not i in bad_chars)
    tokenized_new_des=tokenize(new_des)

    new_summary=new_issue.fields.summary

    new_summary=remove_punctuation(new_summary)
    bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
    new_summary = ''.join(i for i in new_summary if not i in bad_chars)
    tokenized_new_summary=tokenize(new_summary)

    new_terms=tokenized_new_des+tokenized_new_summary
    print(new_terms)

    #now i have the new issue terms
    cnt=0
    for newterm in new_terms:
        if newterm in terms_assignee_map:
            #print(cnt)
            cnt=cnt+1
            print(newterm)
            print(terms_assignee_map[newterm])
            newterm_dev_map[newterm]=terms_assignee_map[newterm]
            #returns a devlist for a single newterm
            #developers who has previously worked on that term
            #one dev name can occur multiple times
            #which implies he has worked on that term multiple times-more experienced!

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


def devFixFreq(term):
    dev_use_count=0
    for dev in assignee_terms_map:
        terms_used=assignee_terms_map[dev]
        if term in terms_used:
            dev_use_count=dev_use_count+1
    return dev_use_count

def calculate_devscore():
    
    global prediction_list
    prediction_list=[]
    global dev_score
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
    
    return sorted_dev_score


def getList():
    a=[]
    a_id=[]
    for i in range (0,len(sorted_dev_score)):
        a.append(sorted_dev_score[i][0])
        a_id.append(account_id_map[sorted_dev_score[i][0]])
        print(sorted_dev_score[i][0])
        print("Account ID")
        print(account_id_map[sorted_dev_score[i][0]])
        print("\n")

    print(a)
    print(a_id)
    
    a=a+a_id
    print(a)
    return a
    #return ["new-lucille.hogan-2","isabel.richardson","marsha.cook","joshua.maples","jerome.johnson"]

@app.route("/suggested/", methods = ['GET'])

def suggested():
    #global weather
    #global assignees
    #convert=conversion()
    #projectpath = request.form['projectFilepath']
    key=request.args.get('keyname')
    print(key)
    data_processing()
    process_new_issue(key)
    global sorted_dev_score
    sorted_dev_score = calculate_devscore()

    a=getList()
    return jsonify([a])
    #global assignees
    #convert=conversion()
    #return convert

#@app.route("/change/", methods = ['GET'])
@app.route("/change/", methods = ['PUT'])

def change():
    url = "https://pg-req.atlassian.net/rest/api/3/issue/SAAJ-8/assignee"

    auth = HTTPBasicAuth("bsse0914@iit.du.ac.bd", "0EkaiQ0u0Zw5nWJkI8iG0D65")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps( {
        "accountId": "5e299526bf04010e70c42927"
    } )

    response = requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    print(response.text)
    rt=response.text
    return rt


if __name__ == '__main__':
    app.run(debug=True)