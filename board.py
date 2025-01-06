from piece import *
import tkinter as tk

'''
NOTES:
    - Starting board position is (1, 1) in the top left, going to (8, 8) in the bottom right
'''
class Board:
    LIGHT_SQUARE_COLOR = "#e2d2a1"
    DARK_SQUARE_COLOR = "#ae9f70"
    SELECTED_SQUARE_COLOR = "#6ce565"
    NORMAL_MOVE_COLOR = "#65a2e5"
    CAPTURE_MOVE_COLOR = "#e56565"
    SPECIAL_MOVE_COLOR = "#b465e5"

    # pos = (x, y) coordinates for the top left corner of the board to be drawn at
    def __init__ (self, pos):
        self.spaces:dict = {} # this is the board itself
        self.whiteAlive:dict = {}
        self.whiteDead:dict = {}
        self.blackAlive:dict = {}
        self.blackDead:dict = {}
        self.max_x = 8
        self.max_y = 8
        self.piecesCreated = 0
        self.pos = pos
        self.buttons = []
        self.curr_player = Color.WHITE # whose turn it is
        self.selected_square = (-1, -1) # the square of the piece currently selected by the player, (-1, -1) if no piece selected

    # create a new piece and insert it onto the board
    def createPiece (self, type, color, x, y):
        piece = Piece(self.piecesCreated+1, type, color)
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
    def movePiece (self, startPos, endPos):
        # check if there's a piece occupying the spot to be moved to
        # if so, take it
        if endPos in self.spaces:
            self.removePiece(endPos)
        self.spaces[endPos] = self.spaces[startPos]
        self.spaces.pop(startPos)

    # for better clarity
    def getPiece (self, x, y):
        return self.spaces[(x, y)]
    
    # return true if a piece of *color* in space x, y could be taken by a piece of the opposing color
    # this is specifically for the king being in check, so things like en passant will be ignored
    def isThreatened (self, x, y, color):
        # check for pawns
        multiplier:int
        if (color == Color.WHITE):
            multiplier = -1 # threats come from above
        else:
            multiplier = 1 # threats come from below

        nextPos = (x-1, y+multiplier)
        if (nextPos in self.spaces & self.spaces[nextPos].color != color & self.spaces[nextPos].type == PieceType.PAWN):
            return True
        nextPos = (x+1, y+multiplier)
        if (nextPos in self.spaces & self.spaces[nextPos].color != color & self.spaces[nextPos].type == PieceType.PAWN):
            return True

        # check horiz/vert for rooks/queens
        for nextX in range(x+1, self.max_x+1):
            nextPos = (nextX, y)
            if nextPos in self.spaces: #occupied
                if self.spaces[nextPos].color != color & (self.spaces[nextPos].type == PieceType.ROOK | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
        for nextX in range(x-1, -1, -1):
            nextPos = (nextX, y)
            if nextPos in self.spaces: #occupied
                if self.spaces[nextPos].color != color & (self.spaces[nextPos].type == PieceType.ROOK | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
        for nextY in range(y+1, self.max_y+1):
            nextPos = (x, nextY)
            if nextPos in self.spaces: #occupied
                if self.spaces[nextPos].color != color & (self.spaces[nextPos].type == PieceType.ROOK | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
        for nextY in range(y-1, -1, -1):
            nextPos = (x, nextY)
            if nextPos in self.spaces: #occupied
                if self.spaces[nextPos].color != color & (self.spaces[nextPos].type == PieceType.ROOK | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break

        # check diagonals for bishops/queens
        step = 1
        while (x+step < self.max_x & y+step < self.max_y):
            newPos = (x+step, y+step)
            if newPos in self.spaces:
                if self.spaces[newPos].color != color & (self.spaces[nextPos].type == PieceType.BISHOP | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
            step += 1
        step = 1
        while (x+step < self.max_x & y-step >= 0):
            newPos = (x+step, y-step)
            if newPos in self.spaces:
                if self.spaces[newPos].color != color & (self.spaces[nextPos].type == PieceType.BISHOP | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
            step += 1
        step = 1
        while (x-step >= 0 & y+step < self.max_y):
            newPos = (x-step, y+step)
            if newPos in self.spaces:
                if self.spaces[newPos].color != color & (self.spaces[nextPos].type == PieceType.BISHOP | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
            step += 1
        step = 1
        while (x-step >= 0 & y-step >= 0):
            newPos = (x-step, y-step)
            if newPos in self.spaces:
                if self.spaces[newPos].color != color & (self.spaces[nextPos].type == PieceType.BISHOP | self.spaces[nextPos].type == PieceType.QUEEN):
                    return True
                break
            step += 1

        # check for knights
        potentialMoves = [(x+2, y-1), (x+2, y+1), (x-2, y-1), (x-2, y+1), (x-1, y+2), (x+1, y+2), (x-1, y-2), (x+1, y-2)]
        for move in potentialMoves:
            # check if space is occupied
            if move in self.spaces: #is occupied
                #check if occupied by friend or foe
                if self.spaces[move].color != color & self.spaces[move].type == PieceType.KNIGHT:
                    return True

        # TODO: check for kings (maybe work in with pawns)


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

            #TODO: check for capture
            
            #TODO: check for en passant
        elif (piece.type == PieceType.ROOK):
            # check in all four cardinal directions
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
        elif (piece.type == PieceType.KNIGHT):
            potentialMoves = [(x+2, y-1), (x+2, y+1), (x-2, y-1), (x-2, y+1), (x-1, y+2), (x+1, y+2), (x-1, y-2), (x+1, y-2)]
            for move in potentialMoves:
                # make sure move is inside board
                if (x <= 0 | x > self.max_x | y <= 0 | y > self.max_y):
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
            while (x+step < self.max_x & y+step < self.max_y):
                newPos = (x+step, y+step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
            step = 1
            while (x+step < self.max_x & y-step >= 0):
                newPos = (x+step, y-step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
            step = 1
            while (x-step >= 0 & y+step < self.max_y):
                newPos = (x-step, y+step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
            step = 1
            while (x-step >= 0 & y-step >= 0):
                newPos = (x-step, y-step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
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
            while (x+step < self.max_x & y+step < self.max_y):
                newPos = (x+step, y+step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
            step = 1
            while (x+step < self.max_x & y-step >= 0):
                newPos = (x+step, y-step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
            step = 1
            while (x-step >= 0 & y+step < self.max_y):
                newPos = (x-step, y+step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
            step = 1
            while (x-step >= 0 & y-step >= 0):
                newPos = (x-step, y-step)
                if newPos in self.spaces:
                    if self.spaces[newPos].color != piece.color: #enemy
                        moves.append(newPos)
                    break
                moves.append(newPos)
                step += 1
        elif (piece.type == PieceType.KING):
            potentialMoves = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
            for move in potentialMoves:
                # make sure move is inside board
                if (x <= 0 | x > self.max_x | y <= 0 | y > self.max_y):
                    continue
                # check if space is threatened
                # cannot move there if so, would put king in check
                if (self.isThreatened(x, y, piece.color)):
                    continue
                # check if space is occupied
                if move in self.spaces: #is occupied
                    #check if occupied by friend or foe
                    if self.spaces[move].color != piece.color:
                        moves.append(move) #this will capture the piece
                else: #not occupied
                    moves.append(move)
        
        return moves

    # set up the board in default configuration   
    def initialize (self):
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

    # draw the board using tkinter
    # TODO: change colors
    def drawBoard (self, root, canvas):
        # create a button for every square on the board
        light_square = True
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
                if (self.selected_square != (-1, -1)):
                    squaresToHighlight = self.getMoves(self.selected_square)
                    if (a, b) in squaresToHighlight:
                        bgColor = Board.NORMAL_MOVE_COLOR

                # create button
                button: tk.Button
                if (a, b) in self.spaces:
                    img = self.spaces[(a, b)].img
                    button = tk.Button(root, width=a, height=b, command= lambda: self.handleClick(root, canvas), text="", image=img)
                else:
                    button = tk.Button(root, width=a, height=b, command= lambda: self.handleClick(root, canvas), text="")
                
                # place button
                button.configure(background=bgColor)
                button_window = canvas.create_window(x, y, width=64, height=64, anchor=tk.NW, window=button)

                # flip square color
                light_square = not light_square
            # flip square color
            light_square = not light_square

        # draw grid lines

        
    
    # handle the square at (x, y) being clicked
    # for spaces with friendly pieces, select that piece and show its moves
    # click again to deselect, or click one of those spaces to make the move
    def handleClick (self, root, canvas):
        # determine which button was clicked based on cursor position
        x = (root.winfo_pointerx() - root.winfo_rootx() - self.pos[0]) // 64 + 1
        y = (root.winfo_pointery() - root.winfo_rooty() - self.pos[1]) // 64 + 1
        clickPos = (x, y)
        
        if (self.selected_square == (-1, -1)): # no square selected
            if (clickPos in self.spaces):
                if (self.curr_player == self.spaces[clickPos].color): #space occupied by friendly piece
                    self.selected_square = clickPos
                    self.drawBoard(root, canvas) #redraw board to show changes
        else: #square selected
            if (self.selected_square in self.spaces):
                moves = self.getMoves(self.selected_square)
                if clickPos in moves:
                    self.movePiece(self.selected_square, clickPos)
            self.selected_square = (-1, -1) #deselect
            self.drawBoard(root, canvas)
            