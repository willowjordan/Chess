from piece import *
import tkinter as tk
import copy

'''
NOTES:
    - Starting board position is (1, 1) in the top left, going to (8, 8) in the bottom right
'''
class GameState(Enum):
    NORMAL = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3

class Board:
    LIGHT_SQUARE_COLOR = "#e2d2a1"
    DARK_SQUARE_COLOR = "#ae9f70"
    SELECTED_SQUARE_COLOR = "#6ce565"
    NORMAL_MOVE_COLOR = "#65a2e5"
    CAPTURE_MOVE_COLOR = "#e56565"
    SPECIAL_MOVE_COLOR = "#b465e5"

    # pos = (x, y) coordinates for the top left corner of the board to be drawn at
    def __init__ (self, pos, root, canvas):
        self.spaces:dict = {} # this is the board itself
        self.whiteAlive:dict = {}
        self.whiteDead:dict = {}
        self.blackAlive:dict = {}
        self.blackDead:dict = {}
        self.max_x = 8
        self.max_y = 8
        self.piecesCreated = 0
        self.pos = pos
        self.root = root
        self.canvas = canvas
        self.curr_player = Color.WHITE # whose turn it is
        self.selected_square = (-1, -1) # the square of the piece currently selected by the player, (-1, -1) if no piece selected
        self.ep_clear_list = [] # list of en passant values to reset at the end of the turn
        self.game_state = GameState.NORMAL

    # create a new piece and insert it onto the board
    def createPiece (self, type, color, x, y):
        piece = Piece(self.piecesCreated+1, type, color, (x, y))
        self.piecesCreated += 1
        #maybe add error checking to make sure pieces aren't replaced?
        self.spaces[(x, y)] = piece
        if (piece.color == Color.WHITE):
            self.whiteAlive[piece.id] = piece
        else: #black
            self.blackAlive[piece.id] = piece
    
    # to be used ONLY FOR REMOVING PIECES FROM THE BOARD ENTIRELY
    # pos is a tuple representing (x, y) coordinates
    def removePiece (self, pos):
        piece = self.spaces[pos]
        self.spaces.pop(pos)
        if (piece.color == Color.WHITE):
            self.whiteAlive.pop(piece.id)
            self.whiteDead[piece.id] = piece
        else: #black
            self.blackAlive.pop(piece.id)
            self.blackDead[piece.id] = piece

    # move piece from starting point to ending point
    # if there is another piece occupying that space, remove (take) that piece
    # startPos and endPos are tuples representing (x, y) coordinates
    # if display is set to false, do not call changeTurns (use this for manipulating hypothetical boards)
    def movePiece (self, startPos, endPos, display = True):
        movingPiece = self.spaces[startPos]
        # check if there's a piece occupying the spot to be moved to
        # if so, take it
        if endPos in self.spaces:
            self.removePiece(endPos)
        self.spaces[endPos] = self.spaces[startPos]
        self.spaces.pop(startPos)

        # update info about moving piece as necessary
        movingPiece.has_moved = True
        movingPiece.pos = endPos

        if (movingPiece.type == PieceType.PAWN):
            # check if this was an en passant move
            multiplier:int
            if (movingPiece.color == Color.WHITE): multiplier = 1
            else: multiplier = -1
            capPos = (endPos[0], endPos[1]+multiplier)
            if (movingPiece.ep_pos == capPos):
                self.removePiece(capPos)
            
            # for pawns, check to see if neighboring pawns can en passant
            if (abs(startPos[1]-endPos[1]) == 2): # two square move
                leftPos = (endPos[0]-1, endPos[1])
                rightPos = (endPos[0]+1, endPos[1])
                if leftPos in self.spaces:
                    if self.spaces[leftPos].color != movingPiece.color:
                        self.spaces[leftPos].ep_pos = endPos
                        self.ep_clear_list.append(self.spaces[leftPos])
                if rightPos in self.spaces:
                    if self.spaces[rightPos].color != movingPiece.color:
                        self.spaces[rightPos].ep_pos = endPos
                        self.ep_clear_list.append(self.spaces[rightPos])
        
        # handle end of turn stuff
        if display: self.changeTurns()
    
    # set up the board in default configuration and start the game
    # optionally, pass an array of eight strings as "setup" for a custom setup
    # each string should be 16 characters long
    # a piece is represented by a two character sequence representing color and type
    # use W for white and B for black, X for blank space
    # use P for pawn, R for rook, N for knight, B for bishop, Q for queen, K for king, and X for blank space
    # optionally, set draw to false to prevent drawing the board
    def initialize (self, setup = [], draw = True):
        if setup == []:
            #pawns
            for x in range(1, 9):
                self.createPiece(PieceType.PAWN, Color.WHITE, x, 7)
                self.createPiece(PieceType.PAWN, Color.BLACK, x, 2)
            #rooks
            self.createPiece(PieceType.ROOK, Color.WHITE, 1, 8)
            self.createPiece(PieceType.ROOK, Color.WHITE, 8, 8)
            self.createPiece(PieceType.ROOK, Color.BLACK, 1, 1)
            self.createPiece(PieceType.ROOK, Color.BLACK, 8, 1)
            #knights
            self.createPiece(PieceType.KNIGHT, Color.WHITE, 2, 8)
            self.createPiece(PieceType.KNIGHT, Color.WHITE, 7, 8)
            self.createPiece(PieceType.KNIGHT, Color.BLACK, 2, 1)
            self.createPiece(PieceType.KNIGHT, Color.BLACK, 7, 1)
            #bishops
            self.createPiece(PieceType.BISHOP, Color.WHITE, 3, 8)
            self.createPiece(PieceType.BISHOP, Color.WHITE, 6, 8)
            self.createPiece(PieceType.BISHOP, Color.BLACK, 3, 1)
            self.createPiece(PieceType.BISHOP, Color.BLACK, 6, 1)
            #queens
            self.createPiece(PieceType.QUEEN, Color.WHITE, 4, 8)
            self.createPiece(PieceType.QUEEN, Color.BLACK, 4, 1)
            #kings
            self.createPiece(PieceType.KING, Color.WHITE, 5, 8)
            self.createPiece(PieceType.KING, Color.BLACK, 5, 1)
        else: #custom setup
            rowNum = 1
            for rowStr in setup:
                colNum = 1
                for j in range(0, 15, 2):
                    if j+2 > len(rowStr): break # if string is shorter than expected
                    colorStr = rowStr[j]
                    typeStr = rowStr[j+1]
                    color:Color
                    ptype:PieceType

                    if colorStr == "W": color = Color.WHITE
                    elif colorStr == "B": color = Color.BLACK
                    elif colorStr == "X": 
                        colNum += 1
                        continue
                    
                    if typeStr == "P": ptype = PieceType.PAWN
                    elif typeStr == "R": ptype = PieceType.ROOK
                    elif typeStr == "N": ptype = PieceType.KNIGHT
                    elif typeStr == "B": ptype = PieceType.BISHOP
                    elif typeStr == "Q": ptype = PieceType.QUEEN
                    elif typeStr == "K": ptype = PieceType.KING
                    elif typeStr == "X": 
                        colNum += 1
                        continue

                    self.createPiece(ptype, color, colNum, rowNum)
                    colNum += 1
                rowNum += 1

        if draw: self.drawBoard()

    def getKing (self, color):
        pieces = []
        if color == Color.WHITE: pieces = self.whiteAlive
        else: pieces = self.blackAlive
        for pc in pieces.values():
            if pc.type == PieceType.KING:
                return pc
    
    # return true if a piece of *color* in space pos could be taken by a piece of the opposing color
    # this is specifically for the king being in check, so things like en passant will be ignored
    def isThreatened (self, pos, color):
        x = pos[0]
        y = pos[1]
        # check for pawns
        multiplier:int
        if (color == Color.WHITE):
            multiplier = -1 # threats come from above
        else:
            multiplier = 1 # threats come from below

        nextPos = (x-1, y+multiplier)
        if nextPos in self.spaces:
            if (self.spaces[nextPos].color != color) & (self.spaces[nextPos].type == PieceType.PAWN):
                return True
        nextPos = (x+1, y+multiplier)
        if nextPos in self.spaces:
            if (self.spaces[nextPos].color != color) & (self.spaces[nextPos].type == PieceType.PAWN):
                return True

        # check horiz/vert for rooks/queens
        for nextX in range(x+1, self.max_x+1):
            nextPos = (nextX, y)
            if nextPos in self.spaces: #occupied
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.ROOK) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
        for nextX in range(x-1, -1, -1):
            nextPos = (nextX, y)
            if nextPos in self.spaces: #occupied
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.ROOK) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
        for nextY in range(y+1, self.max_y+1):
            nextPos = (x, nextY)
            if nextPos in self.spaces: #occupied
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.ROOK) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
        for nextY in range(y-1, -1, -1):
            nextPos = (x, nextY)
            if nextPos in self.spaces: #occupied
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.ROOK) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break

        # check diagonals for bishops/queens
        step = 1
        while (x+step <= self.max_x) & (y+step <= self.max_y):
            nextPos = (x+step, y+step)
            if nextPos in self.spaces:
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.BISHOP) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
            step += 1
        step = 1
        while (x+step <= self.max_x) & (y-step > 0):
            nextPos = (x+step, y-step)
            if nextPos in self.spaces:
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.BISHOP) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
            step += 1
        step = 1
        while (x-step > 0) & (y+step < self.max_y):
            nextPos = (x-step, y+step)
            if nextPos in self.spaces:
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.BISHOP) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
            step += 1
        step = 1
        while (x-step > 0) & (y-step > 0):
            nextPos = (x-step, y-step)
            if nextPos in self.spaces:
                if (self.spaces[nextPos].color != color) & ((self.spaces[nextPos].type == PieceType.BISHOP) | (self.spaces[nextPos].type == PieceType.QUEEN)):
                    return True
                break
            step += 1

        # check for knights
        potentialMoves = [(x+2, y-1), (x+2, y+1), (x-2, y-1), (x-2, y+1), (x-1, y+2), (x+1, y+2), (x-1, y-2), (x+1, y-2)]
        for move in potentialMoves:
            # check if space is occupied
            if move in self.spaces: #is occupied
                #check if occupied by friend or foe
                if (self.spaces[move].color != color) & (self.spaces[move].type == PieceType.KNIGHT):
                    return True

        # TODO: check for kings (maybe work in with pawns)

    # this function should ONLY be used for pieces of the player whose turn it is
    def getMoves (self, pos):
        x = pos[0]
        y = pos[1]
        piece = self.spaces[(x, y)]
        moves = []
        if (piece.type == PieceType.PAWN):
            # set multiplier
            multiplier:int
            if (piece.color == Color.WHITE):
                multiplier = -1 # can only move up
            else:
                multiplier = 1 # can only move down

            # check one space forward
            nextY = y + multiplier
            if (not (x, nextY) in self.spaces):
                moves.append((x, nextY))
                if (not piece.has_moved):
                    # test two spaces forward
                    nextY = y + 2*multiplier
                    if (not (x, nextY) in self.spaces):
                        moves.append((x, nextY))

            #check for capture
            nextY = y + multiplier
            if (x-1, nextY) in self.spaces:
                if self.spaces[(x-1, nextY)].color != piece.color:
                    moves.append((x-1, nextY))
            if (x+1, nextY) in self.spaces:
                if self.spaces[(x+1, nextY)].color != piece.color:
                    moves.append((x+1, nextY))
            
            #check for en passant
            if (piece.ep_pos != (-1, -1)):
                new_pos = (piece.ep_pos[0], piece.ep_pos[1]+multiplier)
                moves.append(new_pos)
        elif (piece.type == PieceType.ROOK):
            # check in all four cardinal directions
            for nextX in range(x+1, self.max_x+1):
                nextPos = (nextX, y)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            for nextX in range(x-1, 0, -1):
                nextPos = (nextX, y)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            for nextY in range(y+1, self.max_y+1):
                nextPos = (x, nextY)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            for nextY in range(y-1, 0, -1):
                nextPos = (x, nextY)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
        elif (piece.type == PieceType.KNIGHT):
            potentialMoves = [(x+2, y-1), (x+2, y+1), (x-2, y-1), (x-2, y+1), (x-1, y+2), (x+1, y+2), (x-1, y-2), (x+1, y-2)]
            for move in potentialMoves:
                # make sure move is inside board
                if (move[0] <= 0) | (move[0] > self.max_x) | (move[1] <= 0) | (move[1] > self.max_y):
                    continue
                # check if space is occupied
                if move in self.spaces: #is occupied
                    #check if occupied by friend or foe
                    if self.spaces[move].color != piece.color:
                        moves.append(move) #this will capture the piece
                else: #not occupied
                    moves.append(move)
        elif (piece.type == PieceType.BISHOP):
            #check all four diagonals
            step = 1
            while (x+step <= self.max_x) & (y+step <= self.max_y):
                nextPos = (x+step, y+step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
            step = 1
            while (x+step <= self.max_x) & (y-step > 0):
                nextPos = (x+step, y-step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
            step = 1
            while (x-step > 0) & (y+step < self.max_y):
                nextPos = (x-step, y+step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
            step = 1
            while (x-step > 0) & (y-step > 0):
                nextPos = (x-step, y-step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
        elif (piece.type == PieceType.QUEEN):
            #horizontals/verticals
            for nextX in range(x+1, self.max_x+1):
                nextPos = (nextX, y)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            for nextX in range(x-1, -1, -1):
                nextPos = (nextX, y)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            for nextY in range(y+1, self.max_y+1):
                nextPos = (x, nextY)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            for nextY in range(y-1, -1, -1):
                nextPos = (x, nextY)
                if nextPos in self.spaces: #occupied
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
            
            #diagonals
            step = 1
            while (x+step <= self.max_x) & (y+step <= self.max_y):
                nextPos = (x+step, y+step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
            step = 1
            while (x+step <= self.max_x) & (y-step > 0):
                nextPos = (x+step, y-step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
            step = 1
            while (x-step > 0) & (y+step < self.max_y):
                nextPos = (x-step, y+step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
            step = 1
            while (x-step > 0) & (y-step > 0):
                nextPos = (x-step, y-step)
                if nextPos in self.spaces:
                    if self.spaces[nextPos].color != piece.color: #enemy
                        moves.append(nextPos)
                    break
                moves.append(nextPos)
                step += 1
        elif (piece.type == PieceType.KING):
            potentialMoves = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
            for move in potentialMoves:
                # make sure move is inside board
                if (move[0] < 0) | (move[0] > self.max_x) | (move[1] < 0) | (move[1] > self.max_y):
                    continue
                # check if space is occupied by a friendly piece
                if move in self.spaces:
                    if self.spaces[move].color == piece.color:
                        continue
                # check if space is threatened
                # cannot move there if so, would put king in check
                if self.isThreatened(move, piece.color):
                    continue
                moves.append(move)
        
        # if currently in check, remove any move which doesn't take the player out of check
        if self.game_state == GameState.CHECK:
            movesToRemove = []
            for move in moves:
                newboard = copy.deepcopy(self)
                newboard.movePiece(pos, move)
                if newboard.isThreatened(newboard.getKing().pos):
                    movesToRemove.append(move)
            for move in movesToRemove:
                moves.remove(move)   

        return moves
    
    # get all moves for the current player
    def getAllMoves (self):
        moves = []
        pieces = []
        if self.curr_player == Color.WHITE: pieces = self.whiteAlive
        else: pieces = self.blackAlive
        for pc in pieces.values():
            for mv in self.getMoves(pc.pos):
                moves.append((pc.pos, mv))
        
        return moves

    # draw the board using tkinter
    def drawBoard (self):
        mv = self.getAllMoves()
        print(mv) #DEBUG

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
                if (light_square): bgColor = Board.LIGHT_SQUARE_COLOR
                else: bgColor = Board.DARK_SQUARE_COLOR
                if (self.selected_square == (a, b)): bgColor = Board.SELECTED_SQUARE_COLOR
                if (a, b) in squaresToHighlight:
                    bgColor = Board.NORMAL_MOVE_COLOR

                # create button
                button: tk.Button
                if (a, b) in self.spaces:
                    img = self.spaces[(a, b)].img
                    button = tk.Button(self.root, width=a, height=b, command=self.handleClick, text="", image=img)
                else:
                    button = tk.Button(self.root, width=a, height=b, command=self.handleClick, text="")
                
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
        #print ("Click!")
        # determine which button was clicked based on cursor position
        x = (self.root.winfo_pointerx() - self.root.winfo_rootx() - self.pos[0]) // 64 + 1
        y = (self.root.winfo_pointery() - self.root.winfo_rooty() - self.pos[1]) // 64 + 1
        clickPos = (x, y)
        
        if (self.selected_square == (-1, -1)): # no square selected
            if (clickPos in self.spaces):
                if (self.curr_player == self.spaces[clickPos].color): #space occupied by friendly piece
                    self.selected_square = clickPos
                    self.drawBoard() #redraw board to show changes
        else: #square selected
            if (self.selected_square in self.spaces):
                moves = self.getMoves(self.selected_square)
                if clickPos in moves:
                    self.movePiece(self.selected_square, clickPos)
                    self.selected_square = (-1, -1)
                    self.drawBoard()
                    return
            prevPos = self.selected_square
            self.selected_square = (-1, -1) #deselect
            if clickPos in self.spaces:
                if (self.spaces[clickPos].color == self.curr_player) & (clickPos != prevPos): #if clicking on a different friendly piece, select
                    self.selected_square = clickPos
            self.drawBoard()

    # return true if there is a stalemate on current player's turn
    def checkForStalemate (self):
        pieces = []
        if self.curr_player == Color.WHITE: pieces = self.whiteAlive
        else: pieces = self.blackAlive
        for pc in pieces.values():
            moves = self.getMoves(pc.pos)
            if len(moves) > 0: return False
        return True

    
    # take all end-of-turn actions, switch players, and take all beginning of turn actions for the next player
    # return end of game scenarios if necessary
    def changeTurns (self):
        # end of turn actions
        pieceToClear = ()
        for piece in self.ep_clear_list:
            # only clear en passant counters for pieces of the current color
            if (piece.color == self.curr_player):
                piece.ep_pos = (-1, -1)
                pieceToClear = piece
        if pieceToClear != ():
            self.ep_clear_list.remove(pieceToClear)
        self.check = False
        
        # change sides
        piecesAlive = []
        if (self.curr_player == Color.WHITE):
            self.curr_player = Color.BLACK
        else:
            self.curr_player = Color.WHITE

        # beginning of turn actions
        # check for check/checkmate
        king = self.getKing(self.curr_player)
        if self.isThreatened(king.pos, self.curr_player):
            self.check = True
            moves = self.getMoves(king.pos)
            if len(moves) == 0:
                self.game_state = GameState.CHECKMATE
                self.canvas.destroy()
                
        else: # not in check
            # check for stalemate
            if (self.checkForStalemate()):
                self.game_state = GameState.STALEMATE
                self.canvas.destroy()