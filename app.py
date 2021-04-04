from flask import jsonify,Flask,render_template,request
#from werkzeug import secure_filename
from flask_cors import CORS
# from flask_restful import Resource, Api;
import os
import json
import nltk
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#stemming
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from jira import JIRA
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import pymongo
import re
import string 
import pandas as pd 
import time
from datetime import datetime, timedelta

#for word in input_str:
 #   print(lemmatizer.lemmatize(word))

app = Flask(__name__)

CORS(app)

jira = JIRA(basic_auth=('bsse0914@iit.du.ac.bd', '4MsH8F6gkCV3yMwY8ZHs8D47'), options={'server':'https://pg-req.atlassian.net'})
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["JiraPlugin"]

projects = jira.projects()
num_of_projects=len(projects)

issueCount=0
for i in range(0,num_of_projects):
    #print(projects[i])
    issues_in_proj = jira.search_issues('project='+str(projects[i]))
    #print(len(issues_in_proj))
    issueCount+=len(issues_in_proj)
#print(issueCount)

def remove_punctuation(text):
    no_punc = "".join([c for c in text if c not in string.punctuation])
    return no_punc.lower()

def tokenize(text):

    pattern = r'[0-9]'
    # Match all digits in the string and replace them by empty string
    text = re.sub(pattern, '', text)
    #print(text)
    text = text.replace("'", "")
    text = text.replace('"', "")

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


global db_assignee_terms_list 
db_assignee_terms_list = []
global db_assignee_list 
db_assignee_list = []
global db_terms_assignee_list 
db_terms_assignee_list = []
#suggestions collection
fetched_available_devlist = []
fetched_terms_assignee_map = {}
fetched_assignee_terms_map = {}
fetched_account_id_map = {}
now = datetime.now()
new_issue_creation_date = now.strftime("%Y-%m-%d %H:%M:%S")


