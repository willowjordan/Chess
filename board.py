#from old_piece import *
from enum import Enum
import tkinter as tk
import copy
from os import walk

'''
NOTES:
    - Starting board position is (1, 1) in the top left, going to (8, 8) in the bottom right
    - Every piece is represented by two characters, color and type
        - W = White, B = Black, X = Empty
        - P = Pawn, R = Rook, N = Knight, B = Bishop, Q = Queen, K = King, X = Empty
'''
class GameState(Enum):
    NORMAL = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3

# might get rid of this later if it proves to not be useful
class Piece:
    WHITE = "W"
    BLACK = "B"
    NOCOLOR = NOTYPE = "X"

    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"
    EMPTY = "XX"

    WHITEPAWN = "WP"
    WHITEROOK = "WR"
    WHITEKNIGHT = "WN"
    WHITEBISHOP = "WB"
    WHITEQUEEN = "WQ"
    WHITEKING = "WK"

    BLACKPAWN = "BP"
    BLACKROOK = "BR"
    BLACKKNIGHT = "BN"
    BLACKBISHOP = "BB"
    BLACKQUEEN = "BQ"
    BLACKKING = "BK"

class Board:
    # setup will replace the default board configuration
    # other (MUST BE A BOARD) will create a copy of that board
    def __init__ (self, setup:list = [], other = None):
        if other is not None:
            self.spaces = copy.deepcopy(other.spaces)
            self.curr_player = other.curr_player
            self.ep_clear_list = other.ep_clear_list
            self.game_state = other.game_state
        else:
            # 2D array of characters (basically) where two characters represent the piece color and type (e.g. WN = white knight)
            if setup == []:
                self.spaces = [
                    "BRBNBBBQBKBBBNBR",
                    "BPBPBPBPBPBPBPBP",
                    "XXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXX",
                    "WPWPWPWPWPWPWPWP",
                    "WRWNWBWKWQWBWNWR"
                ]
            else: self.spaces = setup
            self.curr_player = "W" # whose turn it is
            self.ep_clear_list = [] # list of en passant values to reset at the end of the turn
            self.game_state = GameState.NORMAL
        
    @staticmethod
    def posToArrayCoords(pos):
        rowNum = pos[1]-1
        colNum = (pos[0]-1)*2
        return (rowNum, colNum)

    @staticmethod
    def arrayCoordsToPos(coords):
        x = coords[1]+1
        y = (coords[0]/2)+1
        return (x, y)
    
    # set the space at pos to piece_string
    # this replaces createPiece and removePiece
    def setSpace (self, pos, piece_string):
        try:
            assert len(piece_string) == 2
        except AssertionError:
            print("Error in createPiece(): piece_string must be exactly two characters!")
            exit(1)
        # TODO: maybe add error checking to make sure pieces aren't replaced?
        arrCoords = Board.posToArrayCoords(pos)
        old = self.spaces[arrCoords[0]]
        new = old[:arrCoords[1]] + piece_string + old[arrCoords[1]+2:]
        self.spaces[arrCoords[0]] = new
    
    # get the piece string at pos
    def getSpace (self, pos):
        if (pos[0] <= 0) | (pos[0] > 8) | (pos[1] <= 0) | (pos[1] > 8): # out of range
            return "XX"
        arrCoords = Board.posToArrayCoords(pos)
        return self.spaces[arrCoords[0]][arrCoords[1]:arrCoords[1]+2]
    
    # move piece from starting point to ending point
    # if there is another piece occupying that space, remove (take) that piece
    # startPos and endPos are tuples representing (x, y) coordinates
    def movePiece (self, startPos, endPos):
        self.setSpace(endPos, self.getSpace(startPos))
        self.setSpace(startPos, "XX")
    
    def promotePiece (self, pos, type):
        self.setSpace(pos, self.getSpace()[0]+type)
    
    # return position of king
    def getKing (self, color):
        king = color + "K"
        for x in range (1, 9, 1):
            for y in range (1, 9, 1):
                if self.getSpace((x, y)) == king:
                    return (x, y)
        print("ERROR: " + str(color) + " king not found!")
        exit(1)
    
    def getAllPieces (self, color):
        pieces = []
        for x in range (1, 9, 1):
            for y in range (1, 9, 1):
                if self.getSpace((x, y))[0] == color:
                    pieces.append(x, y)
        return pieces

    # return true if a piece of *color* in space pos could be taken by a piece of the opposing color
    # this is specifically for the king being in check, so things like en passant will be ignored    
    def isThreatened (self, pos, color):
        x = pos[0]
        y = pos[1]
        if color == "W": enemycolor = "B"
        else: enemycolor = "W"
        enemypawn = enemycolor + "P"
        enemyrook = enemycolor + "R"
        enemyknight = enemycolor + "N"
        enemybishop = enemycolor + "B"
        enemyqueen = enemycolor + "Q"
        enemyking = enemycolor + "K"

        # check for pawns
        multiplier:int
        if (color == "W"):
            multiplier = -1 # threats come from above
        else:
            multiplier = 1 # threats come from below
        nextPos = (x-1, y+multiplier)
        if self.getSpace(nextPos) == enemypawn:
            return True
        nextPos = (x+1, y+multiplier)
        if self.getSpace(nextPos) == enemypawn:
            return True
        
        #TODO: check for en passant

        # check horiz/vert for rooks/queens
        for nextX in range(x+1, 9):
            nextPos = (nextX, y)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemyrook) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
        for nextX in range(x-1, -1, -1):
            nextPos = (nextX, y)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemyrook) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
        for nextY in range(y+1, 9):
            nextPos = (x, nextY)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemyrook) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
        for nextY in range(y-1, -1, -1):
            nextPos = (x, nextY)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemyrook) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
        
        # check for knights
        potentialMoves = [(x+2, y-1), (x+2, y+1), (x-2, y-1), (x-2, y+1), (x-1, y+2), (x+1, y+2), (x-1, y-2), (x+1, y-2)]
        for move in potentialMoves:
            if self.getSpace(move) == enemyknight:
                return True
        
        # check diagonals for bishops/queens
        step = 1
        while (x+step <= 8) & (y+step <= 8):
            nextPos = (x+step, y+step)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemybishop) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
            step += 1
        step = 1
        while (x+step <= 8) & (y-step > 0):
            nextPos = (x+step, y-step)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemybishop) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
            step += 1
        step = 1
        while (x-step > 0) & (y+step < 8):
            nextPos = (x-step, y+step)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemybishop) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
            step += 1
        step = 1
        while (x-step > 0) & (y-step > 0):
            nextPos = (x-step, y-step)
            if self.getSpace(nextPos) != "XX": #occupied
                if (self.getSpace(nextPos) == enemybishop) | (self.getSpace(nextPos) == enemyqueen):
                    return True
                break
            step += 1
        
        # check for kings
        potentialMoves = [(x+1, y), (x+1, y+1), (x+1, y-1), (x, y+1), (x, y-1), (x-1, y), (x-1, y+1), (x-1, y-1)]
        for move in potentialMoves:
            if self.getSpace(move) == enemyking:
                return True
        
        return False
    
    # return a list of positions that the piece at pos can move to
    def getMoves (self, pos):
        piece = self.getSpace(pos)
        moves = []
        x = pos[0]
        y = pos[1]
        if piece[0] == "W":
            enemyclr = "B"
            multiplier = -1 # pawns can only move up
            orig_row = 7 # row pawns start on
        else: 
            enemyclr = "W"
            multiplier = 1 # pawns can only move down
            orig_row = 2 # row pawns start on

        if piece == "XX":
            return moves
        elif piece[1] == "P":
            # check one space forward
            nextY = y + multiplier
            if self.getSpace((x, nextY)) == "XX":
                moves.append((x, nextY))
                if y == orig_row:
                    # test two spaces forward
                    nextY = y + 2*multiplier
                    if self.getSpace((x, nextY)) == "XX":
                        moves.append((x, nextY))
            
            # check for capture
            nextY = y + multiplier
            if self.getSpace((x-1, nextY)) != "XX":
                if self.getSpace((x-1, nextY))[0] == enemyclr:
                    moves.append((x-1, nextY))
            if self.getSpace((x+1, nextY)) != "XX":
                if self.getSpace((x+1, nextY))[0] == enemyclr:
                    moves.append((x+1, nextY))
            
            # TODO:check for en passant
        elif piece[1] == "R":
            moves = self.getHorizMoves(pos)
        elif piece[1] == "N":
            potentialMoves = [(x+2, y-1), (x+2, y+1), (x-2, y-1), (x-2, y+1), (x-1, y+2), (x+1, y+2), (x-1, y-2), (x+1, y-2)]
            for move in potentialMoves:
                # make sure move is inside board
                if (move[0] <= 0) | (move[0] > 8) | (move[1] <= 0) | (move[1] > 8):
                    continue
                # space must either be empty or occupied by enemy piece
                if (self.getSpace(move) == "XX") | (self.getSpace(move)[0] == enemyclr):
                    moves.append(move)
        elif piece[1] == "B":
            moves = self.getDiagMoves(pos)
        elif piece[1] == "Q":
            moves = self.getHorizMoves(pos)+self.getDiagMoves(pos)
        elif piece[1] == "K":
            potentialMoves = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
            for move in potentialMoves:
                # make sure move is inside board
                if (move[0] <= 0) | (move[0] > 8) | (move[1] <= 0) | (move[1] > 8):
                    continue
                # space must either be empty or occupied by enemy piece
                if (self.getSpace(move) == "XX") | (self.getSpace(move)[0] == enemyclr):
                    moves.append(move)
        
        # TODO: remove any moves that would put the king in check
        movesToRemove = []
        for move in moves:
            newboard = Board(other=self)
            newboard.movePiece(pos, move)
            if newboard.isThreatened(newboard.getKing(newboard.curr_player), newboard.curr_player):
                movesToRemove.append(move)
        for move in movesToRemove:
            moves.remove(move)

        return moves
    
    # helper function for getMove
    def getHorizMoves (self, pos):
        moves = []
        x = pos[0]
        y = pos[1]
        if self.getSpace(pos)[0] == "W": enemyclr = "B"
        else: enemyclr = "W"

        # check in all four cardinal directions
        for nextX in range(x+1, 9):
            nextPos = (nextX, y)
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
        for nextX in range(x-1, 0, -1):
            nextPos = (nextX, y)
            if nextPos in self.spaces: #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
        for nextY in range(y+1, 9):
            nextPos = (x, nextY)
            if nextPos in self.spaces: #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
        for nextY in range(y-1, 0, -1):
            nextPos = (x, nextY)
            if nextPos in self.spaces: #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
        
        return moves
    
    # helper function for getMove
    def getDiagMoves (self, pos):
        moves = []
        x = pos[0]
        y = pos[1]
        if self.getSpace(pos)[0] == "W": enemyclr = "B"
        else: enemyclr = "W"

        step = 1
        while (x+step <= 8) & (y+step <= 8):
            nextPos = (x+step, y+step)
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
            step += 1
        step = 1
        while (x+step <= 8) & (y-step > 0):
            nextPos = (x+step, y-step)
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
            step += 1
        step = 1
        while (x-step > 0) & (y+step < 8):
            nextPos = (x-step, y+step)
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
            step += 1
        step = 1
        while (x-step > 0) & (y-step > 0):
            nextPos = (x-step, y-step)
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
            step += 1
    
        return moves

    # get all moves for the current player
    def getAllMoves (self):
        pieces = self.getAllPieces(self.curr_player)
        moves = []
        for pc in pieces:
            moves += self.getMoves(pc)
        return moves

    # check for check, checkmate, and stalemate
    # set the gamestate var and return it too
    def updateGameState (self):
        # check for check
        if self.isThreatened(self.getKing(self.curr_player), self.curr_player):
            if self.getAllMoves() == []:
                self.game_state = GameState.CHECKMATE
            else:
                self.game_state = GameState.CHECK
        elif self.getAllMoves() == []:
            self.game_state = GameState.STALEMATE
        else:
            self.game_state = GameState.NORMAL
        return self.game_state

# a special board WITH GRAPHICAL REPRESENTATION that will be used as the main board for the game
class MainBoard(Board):
    pass