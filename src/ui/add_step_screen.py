import tkinter as tk
from src.ui.app_frame import AppFrame


class AddStepScreen(AppFrame):
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        

        self.label = tk.Label(self, text="Step Information: ")
        self.label.grid(row=0, column=0, columnspan=5, sticky="EW")
       
        self.textarea_action_Label = tk.Label(self, text="Action:")
        self.textarea_action_Label.grid(row=1, column=0, sticky=tk.W)

        self.textarea_action = tk.Text(self, width=60, height=10)
        self.textarea_action.grid(row=2, column=0, columnspan=5)


        self.textarea_data_Label = tk.Label(self, text="Data:")
        self.textarea_data_Label.grid(row=3, column=0, sticky=tk.W)

        self.textarea_data = tk.Text(self, width=60, height=10)
        self.textarea_data.grid(row=4, column=0, columnspan=5)

        self.textarea_eResult_Label = tk.Label(self, text="Expected Result:")
        self.textarea_eResult_Label.grid(row=5, column=0, sticky=tk.W)

        self.textarea_eResult = tk.Text(self, width=60, height=10)
        self.textarea_eResult.grid(row=6, column=0, columnspan=5)

        
        
        self.back_button = tk.Button(self, text="Add", command=self.goto_main_add)
        self.back_button.grid(row=9, column=0, columnspan=5, pady=10, sticky="EW")

        self.back_button = tk.Button(self, text="Cancel", command=self.goto_main_cancel)
        self.back_button.grid(row=10, column=0, columnspan=5, pady=10, sticky="EW")

    
    def goto_main_add(self):
        steps = self.context['steps']

        action = self.textarea_action.get(1.0, tk.END).replace("\n","").strip()
        data = self.textarea_data.get(1.0, tk.END).replace("\n","").strip()
        eresult = self.textarea_eResult.get(1.0, tk.END).replace("\n","").strip()

        if action == '':
            self.app.ui.draw_frame(self.app.ui.screen.AddTest, {'key':self.context['key'],'summary':self.context['summary'],'steps':self.context['steps']})
        else:
            steps.append([action,data,eresult])
            self.app.ui.draw_frame(self.app.ui.screen.AddTest, {'key':self.context['key'],'summary':self.context['summary'],'steps':steps})

    def goto_main_cancel(self):
        self.app.ui.draw_frame(self.app.ui.screen.AddTest, {'key':self.context['key'],'summary':self.context['summary'],'steps':self.context['steps']})
