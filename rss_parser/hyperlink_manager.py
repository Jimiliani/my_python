from tkinter import *
import webbrowser

links = {}


class HyperlinkManager:
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

    def add(self, action):
        tag = "hyper-%d" % len(links)
        links[tag] = action
        return "hyper", tag

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                webbrowser.open(links[tag], new=2)
                return
