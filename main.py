'''
TO DO:
    - More testing?
    - Smart redraw function to reduce visual stutter?
    - Title screen/game over screen
    - Add AI opponents?
    - Add online multiplayer (shell programming?)?
'''

from main_board import *

import tkinter as tk
from tkinter import ttk
import time

'''def tkinter_input(prompt=""):
    root = tk.Tk()
    tk.Label(root, text=prompt).pack()
    option_var = tk.StringVar(root)
    options = ("Rook", "Knight", "Bishop", "Queen")
    entry = ttk.OptionMenu(root, option_var, "Rook", "Rook", "Knight", "Bishop", "Queen")
    entry.pack()
    result = None
    def callback():
        nonlocal result
        result = option_var.get()
        root.destroy()
    button = tk.Button(root, text="OK", command=callback)
    button.pack()
    root.mainloop()
    return result

result = tkinter_input("Choose a piece to promote to")
print(result)'''

root = tk.Tk()

# TODO: title screen?
titleCanvas = tk.Canvas(root, width=612, height=612)
titleCanvas.pack()
bg = tk.PhotoImage(file="./sprites/chess_board.png")
titleCanvas.create_image(0, 0, image=bg, anchor=tk.NW)
titleCanvas.create_rectangle((180, 70), (432, 130), fill="white", width=0)
titleCanvas.create_text(306, 100, text="CHESS", font=("DejaVu Sans", 48), anchor=tk.CENTER, fill="black")

def startGame():
    titleCanvas.quit()

startBtn = tk.Button(root, width=128, height=48, command=startGame, text="Start", background="lightgreen")
titleCanvas.create_window(306, 306, width=128, height=48, anchor=tk.CENTER, window=startBtn)
titleCanvas.mainloop()

# create main canvas/board and start the game
titleCanvas.pack_forget()
boardCanvas = tk.Canvas(root, width=612, height=612)
boardCanvas.pack()
mainb = MainBoard((50, 50), root, boardCanvas)
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
#boardCanvas.pack_forget()
print("Winner was " + str(mainb.winner))