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
board.createPiece(PieceType.ROOK, Color.WHITE, 1, 1)
board.drawBoard(canvas)

rook = Piece(1, PieceType.ROOK, Color.WHITE)
rook.draw(canvas, 0, 0, 64)

root.mainloop()