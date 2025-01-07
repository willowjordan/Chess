'''
TO DO:
    - Find a way to delete unused objects from the canvas
    - Update isThreatened() to include threats from enemy kings
    - Make it so when a player is in check, they can only make moves to get out of chess
    - Implement king check/checkmate detection
    - Implement castling
    - Implement promotion
    - Implement turns
'''

from board import *

import tkinter as tk
import time

def foo ():
    print("bar")

root = tk.Tk()
boardCanvas = tk.Canvas(root, width=128*6, height=128*6)
boardCanvas.pack()

board = Board((10, 10), root, boardCanvas)
board.initialize() # this will start the game

boardCanvas.mainloop()