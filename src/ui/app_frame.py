import tkinter as tk


class AppFrame(tk.Frame):
    def __init__(self, app, context=None, **kwargs):
        super().__init__(app.ui.container, **kwargs)
        self.context = context
        self.app = app
