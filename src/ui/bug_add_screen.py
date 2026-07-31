import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.app_frame import AppFrame



class BugAddScreen(AppFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        

        self.label = tk.Label(self, text="Add Bugs:")
        self.label.grid(row=0, column=0, columnspan=5, sticky="EW")
        

        self.team_label = tk.Label(self, text="Select Team:")
        self.team_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        self.team_var = tk.StringVar()
        self.team_dropdown = ttk.Combobox(self, textvariable=self.team_var, values=app.model.teams, state="readonly", width=50)
        self.team_dropdown.grid(row=1, column=3, columnspan=3)
        self.team_dropdown.current(0)

        self.comp_label = tk.Label(self, text="Select Component:")
        self.comp_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

        self.comp_var = tk.StringVar()
        self.comp_dropdown = ttk.Combobox(self, textvariable=self.comp_var, values=app.model.comps, state="readonly", width=50)
        self.comp_dropdown.grid(row=2, column=3, columnspan=3)
        self.comp_dropdown.current(0)

        self.textarea_key_label = tk.Label(self, text="Bug Key (jira):")
        self.textarea_key_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        self.textarea_key = tk.Text(self, width=40, height=1)
        self.textarea_key.grid(row=3, column=3,columnspan=3)
        self.textarea_key.delete(1.0, tk.END)
        self.textarea_key.insert(tk.END, self.context['key'])


        self.textarea_sum_label = tk.Label(self, text="Bug Summary (jira):")
        self.textarea_sum_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)
        

        self.textarea_sum = tk.Text(self, width=40, height=1)
        self.textarea_sum.grid(row=4, column=3,columnspan=3)
        self.textarea_sum.delete(1.0, tk.END)
        self.textarea_sum.insert(tk.END, self.context['summary'])
        

        self.textarea_label = tk.Label(self, text="Bug description:")
        self.textarea_label.grid(row=4, column=0, sticky=tk.W)

        self.textarea = tk.Text(self, width=60, height=30)
        self.textarea.grid(row=5, column=0, columnspan=5)
        self.textarea.delete(1.0, tk.END)
        self.textarea.insert(tk.END, self.context['desc'])
        
        self.back_button = tk.Button(self, text="Save", command=self.goto_main)
        self.back_button.grid(row=9, column=0, columnspan=5, pady=10, sticky="EW")

    
    def goto_main(self):
        summary = self.textarea_sum.get(1.0, tk.END).replace("\n","").strip()
        key = self.textarea_key.get(1.0, tk.END).replace("\n","").strip()
        desc = self.textarea.get(1.0, tk.END)
        desc = desc[:len(desc)-1]

        if summary == "" or key == "" or desc == "":
            messagebox.showwarning("No key or summary or description", f"Please provide a key and summary and description")
            self.app.ui.draw_frame(self.app.ui.screen.AddBug, {'key':key,'summary':summary,'desc':desc})
            
        else:
            selected_team = self.app.model.teams[self.team_dropdown.current()]
            self.app.model.teams.remove(selected_team)
            self.app.model.teams.insert(0,selected_team)

            selected_component = self.app.model.comps[self.comp_dropdown.current()]
            self.app.model.comps.remove(selected_component)
            self.app.model.comps.insert(0,selected_component)
        

            self.app.model.insert_new_bug(key, desc, summary, str(selected_team.id), str(selected_component.id))

            self.app.ui.draw_frame(self.app.ui.screen.Main)
