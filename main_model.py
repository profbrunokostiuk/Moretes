from src.model.model import Model
from src.model.modelAvg import ModelAvg
from src.model.modelRand import ModelRand
import pickle
import time
from jira import JIRA


def getBugsFromJira(apikey,server,start_bug_Key, list_Bugs, qtd, tent, tentlinks):

    loops = 0
    data =[]
    bugs =[]
    tentativas = 0
    while(True):
        if(len(data)<qtd and loops >0):
            break
        if(loops==0):
            string = "issuekey >= "+str(start_bug_Key)+" AND issuetype = Bug ORDER BY key ASC"
        else:
            string = "issuekey > "+str(data[qtd-1].key)+" AND issuetype = Bug ORDER BY key ASC"
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            jira = JIRA(server, token_auth=(apikey))
            data = jira.search_issues(string,maxResults=qtd)
            jira.close()
            bugs += data
            loops+=1
            tentativas =0
        except:
            print(f"Trying to reconnect to the server - List Bug issues {tentativas}/{tent}")
            continue

    b=0
    tentativas=0
    while True:
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            jira2 = JIRA(server, token_auth=(apikey))
            tentativas=0
            break
        except:
             print(f"Trying to reconnect to the server - Get data Bug issues {tentativas}/{tent}")

    
    while b < len(bugs):
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            issue = jira2.issue(bugs[b])
            tentativas=0
        except:
            print(f"Trying to reconnect to the server - Get data Bug issues {tentativas}/{tent}")
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
                elif f == "status":
                    status = str(issue.fields.__dict__[f])
                elif f == "issuelinks":
                    links = []
                    for link_id in issue.fields.__dict__['issuelinks']:
                        tentativas2 = 0
                        while(True):
                            try:
                                tentativas2+=1
                                if tentativas2 > tentlinks:
                                    break
                                jira3 = JIRA(server, token_auth=(apikey))
                                links.append(str(jira3.issue_link(link_id).__dict__['inwardIssue'].__dict__['key']))
                                jira3.close()
                                tentativas2 =0
                                break
                            except:
                                print(f"Trying to reconnect to the server - Get Bug linked issues {tentativas2}/{tentlinks}")
                                continue
              
        dic_bug = {'key':key, 'desc':desc, 'summary':summary, 'teams':team, 'comps':comp, 'status': status, 'links':links}
        list_Bugs.append(dic_bug.copy())
        b+=1
    return list_Bugs

def getStorysFromJira(apikey,server,start_bug_Key, list_Bugs, qtd, tent, tentlinks):

    loops = 0
    data =[]
    bugs =[]
    tentativas = 0
    while(True):
        if(len(data)<qtd and loops >0):
            break
        if(loops==0):
            string = "issuekey >= "+str(start_bug_Key)+" AND issuetype = Story ORDER BY key ASC"
        else:
            string = "issuekey > "+str(data[qtd-1].key)+" AND issuetype = Story ORDER BY key ASC"
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            jira = JIRA(server, token_auth=(apikey))
            data = jira.search_issues(string,maxResults=qtd)
            jira.close()
            bugs += data
            loops+=1
            tentativas =0
        except:
            print(f"Trying to reconnect to the server - List Storys issues {tentativas}/{tent}")
            continue

    b=0
    tentativas=0
    while True:
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            jira2 = JIRA(server, token_auth=(apikey))
            tentativas=0
            break
        except:
             print(f"Trying to reconnect to the server - Get data Bug issues {tentativas}/{tent}")
    
    while b < len(bugs):
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            issue = jira2.issue(bugs[b])
            tentativas=0
        except:
            print(f"Trying to reconnect to the server - Get Data Story issues {tentativas}/{tent}")
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
                elif f == "status":
                    status = str(issue.fields.__dict__[f])
                elif f == "issuelinks":
                    links = []
                    for link_id in issue.fields.__dict__['issuelinks']:
                        tentativas2 = 0
                        while(True):
                            try:
                                tentativas2+=1
                                if tentativas2 > tentlinks:
                                    break
                                jira3 = JIRA(server, token_auth=(apikey))
                                links.append(str(jira3.issue_link(link_id).__dict__['inwardIssue'].__dict__['key']))
                                jira3.close()
                                tentativas2 =0
                                break
                            except:
                                print(f"Trying to reconnect to the server - Get data links Story issues {tentativas2}/{tentlinks}")
                                continue
              
        dic_bug = {'key':key, 'desc':desc, 'summary':summary, 'teams':team, 'comps':comp, 'status': status, 'links':links}
        list_Bugs.append(dic_bug.copy())
        b+=1
    return list_Bugs

