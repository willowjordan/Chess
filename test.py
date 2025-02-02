# test script for the Board class
from board import *

import tkinter as tk
import time

'''def compareLists(t, s):
    t = list(t)   # make a mutable copy
    try:
        for elem in s:
            t.remove(elem)
    except ValueError:
        return False
    return True'''

# inputs is a tuple
# works for primitives and iterables
# order ONLY matters for lists and tuples if you specify
# note: order will still matter for lists/tuples inside of other containers/classes *no matter what*
def assertFunc(func, inputs, output, orderMatters = False, unpack = True):
    if (unpack):
        realoutput = func(*inputs)
    else:
        realoutput = func(inputs)
    try:
        assert type(realoutput) == type(output)
        if ((type(output) == list) | (type(output) == tuple)) & (not orderMatters):
            assert set(realoutput) == set(output)
        else:
            assert realoutput == output
    except AssertionError:
        failStr = "Assertion FAILED: " + func.__name__ + "(" + str(inputs) + ")" + " == " + str(output)
        if (orderMatters):
            failStr += " *ORDER MATTERS*"
        print (failStr)
        print ("Real output was: " + str(realoutput))
        return
    passStr = "Assertion passed: " + func.__name__ + "(" + str(inputs) + ")" + " == " + str(output)
    if (orderMatters):
        passStr += " *ORDER MATTERS*"
    print (passStr)

# posToArrayCoords
'''assertFunc(Board.posToArrayCoords, (1, 1), (0, 0), unpack=False)
assertFunc(Board.posToArrayCoords, (2, 1), (0, 2), unpack=False)
assertFunc(Board.posToArrayCoords, (1, 2), (1, 0), unpack=False)
assertFunc(Board.posToArrayCoords, (8, 8), (7, 14), unpack=False)'''

# getKing and getKing_slow
'''testboard = Board()
testboard.initialize()

start = time.time()
testboard.getKing("W")
end = time.time()
print("getKing took " + str(end-start) + " ms")

start = time.time()
testboard.getKing_slow("W")
end = time.time()
print("getKing_slow took " + str(end-start) + " ms")'''

# testing assertFunc
'''def foo(input):
    return input+1

def foo_list(input):
    output = []
    for i in range(input, 0, -1):
        output.append(i)
    return output

def foo_tuple(input):
    output = []
    for i in range(input, 0, -1):
        output.append(i)
    return tuple(output)

def foo_set(input):
    output = []
    for i in range(input, 0, -1):
        output.append(i)
    return set(output)

def foo_dict(input):
    output = {}
    for i in range(input, 0, -1):
        output[i] = i+1
    return output

assertFunc(foo, 2, 3)
assertFunc(foo, 3, 4)
assertFunc(foo, 3, 3)

assertFunc(foo_list, 3, [3, 2, 1])
assertFunc(foo_list, 3, [1, 2, 3])
assertFunc(foo_list, 3, [1, 2, 3], True)
assertFunc(foo_list, 3, [1, 2])

assertFunc(foo_tuple, 3, (3, 2, 1))
assertFunc(foo_tuple, 3, (1, 2, 3))
assertFunc(foo_tuple, 3, (1, 2, 3), True)
assertFunc(foo_tuple, 3, (1, 2))

assertFunc(foo_set, 3, {3, 2, 1})
assertFunc(foo_set, 3, {1, 2, 3})
assertFunc(foo_set, 3, {1, 2})

assertFunc(foo_dict, 3, {3:4, 2:3, 1:2})
assertFunc(foo_dict, 3, {1:2, 2:3, 3:4})
assertFunc(foo_dict, 3, {1:1, 2:3, 3:4})
assertFunc(foo_dict, 3, {1:2, 2:3})'''

root = tk.Tk()
boardCanvas = tk.Canvas(root, width=128*6, height=128*6)
boardCanvas.pack()

'''createPiece'''

'''removePiece'''

'''movePiece'''

'''initialize'''

