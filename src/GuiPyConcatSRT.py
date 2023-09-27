# -*- coding: utf-8 -*-
"""
"""


import tkinter as tk
from tkinter import ttk, Tk
from tkinter import filedialog, messagebox


class Gui(object):

    def __init__(self, main: Tk, debug: bool = False) -> None:
        self.debug = debug
        self.main = main



def main():
    root = Tk()
    gui = Gui(root)
    root.mainloop()



if __name__ == '__main__':
    main()