def getFeaturesFromJira(apikey,server,start_bug_Key, list_Bugs, qtd, tent, tentlinks):

    loops = 0
    data =[]
    bugs =[]
    tentativas = 0
    while(True):
        if(len(data)<qtd and loops >0):
            break
        if(loops==0):
            string = "issuekey >= "+str(start_bug_Key)+" AND issuetype = Feature ORDER BY key ASC"
        else:
            string = "issuekey > "+str(data[qtd-1].key)+" AND issuetype = Feature ORDER BY key ASC"
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            jira = JIRA(server, token_auth=(apikey))
            data = jira.search_issues(string,maxResults=qtd)
            jira.close()
            bugs += data
            loops+=1
            tentativas =0
        except:
            print(f"Trying to reconnect to the server - List Features issues {tentativas}/{tent}")
            continue

    b=0
    tentativas=0
    while True:
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            jira2 = JIRA(server, token_auth=(apikey))
            tentativas=0
            break
        except:
             print(f"Trying to reconnect to the server - Get data Bug issues {tentativas}/{tent}")
    
    while b < len(bugs):
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Bugs
            issue = jira2.issue(bugs[b])
            tentativas=0
        except:
            print(f"Trying to reconnect to the server - Get data Features issues {tentativas}/{tent}")
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
                elif f == "status":
                    status = str(issue.fields.__dict__[f])
                elif f == "issuelinks":
                    links = []
                    for link_id in issue.fields.__dict__['issuelinks']:
                        tentativas2 = 0
                        while(True):
                            try:
                                tentativas2+=1
                                if tentativas2 > tentlinks:
                                    break
                                jira3 = JIRA(server, token_auth=(apikey))
                                links.append(str(jira3.issue_link(link_id).__dict__['inwardIssue'].__dict__['key']))
                                jira3.close()
                                tentativas2 =0
                                break
                            except:
                                print(f"Trying to reconnect to the server - Get data link Features issues {tentativas2}/{tentlinks}")
                                continue
              
        dic_bug = {'key':key, 'desc':desc, 'summary':summary, 'teams':team, 'comps':comp, 'status': status, 'links':links}
        list_Bugs.append(dic_bug.copy())
        b+=1
    return list_Bugs

def saveBugsInFile(bug_list, model, compsList, teamsList, lista_links, dict_bug, cont_bug):

    for bug in bug_list:
        encode_text = model.encode.encode(bug['desc'], convert_to_tensor=True).tolist()
        summary = bug['summary']
        status = bug['status']
        key = bug['key']
        links = [bug['key'], bug['links']]

        lista_links.append(links)


        comps = []
        for comp in bug['comps']:
            if comp.strip() not in compsList:
                comps.append(len(compsList))
                compsList.append(comp.strip())
            else:
                comps.append(compsList.index(comp.strip()))

        comp_str = str(comps).replace("[","").replace("]","").replace(",","#")
          
        teams = []
        for team in bug['teams']:
            if team.strip() not in teamsList:
                teams.append(len(teamsList))
                teamsList.append(team.strip())
            else:
                teams.append(teamsList.index(team.strip()))

        teams_str = str(teams).replace("[","").replace("]","").replace(",","#")

        file = open('./data/SBert_Bug.csv', 'a', encoding='utf-8')
        file.write(f"{cont_bug},{str(key).strip()},{str(status).strip()},{teams_str.strip()},{comp_str.strip()}")
        for i in range(len(encode_text)):
            file.write(f",{encode_text[i]:.6f}")
        file.write("\n")
        file.close()

        file = open('./data/SummaryBugs.csv', 'a', encoding='utf-8')
        file.write(f"{str(key).strip()},{str(summary.replace(",","(comma)")).strip()}\n")
        file.close()

        dict_bug[str(key)] = cont_bug
        cont_bug+=1

    return compsList, teamsList, lista_links, dict_bug, cont_bug

