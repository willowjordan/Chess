from enum import Enum

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
    pass