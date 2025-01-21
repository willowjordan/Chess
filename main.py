'''
TO DO:
    - More testing
    - Find a way to delete unused objects from the canvas
    - Implement promotion
    - Title screen/game over screen
'''

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

'''subCanvas = tk.Canvas(root, width=448, height=192, bg="lightgray")
window = boardCanvas.create_window(10+32, 10+160, width=448, height=192, anchor = tk.NW, window=subCanvas)
rect = subCanvas.create_rectangle((1, 1), (447, 191), outline='black', width=2)
txt = subCanvas.create_text((200,30), text="Select a piece to promote your pawn to:", font="tkDefaultFont 14")
rookButton = subCanvas.create_rectangle((39, 64), (103, 128), fill="#b465e5")
knightButton = subCanvas.create_rectangle((141, 64), (205, 128), fill="#b465e5")
bishopButton = subCanvas.create_rectangle((243, 64), (307, 128), fill="#b465e5")
queenButton = subCanvas.create_rectangle((345, 64), (409, 128), fill="#b465e5")'''

boardCanvas.mainloop()

# TODO: results screen, maybe option to start a new game or return to title?
boardCanvas.pack_forget()