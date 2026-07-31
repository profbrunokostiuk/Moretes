from alive_progress import alive_bar
import os
import datetime
from sentence_transformers import SentenceTransformer
import pickle



class SentenceT:
    def __init__(self, model):
        self.model = model

def FileCheck(fn):
    try:
        open(fn, "r", encoding="utf-8").close()
        return 1
    except IOError:
        return 0

def dateMinutes(dateTestE):
    #dateMinutes("29-07-2021 14:08")
    data = dateTestE.split(" ")
    d1 = data[0].split("-")
    d2 = data[1].split(":")     

    if len(d1[0])>2:
        data = datetime.datetime(int(d1[0]), int(d1[1]), int(d1[2]), int(d2[0]), int(d2[1]))
    else:
        data = datetime.datetime(int(d1[2]), int(d1[1]), int(d1[0]), int(d2[0]), int(d2[1]))
    dataInit = datetime.datetime(2000, 1, 1, 0, 0)
    time = data - dataInit

    return int(time.total_seconds()/60)

def makeFilesCsv(folder):
    model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
    model.max_seq_length = 512
    
    Sentence = SentenceT(model)

    file = open('./data/SentenceTransformer', 'wb')
    pickle.dump(Sentence,file)

    days = 7

    indexTeam = []
    indexComp =[]
    summaryBugs =[]
    summaryTests =[]

    Tests = []
    Bugs =[]

    dateTimeBug = {}

    #SBert_Bug.csv File
    sbert_bug_filename = folder+"UltimateData\\SBert_Bug.csv"
    print(f"File: {sbert_bug_filename}")
    with open(sbert_bug_filename,"w") as sbert_bug_file:
        allFiles = os.listdir(folder+"Bug\\")
        with alive_bar(len(allFiles)) as bar:
            for key in allFiles:
                if key not in Bugs:
                    Bugs.append(key)
                file_desc = folder+"Bug\\"+key+"\\description.txt"
                if (FileCheck(file_desc)):
                    with open(file_desc, encoding="utf-8") as my_file:
                        text = my_file.read()
                    if text == "":
                        text = "None"
                else:
                    print(f"File not found: {file_desc}")
                    text = "None"
                    
                embedding = model.encode(text, convert_to_tensor=True).tolist()

                file_team = folder+"Bug\\"+key+"\\customfield_15300.txt"
                if (FileCheck(file_team)):
                    with open(file_team, encoding="utf-8") as my_file:
                        team = my_file.read().replace("\n","").replace("[","").replace("]","").replace("'","").strip().split(",")
                    if team == [""]:
                        team = ["None"]
                else:
                    print(f"File not found: {file_team}")
                    team = ["None"]

                teamId =[]
                for t in team:
                    if t.strip() not in indexTeam:
                        teamId.append(len(indexTeam))
                        indexTeam.append(t.strip())
                    else:
                        teamId.append(indexTeam.index(t.strip()))
                    
                

                file_summary = folder+"Bug\\"+key+"\\summary.txt"
                if (FileCheck(file_summary)):
                    with open(file_summary, encoding="utf-8") as my_file:
                        summary = my_file.read().replace("\n","").replace("'","").replace(",","").strip()
                    if summary == "":
                        summary = "None"
                else:
                    print(f"File not found: {file_summary}")
                    summary = "None"

                summaryBugs.append([key,summary])
                


                file_comp = folder+"Bug\\"+key+"\\customfield_15802.txt"
                if (FileCheck(file_comp)):
                    with open(file_comp, encoding="utf-8") as my_file:
                        comp = my_file.read().replace("\n","").replace("[","").replace("]","").replace("'","").strip().split(",")
                    if comp == [""]:
                        comp = ["None"]
                else:
                    print(f"File not found: {file_comp}")
                    comp = ["None"]

                compId = []
                for c in comp:
                    if c.strip() not in indexComp:
                        compId.append(len(indexComp))
                        indexComp.append(c.strip())
                    else:
                        compId.append(indexComp.index(c.strip()))

                file_date = folder+"Bug\\"+key+"\\created.txt"
                if (FileCheck(file_date)):
                    with open(file_date, encoding="utf-8") as my_file:
                        datetext = my_file.read().split(".")[0].replace("T"," ")[:-3]
                    if datetext == "":
                        datetext = "None"
                else:
                    print(f"File not found: {file_date}")
                    datetext = "None"

                dateTimeBug[key] = dateMinutes(datetext)


                sbert_bug_file.write(f"{len(Bugs)-1},{key},{str(teamId).replace('[','').replace(']','').replace(' ','').replace(',','#')},{str(compId).replace('[','').replace(']','').replace(' ','').replace(',','#')},{str(embedding).replace(']','').replace('[','')}\n")
                
                bar()

    #SBert_Test.csv File
    sbert_test_filename = folder+"UltimateData\\SBert_Test.csv"
    print(f"File: {sbert_test_filename}")
    with open(sbert_test_filename,"w") as sbert_test_file:
        allFiles = os.listdir(folder+"Test\\")
        with alive_bar(len(allFiles)) as bar:
            for key in allFiles:
                if key not in Tests:
                    Tests.append(key)
                
                file_desc = folder+"Test\\"+key+"\\customfield_13506.txt"
                if (FileCheck(file_desc)):
                    with open(file_desc, encoding="utf-8") as my_file:
                        text = my_file.read().replace("Action - ","").replace("Expected Result - ","").replace("Data - ","")
                    if text == "":
                        text = "None"
                else:
                    print(f"File not found: {file_desc}")
                    text = "None"
                
                embedding = model.encode(text, convert_to_tensor=True).tolist()

                file_team = folder+"Test\\"+key+"\\customfield_15300.txt"
                if (FileCheck(file_team)):
                    with open(file_team, encoding="utf-8") as my_file:
                        team = my_file.read().replace("\n","").replace("[","").replace("]","").replace("'","").strip().split(",")
                    if team == [""]:
                        team = ["None"]
                else:
                    print(f"File not found: {file_team}")
                    team = ["None"]

                teamId =[]
                for t in team:
                    if t.strip() not in indexTeam:
                        teamId.append(len(indexTeam))
                        indexTeam.append(t.strip())
                    else:
                        teamId.append(indexTeam.index(t.strip()))
                
                file_summary = folder+"Test\\"+key+"\\summary.txt"
                if (FileCheck(file_summary)):
                    with open(file_summary, encoding="utf-8") as my_file:
                        summary = my_file.read().replace("\n","").replace("'","").replace(",","").strip()
                    if summary == [""]:
                        summary = "None"
                else:
                    print(f"File not found: {file_summary}")
                    summary = "None"

                summaryTests.append([key,summary])


                file_comp = folder+"Test\\"+key+"\\customfield_15802.txt"
                if (FileCheck(file_comp)):
                    with open(file_comp, encoding="utf-8") as my_file:
                        comp = my_file.read().replace("\n","").replace("[","").replace("]","").replace("'","").strip().split(",")
                    if comp == "":
                        comp = ["None"]
                else:
                    print(f"File not found: {file_comp}")
                    comp = ["None"]
                
                compId = []
                for c in comp:
                    if c.strip() not in indexComp:
                        compId.append(len(indexComp))
                        indexComp.append(c.strip())
                    else:
                        compId.append(indexComp.index(c.strip()))

                sbert_test_file.write(f"{len(Tests)-1},{key},{str(teamId).replace('[','').replace(']','').replace(' ','').replace(',','#')},{str(compId).replace('[','').replace(']','').replace(' ','').replace(',','#')},{str(embedding).replace(']','').replace('[','')}\n")
               
                bar()    

    #Team_Index.csv File
    team_index_file = folder+"UltimateData\\Team_Index.csv"
    print(f"File: {team_index_file}")
    with open(team_index_file,"w") as test_index_file:
        with alive_bar(len(indexTeam)) as bar:
            for team in range(len(indexTeam)):
                test_index_file.write(f"{team},{indexTeam[team]}\n")
                bar()

    #Comp_Index.csv File
    comp_index_file = folder+"UltimateData\\Comp_Index.csv"
    print(f"File: {comp_index_file}")
    with open(comp_index_file,"w") as comp_index_file:
        with alive_bar(len(indexComp)) as bar:
            for comp in range(len(indexComp)):
                comp_index_file.write(f"{comp},{indexComp[comp]}\n")
                bar()

    #SummaryBugs.csv File
    sum_file = folder+"UltimateData\\SummaryBugs.csv"
    print(f"File: {sum_file}")
    with open(sum_file,"w", encoding="utf-8") as sum_file:
        with alive_bar(len(summaryBugs)) as bar:
            for sum in range(len(summaryBugs)):
                try:
                    sum_file.write(f"{summaryBugs[sum][0]},{summaryBugs[sum][1]}\n")
                except:
                    print(f"{Bugs[sum]}")
                bar()

    #SummaryTestss.csv File
    sum_file = folder+"UltimateData\\SummaryTests.csv"
    print(f"File: {sum_file}")
    with open(sum_file,"w", encoding="utf-8") as sum_file:
        with alive_bar(len(summaryTests)) as bar:
            for sum in range(len(summaryTests)):
                try:
                    sum_file.write(f"{summaryTests[sum][0]},{summaryTests[sum][1]}\n")
                except:
                    print(f"{Tests[sum]}")
                bar()
    

    TestExecsClosed = []
    TestExecsVerify = []

    #SBert_Bug.csv File
    interactions_filename = folder+"UltimateData\\Interacoes.csv"
    print(f"File: {interactions_filename}")
    with open(interactions_filename,"w") as interactions_file:
        allFiles = os.listdir(folder+"TestExecution\\")
        with alive_bar(len(allFiles)) as bar:
            for key in allFiles:
                bar()
                file_status = folder+"TestExecution\\"+key+"\\status.txt"
                if (FileCheck(file_status)):
                    with open(file_status, encoding="utf-8") as my_file:
                        status = my_file.read().replace("\n","")
                    if text == "":
                        status = "None"
                else:
                    print(f"File not found: {file_status}")
                    status = "None"

                if status == "New" or status == "In Progress":
                    if key not in TestExecsVerify:
                        TestExecsVerify.append(key)
                elif status == "Closed":
                    if key not in TestExecsClosed:
                        TestExecsClosed.append(key)

                    file_date = folder+"TestExecution\\"+key+"\\resolutiondate.txt"
                    if (FileCheck(file_date)):
                        with open(file_date, encoding="utf-8") as my_file:
                            dateTE = my_file.read().split(".")[0].replace("T"," ")[:-3]
                        if dateTE == "":
                            print(f"Date not found: {file_date}")
                            dateTE = "None"
                    else:
                        print(f"File not found: {file_date}")
                        dateTE = "None"

                    minutesTest = dateMinutes(dateTE)

                    TestExecsv = folder+"CSV\\"+key+".csv"
                        
                    dataLinks = carregaCSV(TestExecsv)[1:]
                    
                    for link in dataLinks:
                        if link[0] in Tests:
                            testId = Tests.index(link[0])
                            blinks = link[6].split(",")
                            for b in blinks:
                                if b in Bugs:
                                    bugId = Bugs.index(b)
                                    interactions_file.write(f"{testId},{bugId},1,{minutesTest}\n")
                        
                        

    #TestExecsClosed.csv File
    TestExecsClosed_file = folder+"UltimateData\\TestExecsClosed.csv"
    print(f"File: {TestExecsClosed_file}")
    with open(TestExecsClosed_file,"w") as TestExecsClosed_file_file:
        with alive_bar(len(TestExecsClosed)) as bar:
            for test in range(len(TestExecsClosed)):
                TestExecsClosed_file_file.write(f"{TestExecsClosed[test]}\n")
                bar()

    #TestExecsVerify.csv File
    TestExecsVerify_file = folder+"UltimateData\\TestExecsVerify.csv"
    print(f"File: {TestExecsVerify_file}")
    with open(TestExecsVerify_file,"w") as TestExecsVerify_file_file:
        with alive_bar(len(TestExecsVerify)) as bar:
            for test in range(len(TestExecsVerify)):
                TestExecsVerify_file_file.write(f"{TestExecsClosed[test]}\n")
                bar()


    print("Fim")
    return



def test_execution_csv(folder):
    allFiles = os.listdir(folder+"CSV\\")
    with alive_bar(len(allFiles)) as bar:
        for csvname in allFiles:
            bar()
            TestExecsv = folder+"CSV\\"+csvname
            
            data = carregaCSV(TestExecsv)[1:]
            for i in range(len(data)):
                if len(data[i])!= 10:
                    print(f"{TestExecsv} - Line {i}")
            
            



def carregaCSV(file):
    f = open(file, encoding="utf8")
    dataCSV = f.read()
    f.close()
    pos = dataCSV.find("\n")
    if pos >= 0:
        cabeca = []
        for elemento in dataCSV[:pos].split(";"):
            cabeca.append(elemento.strip())
        dataCSV = dataCSV[pos:].split(";")
        data = []
        data.append(cabeca)
        for i in range(0, len(dataCSV), len(cabeca)):
            if dataCSV[i : i + len(cabeca)] != [""]:
                dat = []
                for elemento in dataCSV[i : i + len(cabeca)]:
                    dat.append(elemento.strip())
                data.append(dat)

        for i in range(len(data)):
            data[i][0] = data[i][0].replace("\n", "")
        return data
    return [[d.strip() for d in dataCSV.split(";")]]