def data_processing():
    global assignee_terms_map
    assignee_terms_map = {}
    global terms_assignee_map
    terms_assignee_map={}
    global terms_assignee_list
    terms_assignee_list=[]
    global account_id_map
    account_id_map={}

    projects = jira.projects()
    num_of_projects=len(projects)
    issueCount=0
    for i in range(0,num_of_projects):
        #print(projects[i])
        #jql
        issues_in_proj = jira.search_issues('project='+str(projects[i]))
        #print(len(issues_in_proj))
        issueCount+=len(issues_in_proj)
    #print(issueCount)
    
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
                    
                    creation_date = str(issue.fields.created)
                    creation_date = datetime.strptime(creation_date[:19], "%Y-%m-%dT%H:%M:%S")
            
                    assignee_date = {}
                    assignee_date['assignee']=assignee
                    assignee_date['date']=creation_date
        
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
    
                    terms_assignee_list.append(assignee_date)
        
                    for term in terms:
                        if term in terms_assignee_map:
                            terms_assignee_map[term]=terms_assignee_map[term]+terms_assignee_list
                        else:
                            terms_assignee_map[term]=terms_assignee_list  
                                        
                terms_assignee_list=[]

    #print("Final map:")
    #print(assignee_terms_map)
    
    #print("Final terms assignee map:")
    #print(terms_assignee_map)

    #print("Account ID map:")
    #print(account_id_map)

    #print(len(assignee_terms_map))
    global available_devlist
    available_devlist=[]

    for key,val in assignee_terms_map.items():
        available_devlist.append(key)
    #print(available_devlist) 
    #del assignee_terms_map["None"]
    for key,val in  assignee_terms_map.items():
        print(key, "=>", val)
        #print(key)
        #print(len(val))   
    #now i have mapped the assignee ans terms
    #now need to map term => dev
    #print(len(terms_assignee_map))
    add=0
    #print(terms_assignee_map)
    
    for key in account_id_map:
        temp_dict={}
        temp_dict['name'] = key
        temp_dict['assignee_id'] = account_id_map[key]
        db_assignee_list.append(temp_dict)

    #print("db_assignee_list: ")
    #print(db_assignee_list)
    
    #mongo - collection - assignee
    #{'name': 'Moumita Asad', 'assignee_id': '5f5764e4bea5be0068101b9a'}
    mycol = mydb["Assignee"]

    if mycol.count_documents({})>0:
        for i in range(0,len(db_assignee_list)):
            myquery = {}
            myquery["name"] = db_assignee_list[i]["name"]
            
            mydoc = mycol.find(myquery)
            if(mydoc.count()>0):
                print("Entry exists")
                
            else:
                #print("Entry doesn't exist")
                mydict = {}
                mydict["name"] = myquery["name"]
                mydict["assignee_id"] = db_assignee_list[i]["assignee_id"]
                x = mycol.insert_one(mydict)

    else:
        #print("No document yet in this collection.")
        #mydict = {}
        #mydict["name"] = db_assignee_list[i]["name"]
        #mydict["assignee_id"] = db_assignee_list[i]["assignee_id"]
        x = mycol.insert_many(db_assignee_list)
    
    #check if query exists, if not then create one 

    #print "Assignee" after the update:
    #for x in mycol.find():
        #print(x)
        
    #assignee_terms_map - dictionary
    #{'Moumita Asad': ['write', 'icse', 'paper'], 'Noshin Tahsin': ['regression','atlassian']}
    #for db insertion i need a list of individual dictionaries

    for key in assignee_terms_map:
        temp_dict={}
        temp_dict['name'] = key
        temp_dict['terms'] = assignee_terms_map[key]
        db_assignee_terms_list.append(temp_dict)

    #print("db_assignee_terms_list: ")
    #print(db_assignee_terms_list)

    #mongo - collection - AssigneeTermsMap
    #{'name': 'Moumita Asad', 'terms': '['write', 'icse', 'paper']}
    mycol = mydb["AssigneeTermsMap"]
    setMap = {}

    if mycol.count_documents({})>0:
        for i in range(0,len(db_assignee_terms_list)):
            myquery = {}
            myquery["name"] = db_assignee_terms_list[i]["name"]

            mydoc = mycol.find(myquery)
            if(mydoc.count()>0):
                #print("Entry exists")
                #update expertise/terms list
                setMap["terms"] = db_assignee_terms_list[i]["terms"]
                newvalues = { "$set": setMap }
                mycol.update_one(myquery, newvalues)

            else:
                #print("Entry doesn't exist")
                mydict = {}
                mydict["name"] = myquery["name"]
                mydict["terms"] = db_assignee_terms_list[i]["terms"]
                x = mycol.insert_one(mydict)

    else:
            #print("No document yet in this collection.")
            x = mycol.insert_many(db_assignee_terms_list)

        #check if query exists, if not then create one 

    #print "AssigneeTermsMap" after the update:
    #for x in mycol.find():
        #print(x)
        
    #terms_assignee_map - dictionary - key:list[map,map]
    #{'paper': [{'assignee': 'Moumita Asad', 'date': '2020-09-08T03:58:33.865-0700'}, {'assignee': 'Noshin Tahsin', 
    #'date': '2020-09-08T03:57:26.760-0700'}],'including': [{'assignee': 'Moumita Asad', 'date': '2020-09-08T03:58:33.865-0700'}]}
    #for db insertion i need a list of individual dictionaries
    #{'paper': [{'assignee': 'Moumita Asad', 'date': '2020-09-08T03:58:33.865-0700'}, {'assignee': 'Noshin Tahsin', 
    #'date': '2020-09-08T03:57:26.760-0700'}]}

    db_terms_assignee_list = []
    for key in terms_assignee_map:
        temp_dict={}
        temp_dict['term'] = key
        temp_dict['developer_expertise'] = terms_assignee_map[key]
        
        # datetime object containing current date and time
        now = datetime.now()
        currentTime = now.strftime("%Y-%m-%d %H:%M:%S")

        #print(currentTime)
        temp_dict['last_updated'] = currentTime
        db_terms_assignee_list.append(temp_dict)

    #print("db_terms_assignee_list: ")
    #print(db_terms_assignee_list)

    #mongo - collection - TermsAssigneeMap
    #{'term': 'paper', 'developer_expertise': [{'assignee': 'Moumita Asad', 'date': '2020-09-08T03:58:33.865-0700'}, 
    #{'assignee': 'Noshin Tahsin', 'date': '2020-09-08T03:57:26.760-0700'}]}

    mycol = mydb["TermsAssigneeMap"]
    setMap = {}

    if mycol.count_documents({})>0:
        for i in range(0,len(db_terms_assignee_list)):
            myquery = {}
            myquery["term"] = db_terms_assignee_list[i]["term"]

            mydoc = mycol.find(myquery)
            if(mydoc.count()>0):
                #print("Entry exists")
                #update developer expertise list
                setMap["developer_expertise"] = db_terms_assignee_list[i]["developer_expertise"]
                setMap["last_updated"] = db_terms_assignee_list[i]["last_updated"]
                newvalues = { "$set": setMap }
                mycol.update_one(myquery, newvalues)

            else:
                #print("Entry doesn't exist")
                mydict = {}
                mydict["term"] = myquery["term"]
                mydict["developer_expertise"] = db_terms_assignee_list[i]["developer_expertise"]
                mydict["last_updated"] = db_terms_assignee_list[i]["last_updated"]
                x = mycol.insert_one(mydict)

    else:
            #print("No document yet in this collection.")
            x = mycol.insert_many(db_terms_assignee_list)

        #check if query exists, if not then create one 

    #print "TermsAssigneeMap" after the update:
    #for x in mycol.find():
        #print(x)


