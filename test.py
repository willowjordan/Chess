# test script for the Board class
from board import *

import tkinter as tk
import time

root = tk.Tk()
boardCanvas = tk.Canvas(root, width=128*6, height=128*6)
boardCanvas.pack()

'''createPiece'''
board = Board((10, 10), root, boardCanvas)

'''removePiece'''

'''movePiece'''

'''initialize'''

'''isThreatened'''

'''getMoves'''

'''getAllMoves'''

'''checkForStalemate'''

'''changeTurns'''