'''isThreatened'''
# pawns
pawnsetup = [
    "XXXXXXXXXXXXXXXX",
    "XXBPXXBPXXXXBPXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXWPXXWPXXXXWPXX",
    "XXXXXXXXXXXXXXXX"
]
b_pawn = Board(pawnsetup)

print("---TESTING PAWN THREATS---")
assertFunc(b_pawn.isThreatened, [(1, 6), "B"], True)
assertFunc(b_pawn.isThreatened, [(2, 6), "B"], False)
assertFunc(b_pawn.isThreatened, [(3, 6), "B"], True)
assertFunc(b_pawn.isThreatened, [(4, 6), "B"], False)
assertFunc(b_pawn.isThreatened, [(5, 6), "B"], True)
assertFunc(b_pawn.isThreatened, [(6, 6), "B"], True)
assertFunc(b_pawn.isThreatened, [(7, 6), "B"], False)
assertFunc(b_pawn.isThreatened, [(8, 6), "B"], True)
assertFunc(b_pawn.isThreatened, [(1, 3), "W"], True)
assertFunc(b_pawn.isThreatened, [(2, 3), "W"], False)
assertFunc(b_pawn.isThreatened, [(3, 3), "W"], True)
assertFunc(b_pawn.isThreatened, [(4, 3), "W"], False)
assertFunc(b_pawn.isThreatened, [(5, 3), "W"], True)
assertFunc(b_pawn.isThreatened, [(6, 3), "W"], True)
assertFunc(b_pawn.isThreatened, [(7, 3), "W"], False)
assertFunc(b_pawn.isThreatened, [(8, 3), "W"], True)
print()

# rooks
rooksetup = [
    "XXXXXXXXXXXXXXXX",
    "XXBRXXXXXXXXBRXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXBPXX",
    "XXXXXXXXXXXXWPXX",
    "XXXXXXXXXXXXXXXX",
    "XXWRXXXXXXXXWRXX",
    "XXXXXXXXXXXXXXXX"
]
b_rook = Board(rooksetup)

print("---TESTING ROOK THREATS---")
assertFunc(b_rook.isThreatened, [(2, 1), "W"], True)
assertFunc(b_rook.isThreatened, [(1, 2), "W"], True)
assertFunc(b_rook.isThreatened, [(3, 2), "W"], True)
assertFunc(b_rook.isThreatened, [(2, 4), "W"], True)
assertFunc(b_rook.isThreatened, [(2, 5), "B"], True)
assertFunc(b_rook.isThreatened, [(7, 4), "B"], False)
assertFunc(b_rook.isThreatened, [(7, 5), "W"], False)
print()

# knights
knightsetup = [
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXWNXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXBNXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXX"
]
b_knight = Board(knightsetup)

print("---TESTING KNIGHT THREATS---")
wt_pos = [(5, 4), (7, 4), (8, 5), (8, 7), (7, 8), (5, 8), (4, 7), (4, 5)]
wf_pos = []
for x in range(1, 9):
    for y in range(1, 9):
        if (x, y) not in wt_pos:
            wf_pos.append((x, y))
bt_pos = [(2, 1), (4, 1), (5, 2), (5, 4), (4, 5), (2, 5), (1, 4), (1, 2)]
bf_pos = []
for x in range(1, 9):
    for y in range(1, 9):
        if (x, y) not in bt_pos:
            bf_pos.append((x, y))
for pos in wt_pos:
    assertFunc(b_knight.isThreatened, [pos, "W"], True)
for pos in wf_pos:
    assertFunc(b_knight.isThreatened, [pos, "W"], False)
for pos in bt_pos:
    assertFunc(b_knight.isThreatened, [pos, "B"], True)
for pos in bf_pos:
    assertFunc(b_knight.isThreatened, [pos, "B"], False)
print()

# bishops
bishopsetup = [
    "XXXXXXXXXXXXXXXX",
    "XXBBXXXXXXXXBBXX",
    "XXXXXXXXXXXXXXXX",
    "XXXXXXBRXXXXXXXX",
    "XXXXXXXXWRXXXXXX",
    "XXXXXXXXXXXXXXXX",
    "XXWBXXXXXXXXWBXX",
    "XXXXXXXXXXXXXXXX"
]
b_bishop = Board(bishopsetup)

