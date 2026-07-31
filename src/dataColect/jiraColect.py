import time
from jira import JIRA


def getBugsFromJira(apikey,server,start_bug_Key):
    #print(f"APIKEY = [{apikey}] \nSERVER: [{server}]")
    loops = 0
    data =[]
    bugs =[]
    list_Bugs = []
    tentativas = 0
    while(True):
        if(len(data)<1000 and loops >0):
            break
        if(loops==0):
            string = "issuekey >= "+str(start_bug_Key)+" AND issuetype = Bug ORDER BY key ASC"
        else:
            string = "issuekey > "+str(data[999].key)+" AND issuetype = Bug ORDER BY key ASC"
        try:
            #print(f"[{string}]")
            #print(f"key: [{apikey}]\n server: [{server}]")
            tentativas+=1
            if tentativas > 20:
                return -1
            jira = JIRA(server, token_auth=(apikey))
            data = jira.search_issues(string,maxResults=1000)
            jira.close()
            bugs += data
            loops+=1
            tentativas =0
        except:
            print("1 - Trying to reconnect to the server")
            continue

    b=0
    jira2 = JIRA(server, token_auth=(apikey))
    
    while b < len(bugs):
        try:
            tentativas+=1
            if tentativas > 20:
                return -1
            issue = jira2.issue(bugs[b])
            tentativas=0
        except:
            print(f"2 - Trying to reconnect to the server")
            jira2.close()
            time.sleep(2)
            jira2 = JIRA(server, token_auth=(apikey))
            continue
        desc = ""
        summary = ""
        team = []
        comp = []
        key = str(bugs[b])
        for f in issue.fields.__dict__:
            if issue.fields.__dict__[f] is not None and str(issue.fields.__dict__[f]) != "Please select...":
                if f == "description":
                    desc = str(issue.fields.__dict__[f])
                elif f == "summary":
                    summary = str(issue.fields.__dict__[f])
                elif f == "customfield_15300":
                    team = issue.fields.__dict__[f]
                elif f == "customfield_15802":
                    comp = issue.fields.__dict__[f]
        dic_bug = {'key':key, 'desc':desc, 'summary':summary, 'teams':team, 'comps':comp}
        list_Bugs.append(dic_bug.copy())
        b+=1
    return list_Bugs

def getTestsFromJira(apikey,server,start_test_Key):
    print(f"APIKEY = [{apikey}] \nSERVER: [{server}]")
    loops = 0
    tests = []
    data =[]
    list_Tests = []
    tentativas = 0
    while(True):
        if(len(data)<1000 and loops >0):
            break
        if(loops==0):
            string = "issuekey >= "+str(start_test_Key)+" AND issuetype = Test ORDER BY key ASC"
        else:
            string = "issuekey > "+str(data[999].key)+" AND issuetype = Test ORDER BY key ASC"
        try:
            tentativas+=1
            if tentativas > 20:
                return -1
            print(f"[{string}]")
            print(f"key: [{apikey}]\n server: [{server}]")
            jira = JIRA(server, token_auth=(apikey))
            data = jira.search_issues(string,maxResults=1000)
            jira.close()
            tests += data
            loops+=1
            tentativas=0
        except:
            print("1 - Trying to reconnect to the server")
            continue

    b=0
    jira2 = JIRA(server, token_auth=(apikey))
    
    while b < len(tests):
        try:
            tentativas+=1
            if tentativas > 20:
                return -1
            issue = jira2.issue(tests[b])
            tentativas=0
        except:
            print(f"2 - Trying to reconnect to the server")
            jira2.close()
            time.sleep(2)
            jira2 = JIRA(server, token_auth=(apikey))
            continue
        steps = ""
        summary = ""
        team = []
        comp = []
        key = str(tests[b])
        for f in issue.fields.__dict__:
            if issue.fields.__dict__[f] is not None and str(issue.fields.__dict__[f]) != "Please select...":
                if f == "summary":
                    summary = str(issue.fields.__dict__[f])
                elif f == "customfield_15300":
                    team = issue.fields.__dict__[f]
                elif f == "customfield_15802":
                    comp = issue.fields.__dict__[f]
                elif f == "customfield_13506":
                    for w in issue.fields.customfield_13506.steps:
                        for i in w.fields.__dict__:
                            steps+= str(w.fields.__dict__[i])+"\n"

        dic_test = {'key':key, 'steps':steps, 'summary':summary, 'teams':team, 'comps':comp}
        list_Tests.append(dic_test.copy())
        b+=1
    return list_Tests
