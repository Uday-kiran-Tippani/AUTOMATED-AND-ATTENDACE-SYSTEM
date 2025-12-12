import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar

class ScrollableFrame(tk.Frame):
    def __init__(self, master, width=800, height=400, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.canvas = Canvas(self, width=width, height=height)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        # Make the inner frame expand and resize
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Optional: mouse wheel scrolling
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        # Windows and MacOS compatible
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