def saveStorysInFile(bug_list, model, compsList, teamsList, lista_links, dict_bug, cont_bug):


    for bug in bug_list:
        encode_text = model.encode.encode(bug['desc'], convert_to_tensor=True).tolist()
        summary = bug['summary']
        status = bug['status']
        key = bug['key']
        links = [bug['key'], bug['links']]

        lista_links.append(links)


        comps = []
        for comp in bug['comps']:
            if comp.strip() not in compsList:
                comps.append(len(compsList))
                compsList.append(comp.strip())
            else:
                comps.append(compsList.index(comp.strip()))

        comp_str = str(comps).replace("[","").replace("]","").replace(",","#")
          
        teams = []
        for team in bug['teams']:
            if team.strip() not in teamsList:
                teams.append(len(teamsList))
                teamsList.append(team.strip())
            else:
                teams.append(teamsList.index(team.strip()))

        teams_str = str(teams).replace("[","").replace("]","").replace(",","#")

        file = open('./data/SBert_Bug.csv', 'a', encoding='utf-8')
        file.write(f"{cont_bug},{str(key).strip()},{str(status).strip()},{teams_str.strip()},{comp_str.strip()}")
        for i in range(len(encode_text)):
            file.write(f",{encode_text[i]:.6f}")
        file.write("\n")
        file.close()

        file = open('./data/SummaryBugs.csv', 'a', encoding='utf-8')
        file.write(f"{str(key).strip()},{str(summary.replace(",","(comma)")).strip()}\n")
        file.close()
        dict_bug[str(key)] = cont_bug
        cont_bug+=1

    return compsList, teamsList, lista_links, dict_bug, cont_bug

def saveFeaturesInFile(bug_list, model, compsList, teamsList, lista_links, story_list, dict_bug, cont_bug):

    for bug in bug_list:
        desc = bug['desc']+"\n"
        for l in bug["links"]:
            for sto in story_list:
                if l == sto['key']:
                    desc+=sto['desc']
                    break
        encode_text = model.encode.encode(desc, convert_to_tensor=True).tolist()

        summary = bug['summary']
        status = bug['status']
        key = bug['key']
        links = [bug['key'], bug['links']]

        lista_links.append(links)


        comps = []
        for comp in bug['comps']:
            if comp.strip() not in compsList:
                comps.append(len(compsList))
                compsList.append(comp.strip())
            else:
                comps.append(compsList.index(comp.strip()))

        comp_str = str(comps).replace("[","").replace("]","").replace(",","#")
          
        teams = []
        for team in bug['teams']:
            if team.strip() not in teamsList:
                teams.append(len(teamsList))
                teamsList.append(team.strip())
            else:
                teams.append(teamsList.index(team.strip()))

        teams_str = str(teams).replace("[","").replace("]","").replace(",","#")

        file = open('./data/SBert_Bug.csv', 'a', encoding='utf-8')
        file.write(f"{cont_bug},{str(key).strip()},{str(status).strip()},{teams_str.strip()},{comp_str.strip()}")
        for i in range(len(encode_text)):
            file.write(f",{encode_text[i]:.6f}")
        file.write("\n")
        file.close()

        file = open('./data/SummaryBugs.csv', 'a', encoding='utf-8')
        file.write(f"{str(key).strip()},{str(summary.replace(",","(comma)")).strip()}\n")
        file.close()
        dict_bug[str(key)] = cont_bug
        cont_bug+=1

    return compsList, teamsList, lista_links, dict_bug, cont_bug

