from board import *

# a special board WITH GRAPHICAL REPRESENTATION that will be used as the main board for the game
class MainBoard(Board):
    LIGHT_SQUARE_COLOR = "#e2d2a1"
    DARK_SQUARE_COLOR = "#ae9f70"
    SELECTED_SQUARE_COLOR = "#6ce565"
    NORMAL_MOVE_COLOR = "#65a2e5"
    CAPTURE_MOVE_COLOR = "#e56565"
    SPECIAL_MOVE_COLOR = "#b465e5"
    CHECK_COLOR = ""

    @staticmethod
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
    
    # pos = (x, y) coordinates for the top left corner of the board to be drawn at
    def __init__ (self, pos, root, canvas):
        Board.__init__(self)
        
        # graphical variables
        self.pos = pos
        self.root = root
        self.canvas = canvas
        self.selected_square = (-1, -1)
    
        # generate images as static object when class is created
        self.imgs:dict = {}
        dirpath = "./sprites/"
        filenames = next(walk(dirpath), (None, None, []))[2]
        for fname in filenames:
            key = MainBoard.filenameToKey(fname)
            path = dirpath + fname
            img = tk.PhotoImage(file=path).zoom(2, 2)
            self.imgs[key] = img
    
    def getImage(self, pos):
        key = self.getSpace((pos))
        img = self.imgs[key]
        return img
    
    def movePiece (self, startPos, endPos):
        Board.movePiece(self, startPos, endPos)
        self.changeTurns()
    
    # draw the board using tkinter
    def drawBoard (self):
        squaresToHighlight = []
        if (self.selected_square != (-1, -1)):
            squaresToHighlight = self.getMoves(self.selected_square)
        light_square = True
        # clear the canvas
        self.canvas.delete("all")
        # create a button for every square on the board
        for i in range(0, 512, 64):
            for j in range(0, 512, 64):
                # positioning variables
                x = self.pos[0] + i
                y = self.pos[1] + j
                a = i // 64 + 1
                b = j // 64 + 1

                # get square's background color
                bgColor: str
                if (light_square): bgColor = MainBoard.LIGHT_SQUARE_COLOR
                else: bgColor = MainBoard.DARK_SQUARE_COLOR
                if (self.selected_square == (a, b)): bgColor = MainBoard.SELECTED_SQUARE_COLOR
                if (a, b) in squaresToHighlight:
                    bgColor = MainBoard.NORMAL_MOVE_COLOR

                # create button
                button: tk.Button
                if self.getSpace((a, b)) != "XX":
                    img = self.getImage((a, b))
                    button = tk.Button(self.root, width=64, height=64, command=self.handleClick, text="", image=img)
                else:
                    button = tk.Button(self.root, width=64, height=64, command=self.handleClick, text="")
                
                # place button
                button.configure(background=bgColor)
                button_window = self.canvas.create_window(x, y, width=64, height=64, anchor=tk.NW, window=button)

                # flip square color
                light_square = not light_square
            # flip square color
            light_square = not light_square

        # draw grid lines

    # handle the square at (x, y) being clicked
    # for spaces with friendly pieces, select that piece and show its moves
    # click again to deselect, or click one of those spaces to make the move
    def handleClick (self):
        # determine which button was clicked based on cursor position
        x = (self.root.winfo_pointerx() - self.root.winfo_rootx() - self.pos[0]) // 64 + 1
        y = (self.root.winfo_pointery() - self.root.winfo_rooty() - self.pos[1]) // 64 + 1
        clickPos = (x, y)
        
        if self.selected_square == (-1, -1): # no square selected
            if self.getSpace(clickPos) != "XX":
                if (self.curr_player == self.getSpace(clickPos)[0]): #space occupied by friendly piece
                    self.selected_square = clickPos
                    self.drawBoard() #redraw board to show changes
        else: #square selected
            moves = self.getMoves(self.selected_square)
            if clickPos in moves:
                self.movePiece(self.selected_square, clickPos)
                self.selected_square = (-1, -1)
                self.drawBoard()
                return
            prevPos = self.selected_square
            self.selected_square = (-1, -1) #deselect
            if self.getSpace(clickPos) != "XX":
                if (self.getSpace(clickPos)[0] == self.curr_player) & (clickPos != prevPos): #if clicking on a different friendly piece, select
                    self.selected_square = clickPos
            self.drawBoard()

    # take all end-of-turn actions, switch players, and take all beginning of turn actions for the next player
    # return end of game scenarios if necessary
    def changeTurns (self):
        # end of turn actions
        # remove en passant counters if necessary
        movesToRemove = []
        for pos in self.ep_moves.keys():
            piece = self.getSpace(pos)
            if (piece[0] == self.curr_player) | (piece[0] == "X"):
                movesToRemove.append(pos)
        for pos in movesToRemove:
            self.ep_moves.pop(pos)
        
        # change sides
        self.curr_player = Board.oppColor(self.curr_player)

        # beginning of turn actions
        # check for check/checkmate
        self.updateGameState()
        if self.game_state == GameState.CHECKMATE:
            self.endGame(Board.oppColor(self.curr_player))
        elif self.game_state == GameState.STALEMATE:
            self.endGame("X")
        
        print(self.castling_options) #DEBUG

    def endGame (self, winner):
        self.winner = winner
        self.canvas.delete("all")
        self.canvas.quit()