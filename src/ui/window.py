import tkinter as tk
from typing import Any

from src.ui.screens import Screen


class Window(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.screen = Screen
        self.resizable(True, True)
        self.title("Moretes")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

    def draw_frame(self, screen_enum: Screen, context: Any = None, **kwargs):
        frame = screen_enum.value(self.app, context=context, padx=20, pady=20, **kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