def getTestsFromJira(apikey,server,start_test_Key, list_Tests, qtd,tent, tentlinks):
    loops = 0
    tests = []
    data =[]
    
    tentativas = 0
    while(True):
        if(len(data)<qtd and loops >0):
            break
        if(loops==0):
            string = "issuekey >= "+str(start_test_Key)+" AND issuetype = Test ORDER BY key ASC"
        else:
            string = "issuekey > "+str(data[qtd-1].key)+" AND issuetype = Test ORDER BY key ASC"
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Tests
            jira = JIRA(server, token_auth=(apikey))
            data = jira.search_issues(string,maxResults=qtd)
            jira.close()
            tests += data
            loops+=1
            tentativas=0
        except:
            print(f"Trying to reconnect to the server - List test issues {tentativas}/{tent}")
            continue

    b=0
    tentativas=0
    while True:
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Tests
            jira2 = JIRA(server, token_auth=(apikey))
            tentativas=0
            break
        except:
             print(f"Trying to reconnect to the server - Get data Bug issues {tentativas}/{tent}")
    
    while b < len(tests):
        try:
            tentativas+=1
            if tentativas > tent:
                return list_Tests
            issue = jira2.issue(tests[b])
            tentativas=0
        except:
            print(f"Trying to reconnect to the server - Get data test issues {tentativas}/{tent}")
            jira2.close()
            time.sleep(2)
            jira2 = JIRA(server, token_auth=(apikey))
            continue
        steps = ""
        summary = ""
        status = ""
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
                elif f == "status":
                    status = str(issue.fields.__dict__[f])

        dic_test = {'key':key, 'steps':steps, 'summary':summary, 'teams':team, 'comps':comp, 'status': status}
        list_Tests.append(dic_test.copy())
        b+=1
    return list_Tests

def saveTestsInFile(test_list, model, compsList, teamsList, dict_test, cont_test):
    
    for test in test_list:
        encode_text = model.encode.encode(test['steps'], convert_to_tensor=True).tolist()
        summary = test['summary']
        status = test['status']
        key = test['key']

        comps = []
        for comp in test['comps']:
            if comp.strip() not in compsList:
                comps.append(len(compsList))
                compsList.append(comp.strip())
            else:
                comps.append(compsList.index(comp.strip()))

        comp_str = str(comps).replace("[","").replace("]","").replace(",","#")
          
        teams = []
        for team in test['teams']:
            if team.strip() not in teamsList:
                teams.append(len(teamsList))
                teamsList.append(team.strip())
            else:
                teams.append(teamsList.index(team.strip()))

        teams_str = str(teams).replace("[","").replace("]","").replace(",","#")

        file = open('./data/SBert_Test.csv', 'a', encoding='utf-8')
        file.write(f"{cont_test},{str(key).strip()},{str(status).strip()},{teams_str.strip()},{comp_str.strip()}")
        for i in range(len(encode_text)):
            file.write(f",{encode_text[i]:.6f}")
        file.write("\n")
        file.close()

        file = open('./data/SummaryTests.csv', 'a', encoding='utf-8')
        file.write(f"{str(key).strip()},{str(summary.replace(",","(comma)")).strip()}\n")
        file.close()
        dict_test[str(key)] = cont_test
        cont_test+=1

    return compsList, teamsList, cont_test, dict_test