def process_new_issue(key):
    global new_terms 
    global newterm_dev_map
    newterm_dev_map={}
    global dev_termInfo
    dev_termInfo={}
    global newterm_dev_list 
    global newterm_dev_date 
    newterm_dev_list =[]
    newterm_dev_date = []
    #print("%%%%%%%%%%%%%%%%%%%%%%%%%%"+str(key))

    new_issue=jira.issue(key)
    new_issue_creation_date = str(new_issue.fields.created)
    #issue=jira.issue('SAAJ-4')
    #print("issue status: ",issue.fields.status.name)
    creation_date = str(new_issue.fields.created)
    current_time = creation_date
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
    #print(new_terms)

    #fetch terms_assignee_map from database
    mycol = mydb["TermsAssigneeMap"]

    if mycol.count_documents({})>0:
        mydoc = mycol.find()
        for x in mydoc:
            #tempMap = {}
            fetched_terms_assignee_map[x["term"]] = x["developer_expertise"]
            #tempMap["last_updated"] = x["last_updated"]
            #db_terms_assignee_list.append(tempMap)

    #print(fetched_terms_assignee_map)
    
    #now i have the new issue terms
    cnt=0
    for newterm in new_terms:
        if newterm in fetched_terms_assignee_map:
            cnt=cnt+1
            #print(newterm)
            #print(fetched_terms_assignee_map[newterm])
            newterm_dev_map[newterm]=fetched_terms_assignee_map[newterm]
            #returns a devlist for a single newterm
            #developers who has previously worked on that term
            #one dev name can occur multiple times
            #which implies he has worked on that term multiple times-more experienced!

    #fetch available devlist from db
    mycol = mydb["Assignee"]

    if mycol.count_documents({})>0:
        mydoc = mycol.find()
        for x in mydoc:
            #tempMap = {}
            print(x["name"])
            fetched_available_devlist.append(x["name"])

    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print(fetched_available_devlist)
    
    for dev in fetched_available_devlist:
        #print(dev)
        term_info={}
        #check if he has used a newterm and get the newterm
        for key in newterm_dev_map:
            new_time_diff=798798090
            newterm_dev_list =[]
            term_list_len = len(newterm_dev_map[key])
        
            for i in range (0,term_list_len):
                #print(newterm_dev_map[nterm][i])
                newterm_dev_list.append(newterm_dev_map[key][i]['assignee'])
                newterm_dev_date.append(newterm_dev_map[key][i]['date'])

            if dev in newterm_dev_list:
                #now i need the key-key is the newterm
                #calculate term info for the key
                #just need the fixfrequency
                #how many times dev is in newterm_dev_map[key]
                devnames=newterm_dev_list       
                #print(devnames)
                dev_count=devnames.count(dev)
                #print(key)
                #print(dev_count)
                #List-devcount,termusedate
                for d in newterm_dev_date:
                    datetrack=d
                    #ekhn er date thke shb thke kache jeta first e init inf diye
                    current_time_converted = datetime.strptime(current_time[:19], "%Y-%m-%dT%H:%M:%S")
                    datetrack_converted = datetrack.strftime("%Y-%m-%d %H:%M:%S")
                    datetrack_converted = datetime. strptime(datetrack_converted, '%Y-%m-%d %H:%M:%S')

                    time_diff = current_time_converted - datetrack_converted
                    if(time_diff.days<new_time_diff):
                        kept_datetrack = datetrack 

                devcount_lastuse = {}
                devcount_lastuse['devcount']=dev_count
                devcount_lastuse['lastuse']=kept_datetrack

                term_info[key]=devcount_lastuse #add term_use_date : last fixing time of a term by a developer
                #print(term_info)

        dev_termInfo[dev]=term_info

        #print(dev_termInfo)

        #for key,value in dev_termInfo.items():
            #print(key," => ",value)


