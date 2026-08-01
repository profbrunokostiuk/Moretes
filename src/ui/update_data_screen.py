import tkinter as tk
from src.ui.app_frame import AppFrame
import src.dataColect.jiraColect as jiraColect

class Teams_Comps:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return self.name

class UpdateDataScreen(AppFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        

        self.label = tk.Label(self, text="Update Model: ")
        self.label.grid(row=0, column=0, columnspan=5, sticky="EW")
       
        self.textarea_bug_label = tk.Label(self, text="Add Bugs from:")
        self.textarea_bug_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        #last_bug = 0
        # for bug in self.app.model.list_Bug:
        #     if int(bug.key.replace("SP7-","")) > last_bug:
        #         last_bug = int(bug.key.replace("SP7-",""))

        self.textarea_bug = tk.Text(self, width=40, height=1)
        self.textarea_bug.grid(row=1, column=3,columnspan=3)
        self.textarea_bug.delete(1.0, tk.END)
        #self.textarea_bug.insert(tk.END, "SP7-"+str(last_bug))

        #last_test = 0
        # for test in self.app.model.list_Test:
        #     if int(test.key.replace("SP7-","")) > last_test:
        #         last_test = int(test.key.replace("SP7-",""))

        self.textarea_test_label = tk.Label(self, text="Add Tests from:")
        self.textarea_test_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        self.textarea_test = tk.Text(self, width=40, height=1)
        self.textarea_test.grid(row=2, column=3,columnspan=3)
        self.textarea_test.delete(1.0, tk.END)
        #self.textarea_test.insert(tk.END, "SP7-"+str(last_test))


        self.textarea_server_label = tk.Label(self, text="Server:")
        self.textarea_server_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        self.textarea_server = tk.Text(self, width=40, height=1)
        self.textarea_server.grid(row=3, column=3,columnspan=3)
        self.textarea_server.delete(1.0, tk.END)
        self.textarea_server.insert(tk.END, "jira link")

        self.textarea_apikey_Label = tk.Label(self, text="API Jira Key:")
        self.textarea_apikey_Label.grid(row=4, column=0, sticky=tk.W)

        self.textarea_apikey = tk.Text(self, width=60, height=10)
        self.textarea_apikey.grid(row=5, column=0, columnspan=5)

        self.add_button = tk.Button(self, text="Confirm", command=self.add_itens)
        self.add_button.grid(row=8, column=0, columnspan=5, pady=10, sticky="EW")

        
        self.back_button = tk.Button(self, text="Cancel", command=self.goto_main)
        self.back_button.grid(row=9, column=0, columnspan=5, pady=10, sticky="EW")
    
    def goto_main(self):
        self.app.ui.draw_frame(self.app.ui.screen.Main)

    def add_itens(self):
        
        API_Key = self.textarea_apikey.get(1.0, tk.END).replace("\n","").strip()
        last_test = self.textarea_test.get(1.0, tk.END).replace("\n","").strip()
        last_bug = self.textarea_bug.get(1.0, tk.END).replace("\n","").strip()
        server = self.textarea_server.get(1.0, tk.END).replace("\n","").strip()

        bug_colect_error = 0
        test_colect_error = 0

        total_bug = 0
        total_test= 0
        try:
            if last_bug != "":
                list_Bugs = jiraColect.getBugsFromJira(API_Key,server,last_bug)

            for bug in list_Bugs:
                if bug['key'].strip() not in self.app.model.dic_Bug:
                    total_bug+=1
                    comps = []
                    for comp in bug['comps']:
                        findComp = False
                        for comp_model in self.app.model.comps:
                            if str(comp_model) == comp.strip():
                                comps.append(comp_model.id)
                                findComp = True
                        if not findComp:
                            comps.append(len(self.app.model.comps))
                            self.app.model.comps.append(Teams_Comps(len(self.app.model.comps),comp))

                    teams = []
                    for team in bug['teams']:
                        findTeam = False
                        for team_model in self.app.model.teams:
                            if str(team_model) == team.strip():
                                teams.append(team_model.id)
                                findTeam = True
                        if not findTeam:
                            teams.append(len(self.app.model.teams))
                            self.app.model.teams.append(Teams_Comps(len(self.app.model.teams),team))
                    
                    self.app.model.insert_new_bug(bug['key'], bug['desc'], bug['summary'], str(teams).replace("[","").replace("]","").replace(",","#"), str(comps).replace("[","").replace("]","").replace(",","#"))
        except:
            #tk.messagebox.showwarning("Error collecting Bugs", f"Trying to collect tests")
            bug_colect_error = 1

        try:
            if last_test != "":
                list_Test = jiraColect.getTestsFromJira(API_Key,server,last_test)
            for test in list_Test:
                if test['key'].strip() not in self.app.model.dic_Test:
                    total_test+=1
                    comps = []
                    for comp in test['comps']:
                        findComp = False
                        for comp_model in self.app.model.comps:
                            if str(comp_model) == comp.strip():
                                comps.append(comp_model.id)
                                findComp = True
                        if not findComp:
                            comps.append(len(self.app.model.comps))
                            self.app.model.comps.append(Teams_Comps(len(self.app.model.comps),comp))

                    teams = []
                    for team in test['teams']:
                        findTeam = False
                        for team_model in self.app.model.teams:
                            if str(team_model) == team.strip():
                                teams.append(team_model.id)
                                findTeam = True
                        if not findTeam:
                            teams.append(len(self.app.model.teams))
                            self.app.model.teams.append(Teams_Comps(len(self.app.model.teams),team))
                    

            
                    self.app.model.insert_new_test(test['key'], test['steps'], test['summary'], str(teams).replace("[","").replace("]","").replace(",","#"), str(comps).replace("[","").replace("]","").replace(",","#"))
        except:
            #tk.messagebox.showwarning("Error collecting Tests", f"Try again")
            test_colect_error = 1
        #messagebox.showwarning("Data Update", f"{len(list_Test)} New Test(s) and {list_Bugs} new Bug(s) were added to the model")
        
        if test_colect_error == 1:
            if bug_colect_error == 1:
                tk.messagebox.showwarning("Error collecting Tests and Bugs", f"An error occurred while collecting tests and bugs, check your API key and try again")
            else:
                tk.messagebox.showwarning("Error collecting Tests", f"An error occurred while collecting tests, check your API key and try again")
        else:
            if bug_colect_error == 1:
                tk.messagebox.showwarning("Error collecting Bugs", f"An error occurred while collecting bugs, check your API key and try again")
            else:
                tk.messagebox.showwarning("Data collected successfully", f"{total_test} tests and {total_bug} bugs were collected! Don't forget to save the model!")
        self.app.ui.draw_frame(self.app.ui.screen.Main)
