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

root = tk.Tk()
boardCanvas = tk.Canvas(root, width=128*6, height=128*6)
boardCanvas.pack()

board = Board((10, 10), root, boardCanvas)
board.initialize() # this will start the game

boardCanvas.mainloop()