def devFixFreq(term):
    dev_use_count=0
    #fetch assignee terms map from db
    mycol = mydb["AssigneeTermsMap"]

    if mycol.count_documents({})>0:
        mydoc = mycol.find()
        for x in mydoc:
            fetched_assignee_terms_map[x["name"]] = x["terms"]

    #print(fetched_assignee_terms_map)
    
    for dev in fetched_assignee_terms_map:
        terms_used=fetched_assignee_terms_map[dev]
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
        for each_term in termInfo:
            term_freq=termInfo[each_term]['devcount']
            term_using_date_latest = termInfo[each_term]['lastuse']
            #print(info_term)
            #print(term_freq)
            ##dev=number of devs in the project 
            #len(available_devlist)

            #devfixfreq() : returns numof devs who fixed the term related bugs
            num_of_devs=len(fetched_available_devlist)
            tfIdf=term_freq*math.log(num_of_devs/devFixFreq(each_term))
            #difff = new issue creation - term using date

            c_new_issue_creation_date = datetime.strptime(new_issue_creation_date[:19],'%Y-%m-%d %H:%M:%S')
            #c_term_using_date_latest = datetime.strptime(term_using_date_latest[:19],'%Y-%m-%d %H:%M:%S')

            c_term_using_date_latest = term_using_date_latest.strftime("%Y-%m-%d %H:%M:%S")
            c_term_using_date_latest = datetime. strptime(c_term_using_date_latest, '%Y-%m-%d %H:%M:%S')
                
            difff = c_new_issue_creation_date - c_term_using_date_latest
            #print(difff.days)
            if difff.days!=0:
                fix_date=(1/devFixFreq(each_term))+(1/(difff.days**(1/2)))
            else:
                difff = 14 #one-sprint
                fix_date=(1/devFixFreq(each_term))+(1/(difff**(1/2)))
            expertise+=tfIdf*fix_date
        #end of for
        dev_score[key]=expertise
    #end of for
    #print("\nSCORE: ")
    #print(dev_score)
    sorted_dev_score = sorted(dev_score.items() , reverse=True, key=lambda x: x[1])
    
    return sorted_dev_score

#need to store suggestion in db
def getList():
    a=[]
    a_id=[]
    resultList = []

    #fetch account id map
    mycol = mydb["Assignee"]

    if mycol.count_documents({})>0:
        mydoc = mycol.find()
        for x in mydoc:
            fetched_account_id_map[x["name"]] = x["assignee_id"]

    #print(fetched_account_id_map)
    
    for i in range (0,len(sorted_dev_score)):
        tempMap = {}
        tempMap["name"] = sorted_dev_score[i][0]
        tempMap["account_id"] = fetched_account_id_map[sorted_dev_score[i][0]]
        tempMap["score"] = sorted_dev_score[i][1]
        resultList.append(tempMap)
        
        a.append(sorted_dev_score[i][0])
        a_id.append(fetched_account_id_map[sorted_dev_score[i][0]])
        #print(sorted_dev_score[i][0])
        #print("Account ID")
        #print(fetched_account_id_map[sorted_dev_score[i][0]])
        #print("\n")

    #print(a)
    #print(a_id)
    
    # Iterate over the sorted sequence
    scoreList = []
    for elem in sorted_dev_score :
        #print(elem[0] , " ::" , elem[1] )
        scoreList.append(elem[1])
    
    #a=a+a_id+scoreList
    #print(a)
    print(resultList)
    
    return resultList
    #return ["new-lucille.hogan-2","isabel.richardson","marsha.cook","joshua.maples","jerome.johnson"]

ans=None
@app.route('/suggested/', methods =["GET", "POST"]) 

