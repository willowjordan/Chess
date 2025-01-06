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

def foo ():
    print("bar")

root = tk.Tk()
canvas = tk.Canvas(root, width=128*6, height=128*6)
canvas.pack()

board = Board((10, 10))
board.initialize()
board.drawBoard(root, canvas)

'''bgImage = ImageTk.PhotoImage(Image.open("./sprites/black_rook.png"))
#button = tk.Button(root, command= lambda: self.handleClick(a, b), image=bgImage)
button = tk.Button(root, command=foo, text="", image=bgImage)
button.configure(background="#e2d2a1")
button_window = canvas.create_window(10, 10, width=64, height=64, anchor=tk.NW, window=button)'''

root.mainloop()