import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.app_frame import AppFrame

class MainScreen(AppFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        # Team dropdown menu
        self.team_label = tk.Label(self, text="Select Team:")
        self.team_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(self, textvariable=self.team_var, values=app.model.teams, state="readonly", width=50)
        self.team_dropdown.grid(row=0, column=3, columnspan=3)
        self.team_dropdown.current(0)

        # Components dropdown menu
        self.comp_label = tk.Label(self, text="Select Component:")
        self.comp_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        self.comp_var = tk.StringVar()
        self.comp_dropdown = ttk.Combobox(self, textvariable=self.comp_var, values=app.model.comps, state="readonly", width=50)
        self.comp_dropdown.grid(row=1, column=3, columnspan=3)
        self.comp_dropdown.current(0)

        self.textarea_key_label = tk.Label(self, text="Bug Key:")
        self.textarea_key_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        self.textarea_key = tk.Text(self, width=40, height=1)
        self.textarea_key.grid(row=2, column=3,columnspan=3)

        self.textarea_sum_label = tk.Label(self, text="Bug Title:")
        self.textarea_sum_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        self.textarea_sum = tk.Text(self, width=40, height=1)
        self.textarea_sum.grid(row=3, column=3,columnspan=3)

        self.textarea_label = tk.Label(self, text="Bug description:")
        self.textarea_label.grid(row=4, column=0, sticky=tk.W)

        self.textarea = tk.Text(self, width=60, height=30)
        self.textarea.grid(row=5, column=0, columnspan=5)

        self.submit_button = tk.Button(self, text="Recommend Tests", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=5, pady=10, sticky="EW")

        self.save_button = tk.Button(self, text="Save model to file", command=self.save_model_confirm)
        self.save_button.grid(row=7, column=0, columnspan=5, pady=10, sticky="EW")

        self.save_button = tk.Button(self, text="Manually add a test to the model", command=self.add_test_to_model)
        self.save_button.grid(row=8, column=0, columnspan=5, pady=10, sticky="EW")

        self.save_button = tk.Button(self, text="Manually add a bug to the model", command=self.add_bug_to_model)
        self.save_button.grid(row=9, column=0, columnspan=5, pady=10, sticky="EW")

        self.save_button = tk.Button(self, text="Update model from CSV", command=self.update_model_from_csv)
        self.save_button.grid(row=10, column=0, columnspan=5, pady=10, sticky="EW")


    def add_test_to_model(self):
         self.app.ui.draw_frame(self.app.ui.screen.AddTest,{'key':'','summary':'','steps':[]})

    def add_bug_to_model(self):
         self.app.ui.draw_frame(self.app.ui.screen.AddBug,{'key':'','summary':'','desc':''})

    def update_model_from_csv(self):
         self.app.ui.draw_frame(self.app.ui.screen.Update)


    def save_model_confirm(self):
        ans = messagebox.askquestion("Confirm Change","Are you sure you want to replace the model file??")
        if ans == "yes":
            self.app.model.teams = sorted(self.app.model.teams) #reseta lista de times
            self.app.model.comps = sorted(self.app.model.comps) #reseta lista de componentes
            self.app.save_model()
        self.app.ui.draw_frame(self.app.ui.screen.Main)


    def submit(self):
        selected_team = self.app.model.teams[self.team_dropdown.current()]

        self.app.model.teams.remove(selected_team)
        self.app.model.teams.insert(0,selected_team)

        selected_component = self.app.model.comps[self.comp_dropdown.current()]
        self.app.model.comps.remove(selected_component)
        self.app.model.comps.insert(0,selected_component)


        info = self.textarea.get(1.0, tk.END)
        summary = self.textarea_sum.get(1.0, tk.END).replace("\n","").strip()
        key = self.textarea_key.get(1.0, tk.END).replace("\n","").strip()

        if key == "EXTRACT_INTERACTIONS":
            self.app.model.extract_interactions()
            self.app.ui.draw_frame(self.app.ui.screen.Main)
            return
        
        if key == "": 
            if len(info) <= 1:
                messagebox.showwarning("No description or key", f"Please provide a description or a key")
                self.app.ui.draw_frame(self.app.ui.screen.Main)
                return
            else: 
                best, emb, percent = self.app.model.SBertSimilarity(text=info)
                if percent > 0.95: 
                    ans = messagebox.askquestion("Confirm Bug", f"Your Bug has {percent*100:.0f}% similar to \"{self.app.model.list_Bug[best].key} - {self.app.model.list_Bug[best].summary}\"\nIs it another Bug?")
                    if ans == "yes":
                        if summary == "":
                            messagebox.showwarning("No key and summary", f"Please provide a key and summary")
                            self.app.ui.draw_frame(self.app.ui.screen.Main)
                            return
                        else:
                            messagebox.showwarning("No key", f"Please provide a key")
                            self.app.ui.draw_frame(self.app.ui.screen.Main)
                            return
                    else: 
                        bug = self.app.model.list_Bug[best]
                else:
                    if summary == "":
                        messagebox.showwarning("No key and summary", f"Please provide a key and summary")
                        self.app.ui.draw_frame(self.app.ui.screen.Main)
                        return
                    else:
                        messagebox.showwarning("No key", f"Please provide a key")
                        self.app.ui.draw_frame(self.app.ui.screen.Main)
                        return
        else:
            try:
                bug = self.app.model.list_Bug[key]
            except:
                if len(info) <= 1:
                    if summary == "": 
                        messagebox.showwarning("Bug not found", f"Please provide a description and summary to insert the new bug")
                        self.app.ui.draw_frame(self.app.ui.screen.Main)
                        return
                    else:
                        messagebox.showwarning("Bug not found", f"Please provide a description to insert the new bug")
                        self.app.ui.draw_frame(self.app.ui.screen.Main)
                        return
                else:
                    best, emb, percent = self.app.model.SBertSimilarity(text=info)
                    if percent > 0.95: 
                        ans = messagebox.askquestion("Confirm Bug", f"Your Bug {key} is not found, but has {percent*100:.0f}% similar to \"{self.app.model.list_Bug[best].key} - {self.app.model.list_Bug[best].summary}\"\nIs it another Bug?")
                        if ans == "yes":
                            if summary == "":
                                messagebox.showwarning("No summary", f"Please provide a summary")
                                self.app.ui.draw_frame(self.app.ui.screen.Main)
                                return
                            else:
                                self.app.model.insert_Bug(encode_text = emb, id = best, comp=selected_component, team=selected_team, key=key, opt=percent, title=summary)
                                bug = self.app.model.list_Bug[key]
                        else: 
                            bug = self.app.model.list_Bug[best]
                    else:
                        if summary == "":
                            messagebox.showwarning("No summary", f"Please provide a summary")
                            self.app.ui.draw_frame(self.app.ui.screen.Main)
                            return
                        else:
                            self.app.model.insert_Bug(encode_text = emb, id = best, comp=selected_component, team=selected_team, key=key, opt=percent, title=summary)
                            bug = self.app.model.list_Bug[key]


        recomend = self.app.model.recommend(bug,[16,2,2])
        lista = [bug]
        for i in recomend:
            lista.append(self.app.model.list_Test[i])


        # TODO
        

        

        self.app.ui.draw_frame(self.app.ui.screen.Recommendation, lista)
        # self.textarea.delete(1.0, tk.END)  # Clear previous content
        # self.textarea.insert(tk.END, info)