def loadDataFromJira(apikey, server, model, projects):

    open('./data/SBert_Test.csv', 'w', encoding='utf-8').close()
    open('./data/SummaryTests.csv', 'w', encoding='utf-8').close()
    open('./data/SBert_Bug.csv', 'w', encoding='utf-8').close()
    open('./data/SummaryBugs.csv', 'w', encoding='utf-8').close()

    cont_test = 0
    cont_bug = 0
    tent = 100
    tentlinks = 1

    compsList = []
    teamsList = [] 
    
    lista_links = [] 

    test_dict = {}
    test_list = [] 
    
    dict_bug = {}
    bug_list = []

    story_list = []
    feature_list = []

    # print("Listing projects")
    # tentativas = 0
    # projects = []
    # while(True):
    #     try:
    #         tentativas+=1
    #         if tentativas > 20:
    #             return -1
    #         jira = JIRA(server, token_auth=(apikey))
    #         for i in jira.projects():
    #             if str(i.__dict__['name']) not in projects: 
    #                 projects.append(str(i.__dict__['name']))
    #         jira.close()
    #         break
    #     except:
    #         print("Trying to reconnect to the server")
    #         continue

    #projects = projects[1:]
    # print(projects)
    # projects = ['SP7 A-Team', 'SP7 ALSPICE ', 'SP7 Architects', 'SP7 Area 51', 'SP7 BigBang', 'SP7 Cerberus', 
    #             'SP7 Coyotes', 'SP7 Desperados', 'SP7 DNA', 'SP7 Erlkoenig', 'SP7 ETA', 'SP7 Evergreens', 'SP7 Improvements', 
    #             'SP7 ModelMonks', 'SP7 Outage Management', 'SP7 Portfolio',  'SP7 Program (ART)', 'SP7 Roadrunners', 'SP7 Rockies', 
    #             'SP7 tardHIS', 'SP7 TestTekkies', 'SP7 Update Mavericks', 'Spectrum Power 7', 'WebSDK']
    for proj in projects:
        #print(proj)
        #startKey = None
        tentativas = 0
        while(True):
            string = "project = '"+proj+"' ORDER BY createdDate ASC"
            try:
                tentativas+=1
                if tentativas > tent:
                    startKey = None
                    break
                jira2 = JIRA(server, token_auth=(apikey))
                startKey = jira2.search_issues(string,maxResults=1)
                jira2.close()
                tentativas =0
                break
            except:
                print(f"Get First Issue from {proj} - Trying to reconnect to the server - {tentativas}/{tent}")
                continue
        
        if startKey is not None:
            startKey = startKey[0].key
            print(f"Get Issues from project = {proj}")
            print("Get Test")
            test_list = getTestsFromJira(apikey,server,startKey, test_list, 100, tent, tentlinks)
            print(f"Test Collected {len(test_list)}")
            print("Get Bugs")
            bug_list = getBugsFromJira(apikey,server,startKey, bug_list, 100, tent, tentlinks)
            print(f"Bugs Collected {len(bug_list)}")
            print("Get Story")
            story_list = getStorysFromJira(apikey,server,startKey, story_list, 100, tent, tentlinks)
            print(f"Story Collected {len(story_list)}")
            print("Get Features")
            feature_list = getFeaturesFromJira(apikey,server,startKey, feature_list, 100, tent, tentlinks)
            print(f"Features Collected {len(feature_list)}")
            
    if len(test_list)>0:
        compsList, teamsList, cont_test, test_dict = saveTestsInFile(test_list, model, compsList, teamsList, test_dict, cont_test)
    if len(bug_list)>0:
        compsList, teamsList, lista_links, dict_bug, cont_bug = saveBugsInFile(bug_list, model, compsList, teamsList, lista_links, dict_bug, cont_bug)
    if len(story_list)>0:
        compsList, teamsList, lista_links, dict_bug, cont_bug = saveStorysInFile(story_list, model, compsList, teamsList, lista_links, dict_bug, cont_bug)
    if len(feature_list)>0:
        compsList, teamsList, lista_links, dict_bug, cont_bug = saveFeaturesInFile(feature_list, model, compsList, teamsList, lista_links, story_list, dict_bug, cont_bug)


    file = open('./data/Comp_Index.csv', 'w', encoding='utf-8')
    for com in range(len(compsList)):
        file.write(f"{com},{compsList[com]}\n")
    file.close()

    file = open('./data/Team_Index.csv', 'w', encoding='utf-8')
    for team in range(len(teamsList)):
        file.write(f"{team},{teamsList[team]}\n")
    file.close()

    dict_links = {}

    for link in lista_links:
        dict_links[str(link[0]).strip()] = []
        dest = link[1]
        for d in dest:
            if d.strip() in test_dict:
                dict_links[str(link[0]).strip()].append(d.strip())

    bugs_linked = False
    while not bugs_linked:
        bugs_linked = True
        for link in lista_links:
            dest = link[1]
            for d in dest:
                if d.strip() in dict_bug:
                    for item in dict_links[str(link[0]).strip()]:
                        if item not in dict_links[str(d).strip()]:
                            dict_links[str(d).strip()].append(item)
                            bugs_linked = False
                    for item in dict_links[str(d).strip()]:
                        if item not in dict_links[str(link[0]).strip()]:
                            dict_links[str(link[0]).strip()].append(item)
                            bugs_linked = False

    file = open('./data/Interacoes.csv', 'w', encoding='utf-8')

    fileITE = open('./data/Interacoes_TE.csv', 'r')
    lines = fileITE.readlines()
    for line in lines:
        file.write(line)
    fileITE.close()

    for bug in dict_links:
        for test in dict_links[bug]:
            file.write(f"{test},{bug},1,1\n")
    file.close()


def main():

    print("Create Model")
    model = Model()

    print("Traning model")
    epocs = 10
    model.make_model(epocs)

    print("Saving model")
    file = open('./data/model', 'wb')
    pickle.dump(model,file)
    print("Model save")

   
if __name__=="__main__":
    main()