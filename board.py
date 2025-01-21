#from old_piece import *
from enum import Enum
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

class Board:
    # return the opposite color of the one given
    @staticmethod
    def oppColor(color):
        if color == "W": return "B"
        else: return "W"

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
    
    # setup will replace the default board configuration
    # other (MUST BE A BOARD) will create a copy of that board
    def __init__ (self, setup:list = [], other = None):
        if other is not None:
            self.spaces = copy.deepcopy(other.spaces)
            self.curr_player = other.curr_player
            self.ep_moves = copy.deepcopy(other.ep_moves)
            self.castling_options = copy.deepcopy(other.castling_options)
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
                    "WRWNWBWQWKWBWNWR"
                ]
            else: 
                #TODO: add validation to make sure board is correctly generated
                self.spaces = setup
            self.curr_player = "W" # whose turn it is
            self.ep_moves:dict = {} # dict of possible en passant moves (key is starting position tuple, value is ending position tuple)
            # list containing available options for castling
            # WL = white left, BR = black right, etc
            # will be updated as pieces move
            self.castling_options = ["WL", "WR", "BL", "BR"]
            self.game_state = GameState.NORMAL

    # set the space at pos to piece_string
    # this replaces createPiece and removePiece
    def setSpace (self, pos, piece_string):
        try:
            assert len(piece_string) == 2
        except AssertionError:
            print("Error in setSpace(): piece_string must be exactly two characters!")
            exit(1)
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
        pc = self.getSpace(startPos)
        self.setSpace(endPos, pc)
        self.setSpace(startPos, "XX")

        if pc[1] == "P": # moving piece is a pawn
            # check for en passant move
            if startPos in self.ep_moves:
                if self.ep_moves[startPos] == endPos:
                    self.setSpace((endPos[0], startPos[1]), "XX") # delete piece that was captured
            # check if piece's movement creates opportunity for en passant
            if abs(startPos[1] - endPos[1]) == 2: # moved two squares
                enemypawn = Board.oppColor(pc[0]) + "P"
                midpoint = (startPos[1] + endPos[1]) // 2
                epPos = (endPos[0], midpoint)
                leftPos = (endPos[0]-1, endPos[1])
                if self.getSpace(leftPos) == enemypawn:
                    self.ep_moves[leftPos] = epPos
                rightPos = (endPos[0]+1, endPos[1])
                if self.getSpace(rightPos) == enemypawn:
                    self.ep_moves[rightPos] = epPos
            # check for promotion
            if self.curr_player == "W": y = 1
            else: y = 8
            if endPos[1] == y:
                self.promotePiece(endPos)
                return True # return true in order to stall the program until a piece is selected
        # castling
        if (self.castling_options != []):
            if self.curr_player == "W": y = 8
            else: y = 1
            lstring = self.curr_player + "L"
            rstring = self.curr_player + "R"
            rook = rstring
            if (pc[1] == "R"):
                if (startPos == (1, y)) & (lstring in self.castling_options):
                    self.castling_options.remove(lstring)
                if (startPos == (8, y)) & (rstring in self.castling_options):
                    self.castling_options.remove(rstring)
            if (pc[1] == "K"):
                # check if current move is a castling move
                if startPos == (5, y):
                    # left castle
                    if (endPos == (3, y)) & (lstring in self.castling_options):
                        self.setSpace((4, y), rook)
                        self.setSpace((1, y), "XX")
                    # right castle
                    if (endPos == (7, y)) & (rstring in self.castling_options):
                        self.setSpace((6, y), rook)
                        self.setSpace((8, y), "XX")

                # remove castling options since king has now moved
                if lstring in self.castling_options:
                    self.castling_options.remove(lstring)
                if rstring in self.castling_options:
                    self.castling_options.remove(rstring)

    # since this is not the main board and we cannot take player input, promote to a queen every time
    def promotePiece (self, pos):
        self.setSpace(pos, (self.getSpace(pos)[0]+"Q"))
    
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
                    pieces.append((x, y))
        return pieces

    # return true if a piece of *color* in space pos could be taken by a piece of the opposing color
    # this is specifically for the king being in check, so things like en passant will be ignored    
    def isThreatened (self, pos, color):
        x = pos[0]
        y = pos[1]
        enemycolor = Board.oppColor(color)
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
        
        # TODO: check for en passant
        for pair in self.ep_moves.items():
            if pair[1] == pos: # current pos is the endPos of an en passant move
                if self.getSpace(pair[0]) == enemypawn:
                    return True


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
        if piece == "XX":
            return moves
        
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

        if piece[1] == "P":
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
            
            # check for en passant
            if pos in self.ep_moves:
                moves.append(self.ep_moves[pos])
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
            # add castling options
            if self.curr_player == "W": y = 8
            else: y = 1
            if (self.curr_player + "L") in self.castling_options:
                # make sure spaces between are clear
                if (self.getSpace((2, y)) == "XX") & (self.getSpace((3, y)) == "XX") & (self.getSpace((4, y)) == "XX"):
                    moves.append((3, y))
            if (self.curr_player + "R") in self.castling_options:
                # make sure spaces between are clear
                if (self.getSpace((6, y)) == "XX") & (self.getSpace((7, y)) == "XX"):
                    moves.append((7, y))
        
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
        enemyclr = Board.oppColor(self.getSpace(pos)[0])

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
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
        for nextY in range(y+1, 9):
            nextPos = (x, nextY)
            if self.getSpace(nextPos) != "XX": #occupied
                if self.getSpace(nextPos)[0] == enemyclr:
                    moves.append(nextPos)
                break
            moves.append(nextPos)
        for nextY in range(y-1, 0, -1):
            nextPos = (x, nextY)
            if self.getSpace(nextPos) != "XX": #occupied
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
        enemyclr = Board.oppColor(self.getSpace(pos)[0])

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