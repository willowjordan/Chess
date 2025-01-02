'''
TO DO:
    - Fix circular import issue
    - Finish pieces' move functions
    - Implement king check/checkmate detection
    - Implement castling
    - Add visual representation (tkinter)
    - Implement promotion
    - Implement pawn capture recognition
    - Implement en passant
'''

from board import *

import tkinter as tk
import time

root = tk.Tk()
canvas = tk.Canvas(root, width=128*5, height=128*5)
canvas.pack()

board = Board()
board.initialize()
board.drawBoard(canvas)

root.mainloop()