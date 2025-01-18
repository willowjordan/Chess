'''
TO DO:
    - Fix HypotheticalBoard
    - More testing
    - Find a way to delete unused objects from the canvas
    - Maybe refactor board.py into Board and MainBoard classes?
    - Implement king check/checkmate detection
    - Implement castling
    - Implement promotion
'''

from board import *

import tkinter as tk
import time

def filenameToKey(fname):
    if fname[0] == "t": return "XX" # special case: transparent image
    
    rv = fname[0].upper()
    currPos = 0
    while fname[currPos] != "_": currPos += 1 # advance to type string
    currPos += 1
    if fname[currPos] == "k": # special case: king or knight
        if fname[currPos+1] == "n": rv += "N"
        else: rv += "K"
    else: rv += fname[currPos].upper()
    return rv

root = tk.Tk()
boardCanvas = tk.Canvas(root, width=128*6, height=128*6)
boardCanvas.pack()

imgs:dict = {}
dirpath = "./sprites/"
filenames = next(walk(dirpath), (None, None, []))[2]
for fname in filenames:
    key = filenameToKey(fname)
    path = dirpath + fname
    img = tk.PhotoImage(file=path).zoom(2, 2)
    imgs[key] = img

boardCanvas.mainloop()