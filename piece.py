from enum import Enum
from PIL import ImageTk, Image
import tkinter as tk

class Color(Enum):
    UNDEFINED = 0
    WHITE = 1
    BLACK = 2

class PieceType(Enum):
    UNDEFINED = 0
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

class Piece:
    def __init__(self, id, type, color):
        self.id = id
        self.type = type
        self.color = color
        self.has_moved = False # this will be used for en passant, double pawn moves, and castling
        self.ep_pos = (-1, -1) # if the piece is a pawn and is able to en passant, it can do so to the piece at this location. otherwise, this var will be (-1, -1)
        
        # create image for piece (this will hopefully avoid garbage collection problems)
        color_string = str(self.color)[6:].lower()
        type_string = str(self.type)[10:].lower()
        path = "./sprites/" + color_string + "_" + type_string + ".png"
        self.img = tk.PhotoImage(file=path).zoom(2, 2)

    def __str__(self):
        return "Piece[id=" + str(self.id) + ", color=" + str(self.color) + ", type=" + str(self.type) + "]"

    '''# draw piece according to provided size at (x, y) on canvas
    def draw(self, canvas, x, y, size):
        color_string = str(self.color)[6:].lower()
        type_string = str(self.type)[10:].lower()
        path = "./sprites/" + color_string + "_" + type_string + ".png"
        img = tk.PhotoImage(file=path)
        canvas.create_image(0, 0, image = img, anchor = tk.NW)

    # get an image of piece of size (width, height) in pixels
    def getImage(self, width, height):
        color_string = str(self.color)[6:].lower()
        type_string = str(self.type)[10:].lower()
        path = "./sprites/" + color_string + "_" + type_string + ".png"
        img = tk.PhotoImage(file=path)
        dW = width / img.width()
        dH = height / img.height()
        return img.zoom(dW, dH)'''
        
'''
class Piece:
    # returns true if a piece in the spot (x, y) could be taken by an opposing piece
    @staticmethod
    def isSpotThreatened(x, y, board):
        pass

    # vars
    x = -1
    y = -1
    color = Color.UNDEFINED

    # methods
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    # returns an array of all possible moves 
    def getMoves(self, board):
        print ("ERROR: Cannot call getMoves() on an undefined piece")
    
    def move (self, x, y, board):
        self.x = x
        self.y = y

# piece subclasses
class Pawn(Piece):
    canEnPassant = False # this will be set to true by a neighboring pawn
    enPassantPos = (-1, -1)
    hasMoved = False # for en passant testing

    def getMoves(self, board):
        moves = []
        multiplier:int
        if (self.color == Color.WHITE):
            multiplier = 1
        else:
            multiplier = -1

        # test one space forward
        nextY = self.y + multiplier
        if (board.spaces[Board.getIndex(self.x, nextY)] == Board.EMPTY_SPACE):
            moves.append((self.x, nextY))
            if (not self.hasMoved):
                # test two spaces forward
                nextY = self.y + 2*multiplier
                if (board.spaces[Board.getIndex(self.x, nextY)] == Board.EMPTY_SPACE):
                    moves.append((self.x, nextY))

        # test for capture
        if (board.spaces[Board.getIndex(self.x - 1, nextY)] != Board.EMPTY_SPACE):
            moves.append((self.x - 1, nextY))
        if (board.spaces[Board.getIndex(self.x + 1, nextY)] != Board.EMPTY_SPACE):
            moves.append((self.x + 1, nextY))
        if (self.canEnPassant):
            moves.append(self.enPassantPos)
    
    def move(self, x, y, board):
        prevY = self.y
        Piece.move(self, x, y, board)
        if (not self.hasMoved):
            self.hasMoved = True
            if (abs(y - prevY) == 2): #pawn moved two spaces
                #check neighbors for pawns (en passant)
                n1 = board.getPiece(x-1, y)
                n2 = board.getPiece(x-1, y)
                if (type(n1) == Pawn & n1.color != self.color):
                    n1.canEnPassant = True
                    n1.enPassantPos = (x, y)
                if (type(n2) == Pawn & n2.color != self.color):
                    n2.canEnPassant = True
                    n2.enPassantPos = (x, y)
                #TODO: Find a way to remove en passant ability after one turn

class Rook(Piece):
    def getMoves(self, board):
        #check along row and column in both directions until there's a piece in the way or we reach edge of board
        for x in range(self.x+1, board.max_x):
            pass

class Knight(Piece):
    def getMoves(self, board):
        pass

class Bishop(Piece):
    def getMoves(self, board):
        pass

class Queen(Piece):
    def getMoves(self, board):
        pass

class King(Piece):
    def getMoves(self, board):
        pass
'''