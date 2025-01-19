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
from main_board import *

import tkinter as tk
import time

root = tk.Tk()

# TODO: title screen?

# create main canvas/board and start the game
boardCanvas = tk.Canvas(root, width=128*6, height=128*6)
boardCanvas.pack()
mainb = MainBoard((10, 10), root, boardCanvas)
mainb.drawBoard()
boardCanvas.mainloop()

# TODO: results screen, maybe option to start a new game or return to title?
boardCanvas.pack_forget()