print ("---TESTING BISHOP THREATS---")
assertFunc(b_bishop.isThreatened, [(2, 7), "W"], True)
assertFunc(b_bishop.isThreatened, [(7, 7), "W"], False)
assertFunc(b_bishop.isThreatened, [(2, 2), "B"], False)
assertFunc(b_bishop.isThreatened, [(7, 2), "B"], True)
assertFunc(b_bishop.isThreatened, [(1, 6), "B"], True)
assertFunc(b_bishop.isThreatened, [(1, 8), "B"], True)
assertFunc(b_bishop.isThreatened, [(3, 8), "B"], True)
assertFunc(b_bishop.isThreatened, [(4, 4), "B"], False)
assertFunc(b_bishop.isThreatened, [(5, 5), "W"], False)
print()

# queens

# kings

'''getMoves'''
# standard config
b1 = Board()

pawnmoves = [(1, 6), (1, 5)]
rookmoves = []
knightmoves = [(1, 6), (3, 6)]
bishopmoves = []
queenmoves = []
kingmoves = []

assertFunc(b1.getMoves, (1, 7), pawnmoves, unpack=False)
assertFunc(b1.getMoves, (1, 8), rookmoves, unpack=False)
assertFunc(b1.getMoves, (2, 8), knightmoves, unpack=False)
assertFunc(b1.getMoves, (3, 8), bishopmoves, unpack=False)
assertFunc(b1.getMoves, (4, 8), queenmoves, unpack=False)
assertFunc(b1.getMoves, (5, 8), kingmoves, unpack=False)

# custom config 1
setup = [
    "BRXXXXBQBKXXXXBR",
    "XXBPBPXXXXXXBBBP",
    "BNXXBBXXXXXXBPBN",
    "BPWBXXBPWNBPXXXX",
    "XXXXXXXXXXXXXXXX",
    "WNWPXXXXWPXXWQXX",
    "WPWBWPWPXXWPWPWP",
    "WRXXXXXXXXWRWKXX"
]
b2 = Board(setup)

pawnmoves1 = [(2, 5)]
pawnmoves2 = [(3, 6), (3, 5)]
rookmoves1 = [(2, 8), (3, 8), (4, 8), (5, 8)]
rookmoves2 = [(2, 8), (3, 8), (4, 8), (5, 8)]
knightmoves1 = [(3, 5), (2, 8)]
knightmoves2 = [(4, 2), (6, 2), (7, 3), (7, 5), (6, 6), (4, 6), (3, 5), (3, 3)]
bishopmoves1 = [(1, 3), (3, 3), (1, 5), (3, 5), (4, 6), (5, 7)]
bishopmoves2 = [(3, 8), (3, 6), (4, 5)]
queenmoves = [(7, 3), (7, 4), (7, 5), (6, 5), (6, 6), (8, 5), (8, 6)]
kingmoves = [(8, 8)]

assertFunc(b2.getMoves, (2, 6), pawnmoves1, unpack=False)
assertFunc(b2.getMoves, (3, 7), pawnmoves2, unpack=False)
assertFunc(b2.getMoves, (1, 8), rookmoves1, unpack=False)
assertFunc(b2.getMoves, (6, 8), rookmoves2, unpack=False)
assertFunc(b2.getMoves, (1, 6), knightmoves1, unpack=False)
assertFunc(b2.getMoves, (5, 4), knightmoves2, unpack=False)
assertFunc(b2.getMoves, (2, 4), bishopmoves1, unpack=False)
assertFunc(b2.getMoves, (2, 7), bishopmoves2, unpack=False)
assertFunc(b2.getMoves, (7, 6), queenmoves, unpack=False)
assertFunc(b2.getMoves, (7, 8), kingmoves, unpack=False)

# should probably test for check/checkmate

'''getAllMoves'''

'''checkForStalemate'''

'''changeTurns'''