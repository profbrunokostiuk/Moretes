import tkinter as tk
from src.ui.app_frame import AppFrame


class RecommendationScreen(AppFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

        self.label = tk.Label(self, text="Recommended Tests: ")
        self.label.grid(row=0, column=0, columnspan=5, sticky="EW")
        

        self.list_box = tk.Listbox(self, width=80, height=21, selectmode="multiple")
        for item in range(len(self.context)-1):
            self.list_box.insert(item, f"{self.context[item+1].id} - {self.context[item+1].title}")
        self.list_box.grid(row=1, column=0, columnspan=5, pady=10)

        

        self.back_button = tk.Button(self, text="Save", command=self.goto_main)
        self.back_button.grid(row=3+len(self.context), column=0, columnspan=5, pady=10, sticky="EW")

        self.back_button = tk.Button(self, text="Cancel", command=self.goto_main_cancel)
        self.back_button.grid(row=4+len(self.context), column=0, columnspan=5, pady=10, sticky="EW")

   
        
    def goto_main(self):

        values = [idx for idx in self.list_box.curselection()]

        positives=[]
        negatives=[]

        for i in range(len(self.context)-1):
            if i in values:
                positives.append(self.context[i+1].id)
            else:
                negatives.append(self.context[i+1].id)

        self.app.model.register_interactions(bugId=self.context[0].id, positives=positives, negatives=negatives)
        self.app.model.update_model(self.context[0].id, positives, negatives)
        self.app.ui.draw_frame(self.app.ui.screen.Main)

    def goto_main_cancel(self):
        self.app.ui.draw_frame(self.app.ui.screen.Main)