def suggested(ans=""):
  
    if request.method == "GET":
        key=request.args.get('keyname')
        print(key)
        process_new_issue(key)
        global sorted_dev_score
        sorted_dev_score = calculate_devscore()

        global FinalResult
        FinalResult=getList()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
        print(FinalResult)
        #Final Result List: [{'name': 'A. T. M. Fazlay Rabbi', 'account_id': '5e9412627bc0680c2ca4dd39', 'score': 3.126493726796646},{...}]
        ans=jsonify(FinalResult)

        return ans

rt = None

@app.route("/change/", methods = ["GET","POST","PUT"])

def change(rt=""):
    key=request.args.get('keyname')
    #print("&&&&&&&&&&&&KeyToChange: ",key)

    toAssign=request.args.get('idToAssign')
    #print("&&&&&&&&&&&&toAssign: ",toAssign)

    url = "https://pg-req.atlassian.net/rest/api/3/issue/"
    url = url + key +"/assignee"

    #toAssign = "5e299526bf04010e70c42927"

    auth = HTTPBasicAuth("bsse0914@iit.du.ac.bd", "4MsH8F6gkCV3yMwY8ZHs8D47")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    #need to add the target account id here
    payload = json.dumps( {
        "accountId": toAssign
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

    #project_id: ‘RP’
    #issue_id: ‘RP-1’
    #suggestion_list:
    #assignee_id: '5f5764e4bea5be0068101b9a'
    #assigning_date : ‘2021-02-22T09:37:09.508-0800’
    formKey = key
    project_id = formKey.split('-')[0]
    issue_id = formKey
    assignee_id = toAssign
    now = datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    assigning_date = currentTime

    mycol = mydb["Suggestions"]

    suggestiondict = {}

    suggestiondict["project_id"] = project_id
    suggestiondict["issue_id"] = issue_id
    suggestiondict["suggestion"] = FinalResult
    suggestiondict["assignee_id"] = assignee_id
    suggestiondict["assigning_date"] = assigning_date

    x = mycol.insert_one(suggestiondict)
    #print "Suggestions" after the update:
    #for x in mycol.find():
        #print(x)
    
    return rt
    
@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':

        file = request.files['myfile']
        username = request.form.get("username")
        print(username)

        resumeInfo = file.read()
        resumeInfo = resumeInfo.decode()
        resumeInfo=remove_punctuation(resumeInfo)
        bad_chars=['!','@', '#', '$','%', '^', '&','*','(',')','-','+']
        resumeInfo = ''.join(i for i in resumeInfo if not i in bad_chars)
        tokenized_resumeInfo=tokenize(resumeInfo)
        print(tokenized_resumeInfo)

        #cv data
        #update mongo - collection - AssigneeTermsMap for resume data
        ResumeEntry = {}
        ResumeEntry["name"] = username
        ResumeEntry["terms"] = tokenized_resumeInfo

        #{"name": "Yasin Sazid", "terms": ['bug', 'javascript', 'html','UI']}
        
        mycol = mydb["AssigneeTermsMap"]
        setMap = {}

        if mycol.count_documents({})>0:
            myquery = {}
            myquery["name"] = ResumeEntry["name"]
            mydoc = mycol.find(myquery)
                
            if(mydoc.count()>0):
                #print("Entry exists")
                #update expertise/terms list
                setMap["terms"] = ResumeEntry["terms"]
                newvalues = { "$set": setMap }
                mycol.update_one(myquery, newvalues)

            else:
                #print("Entry doesn't exist")
                x = mycol.insert_one(ResumeEntry)

        else:
            #print("No document yet in this collection.")
            x = mycol.insert_one(ResumeEntry)
                       
            #for x in mycol.find():
                #print(x)
                
        #update mongo - collection - TermsAssigneeMap for resume data
        #term-developer expertise list : assignee, date map, last updated

        now = datetime.now()
        currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
        last_updated = currentTime
        currentTime = datetime. strptime(currentTime, '%Y-%m-%d %H:%M:%S')
        assigning_date = currentTime

        #fetch terms_assignee_map from database
        mycol = mydb["TermsAssigneeMap"]

        if mycol.count_documents({})>0:
            mydoc = mycol.find()
            for x in mydoc:
                fetched_terms_assignee_map[x["term"]] = x["developer_expertise"]
            
            #print(fetched_terms_assignee_map)


        for term in ResumeEntry["terms"]:
            if mycol.count_documents({})>0:
                if(term in fetched_terms_assignee_map):
                    setMap = {}
                    #print("Term exists")
                    #update expertise/terms list
                    fetchedDeveloperExpertise = []
                    
                    fetchedDeveloperExpertise = fetched_terms_assignee_map[term]
                    
                    tempDevMap = {}
                    tempDevMap["assignee"] = ResumeEntry["name"]
                    tempDevMap["date"] = assigning_date
                    
                    fetchedDeveloperExpertise.append(tempDevMap)
                    
                    myquery = {}
                    myquery["term"] = term
                    mydoc = mycol.find(myquery)
                    
                    setMap["developer_expertise"] = fetchedDeveloperExpertise
                    newvalues = { "$set": setMap }
                    
                    mycol.update_one(myquery, newvalues)
                    
                    setMap["last_updated"] = last_updated
                    newvalues = { "$set": setMap }
                    mycol.update_one(myquery, newvalues)

                else:
                    setMap = {}
                    #print("Entry doesn't exist")
                    setMap["term"] = term
                    
                    devExpertiseList = []

                    tempDevMap = {}
                    tempDevMap["assignee"] = ResumeEntry["name"]
                    tempDevMap["date"] = assigning_date
                    
                    devExpertiseList.append(tempDevMap)
                    
                    setMap["developer_expertise"] = devExpertiseList
                    setMap["last_updated"] = last_updated

                    x = mycol.insert_one(setMap)

            else:
                setMap = {}
                #print("No document yet in this collection.")
                setMap["term"] = term
                devExpertiseList = []

                tempDevMap = {}
                tempDevMap["assignee"] = ResumeEntry["name"]
                tempDevMap["date"] = assigning_date

                devExpertiseList.append(tempDevMap)

                setMap["developer_expertise"] = devExpertiseList
                setMap["last_updated"] = last_updated

                x = mycol.insert_one(setMap)

            #for x in mycol.find():
                    #print(x)

        return ('', 204)     

    else:
        result = request.args.get['myfile']
    
        return result

@app.route('/constructCorpus', methods=['GET','POST'])
def constructCorpus():
    data_processing()

    return ('', 204)  

s = None
@app.route('/summary/', methods=['GET','POST'])
def summary(s=""):
    
    if request.method == "GET":
        path=request.args.get('pathname')

        issue_id_list = []
        project_id_list = []
        assigning_date_list = []
        suggestion_list = []
        assignee_id_list = []
        YesNoList = []

        mycol = mydb["Suggestions"]
        if mycol.count_documents({})>0:
            mydoc = mycol.find()
            for x in mydoc:
                #tempMap = {}
                #pprint(x)
                issue_id_list.append(x["issue_id"])
                project_id_list.append(x["project_id"])
                assigning_date_list.append(str(x["assigning_date"]))
                suggestion_list.append(x['suggestion'])
                assignee_id_list.append(x["assignee_id"])
                id_list = []
                
                for s in x['suggestion']:
                    id_list.append(s['account_id'])
                    
                if x["assignee_id"] in id_list:
                    YesNoList.append("Yes")
                else:
                    YesNoList.append("No")

        # dictionary of lists 
        dict = {'IssueID': issue_id_list, 'ProjectID': project_id_list, 'Assigning Date': assigning_date_list, 'Suggestions':suggestion_list,'Assigneed To':assignee_id_list, 'Suggestion Followed':YesNoList} 
            
        df = pd.DataFrame(dict)

        totalCount = df['Suggestion Followed'].value_counts()
        #print(totalCount)

        YesCount = 0
        NoCount = 0

        for x in df['Suggestion Followed']:
            if x=="Yes":
                YesCount = YesCount + 1
            else:
                NoCount = NoCount + 1

        #print(YesCount)
        #print(NoCount)

        reportSummary = []
        reportSummary.append(int(totalCount))
        reportSummary.append(YesCount)
        reportSummary.append(NoCount)

        print(">>>>>>>>>>>>>>>>>>>>>>>")
        print(reportSummary)
        #specify path
        #r'C:/Users/ASUS/Desktop/SPL3/Resume/VSReport.csv'
        now = datetime.now()
        filedate = now.strftime("%Y-%m-%d")
        filename = "Jira-Plugin-Summary-"+filedate+".csv"
        pathstring = path + filename
        df.to_csv(pathstring, index=False)
        #summary = [3,3,0]
        s=json.dumps(reportSummary)
        return s

if __name__ == '__main__':
    app.run(debug=True)