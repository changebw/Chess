#TERM PROJECT: CHESS

import random
import copy
from cmu_112_graphics import *
from walter import *

# PIECES CLASSES
class Pawn(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = []
        self.captures = []

    def __repr__(self):
        return self.name

    def getColor(self):
        return self.color

    def getMoves(self, board, row, col, en):
        legalMoves = []
        self.moves = []
        if (self.color == 'white'):
            if (row == 6):
                self.moves = [(-1,0),(-2,0)]
            else:
                self.moves = [(-1,0)]
            self.captures = [(-1,1),(-1,-1)]
        else:
            if (row == 1):
                self.moves = [(1,0),(2,0)]
            else:
                self.moves = [(1,0)]
            self.captures = [(1,1),(1,-1)]
        for x, y in self.moves:
            if (0 <= row + x < 8):
                if (board[row + x][col] == 0):
                    if (abs(x) == 2):
                        if (board[row + int(x/2)][col] == 0):
                            legalMoves.append((row + x, col + y))
                            break
                    else:
                        legalMoves.append((row + x, col + y))
        #captures
        for x, y in self.captures:
            if (0 <= row + x < 8 and 0 <= col + y < 8):
                if (board[row + x][col + y] != 0 and board[row + x][col + y].getColor() != self.color):
                    legalMoves.append((row + x, col + y))
                elif en < 9:
                    if (col + y == en):
                        if self.color == "white" and row == 3 and board[row][en].getColor() != self.color:
                            legalMoves.append((row + x, col + y))
                        elif self.color == "black" and row == 4 and board[row][en].getColor() != self.color:
                            legalMoves.append((row + x, col + y))
        return legalMoves

class Knight(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = [(1,2),(2,1),(-1,-2),(-2,-1),(-1,2),(2,-1),(1,-2),(-2,1)]

    def __repr__(self):
        return self.name

    def getColor(self):
        return self.color

    def getMoves(self, board, row, col):
        legalMoves = []
        for x, y in self.moves:
            if (0 <= row + x < 8 and 0 <= col + y < 8):
                if (board[row + x][col + y] == 0 or board[row + x][col + y].getColor() != self.color):
                    legalMoves.append((row + x, col + y))
        return legalMoves 

class Bishop(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def __repr__(self):
        return self.name

    def getColor(self):
        return self.color

    def getMoves(self, board, row, col):
        legalMoves = []
        directions = [(1,1),(1,-1), (-1,1),(-1,-1)]
        
        for dRow, dCol in directions:
            newRow = row + dRow
            newCol = col + dCol
            openSquares = True
            while openSquares:
                if (0 <= newRow < 8 and 0 <= newCol < 8):
                    if (board[newRow][newCol] == 0):
                        legalMoves.append((newRow, newCol))
                        newRow += dRow
                        newCol += dCol
                    elif (board[newRow][newCol].getColor() != self.color):
                        legalMoves.append((newRow, newCol))
                        openSquares = False
                    else:
                        openSquares = False
                else:
                    openSquares = False 
        return legalMoves

class Rook(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = []
    
    def __repr__(self):
        return self.name

    def getColor(self):
        return self.color
    
    def getMoves(self, board, row, col):
        legalMoves = []
        directions = [(1,0),(-1,0), (0,1),(0,-1)]

        for dRow, dCol in directions:
            newRow = row + dRow
            newCol = col + dCol
            openSquares = True
            while (openSquares == True):
                if (0 <= newRow < 8 and 0 <= newCol < 8):
                    if (board[newRow][newCol] == 0):
                        legalMoves.append((newRow, newCol))
                        newRow += dRow
                        newCol += dCol
                    elif (board[newRow][newCol].getColor() != self.color):
                        legalMoves.append((newRow, newCol))
                        openSquares = False
                    else:
                        openSquares = False
                else:
                    openSquares = False
        return legalMoves    

class Queen(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def __repr__(self):
        return self.name
    
    def getMoves(self, board, row, col):
        legalMoves = []
        directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        for dRow, dCol in directions:
            newRow = row + dRow
            newCol = col + dCol
            openSquares = True
            while (openSquares == True):
                if (0 <= newRow < 8 and 0 <= newCol < 8):
                    if (board[newRow][newCol] == 0):
                        legalMoves.append((newRow, newCol))
                        newRow += dRow
                        newCol += dCol
                    elif (board[newRow][newCol].getColor() != self.color):
                        legalMoves.append((newRow, newCol))
                        openSquares = False
                    else:
                        openSquares = False
                else:
                    openSquares = False
        return legalMoves

    def getColor(self):
        return self.color

class King(object):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moves = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
        self.whiteCastleK = True
        self.whiteCastleQ = True
        self.blackCastleK = True
        self.blackCastleQ = True

    def __repr__(self):
        return self.name
    
    def getColor(self):
        return self.color

    def getMoves(self, board, row, col, wk, wq, bk, bq):
        moves = []
        for x, y in self.moves:
            if (0 <= row + x < 8 and 0 <= col + y < 8):
                if (board[row + x][col + y] == 0 or board[row + x][col + y].getColor() != self.color):
                    moves.append((row + x, col + y))
        if (self.color == "white"):
            if wk:
                if (board[7][5] == 0 and board[7][6] == 0):
                    moves.append((7, 6))
            if wq:
                if (board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0):
                    moves.append((7, 2))
        else:
            if bk:
                if (board[0][5] == 0 and board[0][6] == 0):
                    moves.append((0, 6))
            if bq:
                if (board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0):
                    moves.append((0, 2))
        return moves

# BOARD CLASS
class Board(object):
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.promPiece = 0
        self.enp = 9
        self.fifty = 0
        self.lastScore = 0
        self.blackCheck = False
        self.whiteCheck = False
        self.squares = [[0]*self.cols for i in range(self.rows)]
        self.pastPieces = []
        self.pastMoves = []
        self.castList = []
        self.promList = []
        self.checkList = []
        self.enpList = []
        self.enHapList = []
        self.pastScores = []
        self.scores = []
        self.enHap = False
        self.mate = False
        self.whiteCastleK = True
        self.whiteCastleQ = True
        self.blackCastleK = True
        self.blackCastleQ = True
        self.blackPromote = False
        self.whitePromote = False
        self.winner = None
        self.heat = [[1,1,1,1.01,1.01,1,1,1],[1,1.01,1.02,1.03,1.03,1.02,1.01,1],[1,1.02,1.03,1.04,1.04,1.03,1.02,1],[1.01,1.03,1.04,1.05,1.05,1.04,1.03,1.01],[1.01,1.03,1.04,1.05,1.05,1.04,1.03,1.01],[1,1.02,1.03,1.04,1.04,1.03,1.02,1],[1,1.01,1.02,1.03,1.03,1.02,1.01,1],[1,1,1,1.01,1.01,1,1,1]]
        self.pawnHeat = [[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1.01,1.02,1.02,1,1,1],[1.01,1.01,1.02,1.04,1.04,1.01,1.01,1.01],[1.02,1.02,1.03,1.05,1.05,1.02,1.02,1.02],[1.04,1.04,1.05,1.07,1.07,1.04,1.04,1.04],[1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1],[10,10,10,10,10,10,10,10]]

    def startBoard(self, app):
        #add black pieces to top of the board
        col = 0
        for i in range(len(app.blackPieces)):
            if (i < 8):
                self.squares[0][i] = app.blackPieces[i]
            else:
                self.squares[1][col] = app.blackPieces[i]
                col += 1
        #add white pieces to bottom of the board
        col = 0
        for i in range(len(app.whitePieces)):
            if (i < 8):
                self.squares[7][i] = app.whitePieces[i]
            else:
                self.squares[6][col] = app.whitePieces[i]
                col += 1
        for x in range(4):
            for y in range(8):
                self.squares[x+2][y] = 0
        return self.squares

    def getRowsAndCols(self):
        return self.rows, self.cols

    def makeMove(self, one, two):
        x1, y1 = one
        x2, y2 = two
        #appends all the lists to store values for when moves are undone
        self.pastMoves.append(one)
        self.pastMoves.append(two)
        self.promList.append((self.whitePromote, self.blackPromote))
        self.castList.append((self.whiteCastleK, self.whiteCastleQ, self.blackCastleK, self.blackCastleQ))
        self.checkList.append((self.whiteCheck, self.blackCheck))
        self.enpList.append(self.enp)
        self.enHapList.append(self.enHap)
        self.pastScores.append(self.lastScore)
        self.checkEnPassant(x1, y1, x2, y2)
        if (self.squares[x2][y2] == 0):
            piece = None
            self.pastPieces.append(piece)
        else:
            self.pastPieces.append(self.squares[x2][y2])
        #makes the move and checks for special kinds of moves
        self.checkPromotion(x1, y1, x2)
        if self.whitePromote:
            self.promote(one, two, "white")
        elif self.blackPromote:
            self.promote(one, two, "black")
        else:
            self.squares[x2][y2] = self.squares[x1][y1]
        self.checkEnPassant(x1, y1, x2, y2)
        self.checkTwoPawn(x1, x2, y2)
        self.squares[x1][y1] = 0
        self.checkCastling(one, two)
        self.checkChecks(x2, y2)
        self.whitePromote = False
        self.blackPromote = False
        self.promPiece = 0

    def setPromote(self, p):
        #sets promote value based on piece selected
        self.promPiece = p
    
    def getPromPiece(self):
        return self.promPiece

    def getCheck(self):
        return self.whiteCheck, self.blackCheck

    def promote(self, one, two, color):
        x1, y1 = one
        x2, y2 = two
        #promotes pawn based on input prom piece value
        if self.promPiece == 1:
            self.squares[x2][y2] = Knight('N', color)
        elif self.promPiece == 2:
            self.squares[x2][y2] = Bishop('B', color)
        elif self.promPiece == 3:
            self.squares[x2][y2] = Rook('R', color)
        elif self.promPiece == 4:
            self.squares[x2][y2] = Queen('Q', color)
        else:
            self.squares[x2][y2] = self.squares[x1][y1]

    def getPromote(self):
        return self.whitePromote, self.blackPromote

    def checkPromotion(self, x, y, row):
        if isinstance(self.squares[x][y], Pawn):
            #checks square of Pawn to see if reached end of the board
            if (self.squares[x][y].getColor() == "white" and row == 0):
                self.whitePromote = True
                self.blackPromote = False
            elif (self.squares[x][y].getColor() == "black" and row == 7):
                self.blackPromote = True
                self.whitePromote = False
            else:
                self.whitePromote = False
                self.blackPromote = False

    def checkTwoPawn(self, x1, x2, y):
        if isinstance(self.squares[x2][y], Pawn):
            if abs(x1 - x2) == 2:
                self.enp = y
            else:
                self.enp = 9
        else:
            self.enp = 9

    def checkEnPassant(self, x1, y1, x2, y2):
        if self.enp != 9:
            if isinstance(self.squares[x2][y2], Pawn):
                if y2 == self.enp:
                    if (x2 == 2 and self.squares[x2][y2].getColor() == "white") or (x2 == 5 and self.squares[x2][y2].getColor() == "black"):
                        if abs(x1 - x2) == 1:
                            if abs(y1 - y2) == 1:
                                self.squares[x1][y2] = 0
                                self.enHap = True
        else:
            self.enHap = False

    def checkLegal(self, color, r, c, a, b):
        moves = []
        for row in range(8):
            for col in range(8):
                if (self.squares[row][col] != 0):
                    if (self.squares[row][col].getColor() != color):
                        if isinstance(self.squares[row][col], King):
                            moves = self.squares[row][col].getMoves(self.squares, row, col, self.whiteCastleK, self.whiteCastleQ, self.blackCastleK, self.blackCastleQ)
                        elif isinstance(self.squares[row][col], Pawn):
                            moves = self.squares[row][col].getMoves(self.squares, row, col, self.enp)
                        else:
                            moves = self.squares[row][col].getMoves(self.squares, row, col)
                        for x, y in moves:
                            if self.squares[x][y] != 0:
                                if (isinstance(self.squares[x][y], King) and self.squares[x][y].getColor() == color):
                                    return False
                                elif isinstance(self.squares[a][b], King):
                                    if (c - b == 2):
                                        if (y == 3 and r == x):
                                            return False
                                    elif (c - b == -2):
                                        if (y == 5 and r == x):
                                            return False
        return True
        
    def checkChecks(self, row, col):
        mayChecks = []
        if (self.squares[row][col] != 0):
            if isinstance(self.squares[row][col], Pawn):
                pawnMoves = self.squares[row][col].getMoves(self.squares, row, col, self.enp)
                for x, y in pawnMoves:
                    if (y != col):
                        mayChecks.append((x, y))
            else:
                if isinstance(self.squares[row][col], King):
                    mayChecks = self.squares[row][col].getMoves(self.squares, row, col, self.whiteCastleK, self.whiteCastleQ, self.blackCastleK, self.blackCastleQ)
                else:
                    mayChecks = self.squares[row][col].getMoves(self.squares, row, col)
            for x, y in mayChecks:
                if (repr(self.squares[x][y]) == 'bk' and self.squares[row][col].getColor() == "white"):
                    self.blackCheck = True
                    self.whiteCheck = False
                    self.blackCastleK = False
                    self.blackCastleQ = False
                    break
                elif (repr(self.squares[x][y]) == 'wk' and self.squares[row][col].getColor() == "black"):
                    self.whiteCheck = True
                    self.blackCheck = False
                    self.whiteCastleK = False
                    self.whiteCastleQ = False
                    break
                else:
                    self.whiteCheck = False
                    self.blackCheck = False

    def checkmate(self, color):
        moves = []
        moves = self.allMoves(color)
        if moves == []:
            self.mate = True
        elif self.draw():
            self.mate = True
        elif self.fifty == 50:
            self.mate = True
        return self.mate

    def draw(self):
        mCountB = 0
        mCountW = 0
        for row in range(8):
            for col in range(8):
                if self.squares[row][col] == 0 or isinstance(self.squares[row][col], King):
                    pass
                elif isinstance(self.squares[row][col], Bishop):
                    if self.squares[row][col].getColor() == "white":
                        mCountW += 1
                    else:
                        mCountB += 1
                elif isinstance(self.squares[row][col], Knight):
                    if self.squares[row][col].getColor() == "white":
                        mCountW += 1
                    else:
                        mCountB += 1
                else:
                    return False
                if mCountB > 1 or mCountW > 1:
                    return False
        return True

    def getWinner(self):
        if self.mate:
            if self.blackCheck:
                self.winner = "White"
            elif self.whiteCheck:
                self.winner = "Black"
            else:
                self.winner = "Draw"
        return self.winner

    def undoMove(self):
        x2, y2 = self.pastMoves.pop()
        x1, y1 = self.pastMoves.pop()
        piece1 = self.pastPieces.pop()
        wprom, bprom = self.promList.pop()
        self.whiteCastleK, self.whiteCastleQ, self.blackCastleK, self.blackCastleQ = self.castList.pop()
        self.whiteCheck, self.blackCheck = self.checkList.pop()
        self.enp = self.enpList.pop()
        self.lastScore = self.pastScores.pop()
        if wprom:
            self.squares[x1][y1] = Pawn('wp', 'white')
        elif bprom:
            self.squares[x1][y1] = Pawn('bp', 'black')
        else:
            self.squares[x1][y1] = self.squares[x2][y2]
        if isinstance(self.squares[x1][y1], King):
            if (y2 - y1 == 2):
                if (x1 == 7):
                    self.squares[x1][7] = Rook('wr','white')
                    self.squares[x1][5] = 0
                elif (x1 == 0):
                    self.squares[x1][7] = Rook('br','black')
                    self.squares[x1][5] = 0
            elif (y2 - y1 == -2):
                if (x1 == 7):
                    self.squares[x1][0] = Rook('wr','white')
                    self.squares[x1][3] = 0
                elif (x1 == 0):
                    self.squares[x1][0] = Rook('br','black')
                    self.squares[x1][3] = 0
        if self.enHap:
            if self.squares[x1][y1].getColor() == "white":
                self.squares[x1][y2] = Pawn('bp', 'black')
            else:
                self.squares[x1][y2] = Pawn('wp', 'white')
        self.enHap = self.enHapList.pop()
        if (piece1 != None):
            self.squares[x2][y2] = piece1
        else:
            self.squares[x2][y2] = 0
        self.mate = False
        self.winner = None
    
    def checkCastling(self, one, two):
        y1 = one[1]
        x2, y2 = two
        if (repr(self.squares[x2][y2]) == "wk"):
            if (y1 - y2 == -2):
                self.squares[7][5] = self.squares[7][7]
                self.squares[7][7] = 0
            elif (y1 - y2 == 2):
                self.squares[7][3] = self.squares[7][0]
                self.squares[7][0] = 0
            self.whiteCastleK = False
            self.whiteCastleQ = False
        elif (repr(self.squares[x2][y2]) == "bk"):
            if (y1 - y2 == -2):
                self.squares[0][5] = self.squares[0][7]
                self.squares[0][7] = 0
            elif (y1 - y2 == 2):
                self.squares[0][3] = self.squares[0][0]
                self.squares[0][0] = 0
            self.blackCastleK = False
            self.blackCastleQ = False
        elif ((repr(self.squares[x2][y2]) == "wr" and y1 == 0) or (x2 == 7 and y2 == 0)):
            self.whiteCastleQ = False
        elif ((repr(self.squares[x2][y2]) == "wr" and y1 == 7) or (x2 == 7 and y2 == 7)):
            self.whiteCastleK = False
        elif ((repr(self.squares[x2][y2]) == "br" and y1 == 0) or (x2 == 0 and y2 == 0)):
            self.blackCastleQ = False
        elif ((repr(self.squares[x2][y2]) == "br" and y1 == 7) or (x2 == 0 and y2 == 7)):
            self.blackCastleK = False

    def getScore(self):
        score = 0
        for row in range(8):
            for col in range(8):
                if (self.squares[row][col] != 0):
                    if isinstance(self.squares[row][col], Pawn):
                        if (self.squares[row][col].getColor() == "white"):
                            score += 1*self.pawnHeat[row][col]
                        else:
                            score -= 1*self.pawnHeat[7-row][7-col]
                    if isinstance(self.squares[row][col], Knight):
                        if (self.squares[row][col].getColor() == "white"):
                            score += 3*self.heat[row][col]
                        else:
                            score -= 3*self.heat[row][col]
                    if isinstance(self.squares[row][col], Bishop):
                        if (self.squares[row][col].getColor() == "white"):
                            score += 3*self.heat[row][col]
                        else:
                            score -= 3*self.heat[row][col]
                    if isinstance(self.squares[row][col], Rook):
                        if (self.squares[row][col].getColor() == "white"):
                            score += 5*self.heat[row][col]
                        else:
                            score -= 5*self.heat[row][col]
                    if isinstance(self.squares[row][col], Queen):
                        if (self.squares[row][col].getColor() == "white"):
                            score += 9*self.heat[row][col]
                        else:
                            score -= 9*self.heat[row][col]
                    if isinstance(self.squares[row][col], King):
                        if (self.squares[row][col].getColor() == "white"):
                            score += 1000
                        else:
                            score -= 1000
        return score

    def getBoard(self):
        return self.squares

    def allMoves(self, color):
        moves = []
        moves2 = []
        possible = []
        for row in range(8):
            for col in range(8):
                if (self.squares[row][col] != 0):
                    if (self.squares[row][col].getColor() == color):
                        if isinstance(self.squares[row][col], King):
                            possible = self.squares[row][col].getMoves(self.squares, row, col, self.whiteCastleK, self.whiteCastleQ, self.blackCastleK, self.blackCastleQ)
                        elif isinstance(self.squares[row][col], Pawn):
                            possible = self.squares[row][col].getMoves(self.squares, row, col, self.enp)
                        else:
                            possible = self.squares[row][col].getMoves(self.squares, row, col)
                        if (len(possible) != 0):
                            for x, y in possible:
                                self.makeMove((row, col), (x, y))
                                legal = self.checkLegal(color, row, col, x, y)
                                self.undoMove()
                                if legal:
                                    moves.append((row, col))
                                    moves.append((x, y))
                                    moves2.append(moves)
                                    moves = []
                possible = []
        return moves2

    def testPrint(self):
        print(self.enpList)
        print(self.enHap)

#start the app
def appStarted(app):
    app.margin = app.height/25
    app.moveNum = 0
    app.theBoard = Board()
    app.rows, app.cols = app.theBoard.getRowsAndCols()
    app.board = []
    app.blackPieces = []
    app.whitePieces = []
    app.legalMoves = []
    app.pastBoard = []
    #app.passing = []
    app.illegal = []
    app.checkMoves = []
    app.lastMove = []
    app.whitePawn = app.loadImage('wp.png')
    app.blackPawn = app.loadImage('bp.png')
    app.whiteKnight = app.loadImage('wn.png')
    app.blackKnight = app.loadImage('bn.png')
    app.whiteBishop = app.loadImage('wb.png')
    app.blackBishop = app.loadImage('bb.png')
    app.whiteRook = app.loadImage('wr.png')
    app.blackRook = app.loadImage('br.png')
    app.whiteQueen = app.loadImage('wq.png')
    app.blackQueen = app.loadImage('bq.png')
    app.whiteKing = app.loadImage('wk.png')
    app.blackKing = app.loadImage('bk.png')
    app.background = app.loadImage('chess.jpg')
    app.background2 = app.loadImage('pretty.png')
    #black pieces, first half of back row
    app.blackPieces.extend([Rook('br','black'),Knight('bn','black'),Bishop('bb','black'),Queen('bq','black')])
    #black pieces, second half of back row
    app.blackPieces.extend([King('bk','black'),Bishop('bb','black'),Knight('bn','black'),Rook('br','black')])
    #white pieces, first half of back row
    app.whitePieces.extend([Rook('wr','white'),Knight('wn','white'),Bishop('wb','white'),Queen('wq','white')])
    #white pieces, second half of back row
    app.whitePieces.extend([King('wk','white'),Bishop('wb','white'),Knight('wn','white'),Rook('wr','white')])
    #black pawns
    app.blackPieces.extend([Pawn('bp','black'),Pawn('bp','black'),Pawn('bp','black'),Pawn('bp','black')])
    app.blackPieces.extend([Pawn('bp','black'),Pawn('bp','black'),Pawn('bp','black'),Pawn('bp','black')])
    #white pawns
    app.whitePieces.extend([Pawn('wp','white'),Pawn('wp','white'),Pawn('wp','white'),Pawn('wp','white')])
    app.whitePieces.extend([Pawn('wp','white'),Pawn('wp','white'),Pawn('wp','white'),Pawn('wp','white')])
    #empty squares
    app.board = app.theBoard.startBoard(app)
    app.gameMode = 'menu'
    app.drawLegal = False
    app.updateColor = False
    app.clickedSquareRow = None
    app.clickedSquareCol = None
    app.moveToSquareRow = None
    app.moveToSquareCol = None
    app.checkPieceRow = None
    app.checkPieceCol = None
    app.whiteCastleK = True
    app.whiteCastleQ = True
    app.blackCastleK = True
    app.blackCastleQ = True
    app.blackCheck = False
    app.whiteCheck = False
    app.whiteProm = False
    app.blackProm = False
    app.firstSquareClicked = False
    app.flip = False
    app.inPassing = False
    app.twoPlayer = False
    app.onePlayer = False
    app.gameOver = False
    app.winner = None
    app.player = None
  
#from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    if app.width <= app.height:
        size = app.width
    else:
        size = app.height
    gridWidth  = size - 4*app.margin
    gridHeight = size - 4*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    if app.flip:
        row = 7 - row
        col = 7 - col
    x0 = 2*app.margin + col * cellWidth
    x1 = 2*app.margin + (col+1) * cellWidth
    y0 = 2*app.margin + row * cellHeight
    y1 = 2*app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

#from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if app.width <= app.height:
        size = app.width
    else:
        size = app.height
    gridWidth  = size - 4*app.margin
    gridHeight = size - 4*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - 2*app.margin) / cellHeight)
    col = int((x - 2*app.margin) / cellWidth)
    if app.flip:
        row = 7 - row
        col = 7 - col
    return (row, col)

#have to check if the move is legal!
def movePiece(app, x, y):
    #first square
    row, col = getCell(app, x, y)
    if row < 0 or row > 7 or col < 0 or col > 7:
        return None
    if (app.firstSquareClicked == False):
        app.legalMoves = []
        app.clickedSquareRow = row
        app.clickedSquareCol = col
        if app.moveNum % 2 == 0:
            color = "white"
        else:
            color = "black"
        app.legalMoves = app.theBoard.allMoves(color)
        for move in app.legalMoves:
            if ((row, col) == move[0]):
                app.firstSquareClicked = True
                app.drawLegal = True
                app.updateColor = True
                break
    #move to second square
    else: 
        #check which piece was clicked, call getMoves from piece class
        #loop through piece class 
        #and check if coordinates from first clicked square + coordinates from array equal second clicked square
        for move in app.legalMoves:
            if ((app.clickedSquareRow, app.clickedSquareCol) == move[0]):
                if ((row, col) == move[1]):
                    app.moveToSquareRow = row
                    app.moveToSquareCol = col
                    app.theBoard.checkPromotion(app.clickedSquareRow, app.clickedSquareCol, row)
                    app.whiteProm, app.blackProm = app.theBoard.getPromote()
                    
        else:
            if (app.board[row][col] != 0):
                if (app.board[app.clickedSquareRow][app.clickedSquareCol].getColor() == app.board[row][col].getColor()):
                    app.clickedSquareRow = row
                    app.clickedSquareCol = col
    #if two squares are clicked, move the piece to the second clicked square
    if (app.clickedSquareRow != None and app.moveToSquareRow != None and app.whiteProm == False and app.blackProm == False):
        moves(app)

def moves(app):
    x1 = copy.deepcopy(app.clickedSquareRow)
    y1 = copy.deepcopy(app.clickedSquareCol)
    x2 = copy.deepcopy(app.moveToSquareRow)
    y2 = copy.deepcopy(app.moveToSquareCol)
    one = (x1, y1)
    two = (x2, y2)
    app.theBoard.makeMove(one, two)
    app.lastMove.append([one, two])
    app.whiteCheck, app.blackCheck = app.theBoard.getCheck()
    if (app.moveNum % 2 == 0):
        color = "black"
    else:
        color = "white"
    app.gameOver = app.theBoard.checkmate(color)
    if app.gameOver:
        if app.whiteCheck:
            app.winner = "Black"
        elif app.blackCheck:
            app.winner = "White"
        else:
            app.winner = "Draw"
    app.clickedCell = 0
    app.updateColor = False
    app.drawLegal = False
    app.clickedSquareRow = None
    app.clickedSquareCol = None
    app.moveToSquareRow = None
    app.moveToSquareCol = None
    app.firstSquareClicked = False
    app.whiteProm = False
    app.blackProm = False
    app.moveNum += 1
    if (app.gameMode == '1p' and app.gameOver == False):
        computerMove(app)

def computerMove(app):
    if app.moveNum % 2 == 0:
        color = "white"
        ncolor = "black"
        maxPlayer = True
    else:
        color = "black"
        ncolor = "white"
        maxPlayer = False
    one, two = miniMax(app.theBoard, 3, -10000, 10000, maxPlayer, color)[0]
    x, y = one
    app.theBoard.checkPromotion(x, y, two[0])
    wp, bp = app.theBoard.getPromote()
    if wp or bp:
        app.theBoard.setPromote(4)
    app.theBoard.makeMove(one, two)
    app.lastMove.append([one, two])
    app.moveNum += 1
    app.gameOver = app.theBoard.checkmate(ncolor)
    app.whiteCheck, app.blackCheck = app.theBoard.getCheck()
    if app.gameOver:
        if app.whiteCheck:
            app.winner = "Black"
        elif app.blackCheck:
            app.winner = "White"
        else:
            app.winner = "Draw"
    if app.gameOver == False:
        app.whiteCheck, app.blackCheck = app.theBoard.getCheck()

def keyPressed(app, event):
    if (event.key == 'r'):
        appStarted(app)
    elif (event.key == 'u'):
        if (app.moveNum > 0):
            if (app.gameMode == '1p' and app.moveNum > 1):
                    app.theBoard.undoMove()
                    app.moveNum -= 1
            app.moveNum -= 1
            app.theBoard.undoMove()
            app.board = app.theBoard.getBoard()
            app.lastMove.pop()
            app.gameOver = False
            app.clickedCell = 0
            app.updateColor = False
            app.drawLegal = False
            app.clickedSquareRow = None
            app.clickedSquareCol = None
            app.moveToSquareRow = None
            app.moveToSquareCol = None
            app.firstSquareClicked = False
            app.whiteProm = False
            app.blackProm = False
            app.whiteCheck, app.blackCheck = app.theBoard.getCheck()
            app.winner = None
    elif (event.key == 'p'):
        app.theBoard.testPrint()
    elif (event.key == 'f'):
        app.flip = not(app.flip)
    elif (event.key == 'Space'):
        if (app.gameMode == '0p' and app.gameOver == False):
            computerMove(app)
        elif (app.gameMode == '1p' and app.player == 'black' and app.moveNum == 0):
            computerMove(app)

def mousePressed(app, event):
    if app.gameOver == False:
        x, y = event.x, event.y
        if event.num == 1:
            if (app.gameMode == 'menu'):
                menuClick(app, x, y)
            elif (app.gameMode == 'choose'):
                choiceClick(app, x, y)
            elif (app.gameMode == 'pickColor'):
                colorClick(app, x, y)
            elif (app.whiteProm or app.blackProm) and app.theBoard.getPromPiece() == 0:
                promClick(app, x, y)
            else:
                movePiece(app, x, y)

def menuClick(app, x, y):
    if (app.width//4 <= x <= app.width*3//4 and app.height//2 <= y <= app.height*3//4):
        app.gameMode = 'choose'

def choiceClick(app, x, y):
    if (app.width*3//8 <= x <= app.width*5//8 and app.height*5//16 <= y <= app.height*7//16):
        app.gameMode = 'pickColor'
    elif (app.width*3//8 <= x <= app.width*5//8 and app.height*5//8 <= y <= app.height*6//8):
        app.gameMode = '2p'
    elif (app.width*31//36 <= x <= app.width*35//36 and app.height*33//36 <= y <= app.height*35//36):
        app.gameMode = '0p'

def promClick(app, x, y):
    if (app.width//4 <= x <= app.width*3//8 and app.height*7//16 <= y <= app.height*9//16):
        app.theBoard.setPromote(1)
    elif (app.width*3//8 <= x <= app.width//2 and app.height*7//16 <= y <= app.height*9//16):
        app.theBoard.setPromote(2)
    elif (app.width//2 <= x <= app.width*5//8 and app.height*7//16 <= y <= app.height*9//16):
        app.theBoard.setPromote(3)
    elif (app.width*5//8 <= x <= app.width*3//4 and app.height*7//16 <= y <= app.height*9//16):
        app.theBoard.setPromote(4)
    if app.theBoard.getPromPiece() != 0:
        moves(app)

def colorClick(app, x, y):
    if (app.width*3//8 <= x <= app.width*5//8 and app.height*5//16 <= y <= app.height*7//16):
        app.gameMode = '1p'
        app.player = 'white'
    elif (app.width*3//8 <= x <= app.width*5//8 and app.height*5//8 <= y <= app.height*6//8):
        app.gameMode = '1p'
        app.player = 'black'
        app.flip = True

def redrawAll(app, canvas):
    if app.gameMode == 'menu':
        drawMenu(app, canvas)
    elif app.gameMode == 'choose':
        drawChoices(app, canvas)
    elif app.gameMode == 'pickColor':
        drawPColor(app, canvas)
    else:
        drawBoard(app, canvas)
        drawLegalMoves(app, canvas)
        drawPieces(app, canvas)
        if app.whiteProm or app.blackProm:
            drawProm(app, canvas)

def drawProm(app, canvas):
    if app.width <= app.height:
        size = app.width
    else:
        size = app.height
    canvas.create_rectangle(size//4, size*7//16, size*3//4, size*9//16, fill = 'gray60', outline = 'gray30', width = 5)
    canvas.create_rectangle(size//4, size*7//16, size*3//8, size*9//16, outline = 'gray30', width = 5)
    canvas.create_rectangle(size*3//8, size*7//16, size//2, size*9//16, outline = 'gray30', width = 5)
    canvas.create_rectangle(size//2, size*7//16, size*5//8, size*9//16, outline = 'gray30', width = 5)
    canvas.create_rectangle(size*5//8, size*7//16, size*3//4, size*9//16, outline = 'gray30', width = 5)
    if app.whiteProm:
        canvas.create_image(size*5//16, size//2, 
                                    pilImage=app.whiteKnight.resize((size//10,size//10)))
        canvas.create_image(size*7//16, size//2, 
                                    pilImage=app.whiteBishop.resize((size//10,size//10)))
        canvas.create_image(size*9//16, size//2, 
                                    pilImage=app.whiteRook.resize((size//10,size//10)))
        canvas.create_image(size*11//16, size//2, 
                                    pilImage=app.whiteQueen.resize((size//10,size//10)))
    elif app.blackProm:
        canvas.create_image(size*5//16, size//2, 
                                    pilImage=app.blackKnight.resize((size//10,size//10)))
        canvas.create_image(size*7//16, size//2, 
                                    pilImage=app.blackBishop.resize((size//10,size//10)))
        canvas.create_image(size*9//16, size//2, 
                                    pilImage=app.blackRook.resize((size//10,size//10)))
        canvas.create_image(size*11//16, size//2, 
                                    pilImage=app.blackQueen.resize((size//10,size//10)))

def drawLegalMoves(app, canvas):
    if (app.drawLegal):
        for move in app.legalMoves:
            if ((app.clickedSquareRow, app.clickedSquareCol) == move[0]):
                x, y = move[1]
                x0, y0, x1, y1 = getCellBounds(app, x, y)
                if (app.board[x][y] == 0):
                    canvas.create_oval(x0 + (x1-x0)/3, y0 + (y1-y0)/3, x1 - (x1-x0)/3, y1 - (y1-y0)/3,fill = 'turquoise')
                else:
                    canvas.create_rectangle(x0, y0, x1, y1,fill = 'light coral', outline = '')
                    if (x + y) % 2 == 0:
                        color = 'cornsilk2'
                    else:
                        color = 'PaleGreen4'
                    canvas.create_oval(x0, y0, x1, y1, fill = color, outline = '')
    else:
        pass

def drawMenu(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray10')
    canvas.create_rectangle(app.width//16, app.height//8, app.width*7//8, app.height*15//16, fill = 'gray20', width = 0)
    canvas.create_rectangle(app.width//6, app.height//20, app.width*15//16, app.height*13//16, fill = 'gray30', width = 0)
    canvas.create_rectangle(app.width//12, app.height//4, app.width*13//16, app.height*7//8, fill = 'gray40', width = 0)
    canvas.create_rectangle(app.width//5, app.height*2//15, app.width*14//16, app.height*11//16, fill = 'gray50', width = 0)
    canvas.create_rectangle(app.width*2//8, app.height*3//16, app.width*6//8, app.height*6//16, fill = 'gray75', outline = 'gray15', width = 5)
    canvas.create_rectangle(app.width*3//8, app.height//2, app.width*5//8, app.height*10//16, fill = 'gray75', outline = 'gray15', width = 5, activefill = 'indian red')
    canvas.create_text(app.width//2, app.height*9//32, text= "Chess (cool)", font = ('Comic Sans MS', -int(app.height//15), 'bold'), fill = 'gray15')
    canvas.create_text(app.width/2, app.height*9//16, text= "Play", font = ('Comic Sans MS', -int(app.height/20), 'bold'), fill = 'gray15')

def drawChoices(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray10')
    canvas.create_rectangle(app.width//16, app.height//8, app.width*7//8, app.height*15//16, fill = 'gray20', width = 0)
    canvas.create_rectangle(app.width//6, app.height//20, app.width*15//16, app.height*13//16, fill = 'gray30', width = 0)
    canvas.create_rectangle(app.width//12, app.height//4, app.width*13//16, app.height*7//8, fill = 'gray40', width = 0)
    canvas.create_rectangle(app.width//5, app.height*2//15, app.width*14//16, app.height*11//16, fill = 'gray50', width = 0)
    canvas.create_rectangle(app.width*3//8, app.height*5//16, app.width*5//8, app.height*7//16, fill = 'gray75', outline = 'gray15', width = 5, activefill = 'indian red')
    canvas.create_rectangle(app.width*3//8, app.height*10//16, app.width*5//8, app.height*12//16, fill = 'gray75', outline = 'gray15', width = 5, activefill = 'indian red')
    canvas.create_rectangle(app.width*31//36, app.height*33//36, app.width*35//36, app.height*35//36, fill = 'gray75', outline = 'gray15', width = 5, activefill = 'indian red')
    canvas.create_text(app.width//2, app.height*6//16, text= "One-Player", font = ('Comic Sans MS', -int(app.height/30), 'bold'), fill = 'gray15')
    canvas.create_text(app.width//2, app.height*11//16, text= "Two-Player", font = ('Comic Sans MS', -int(app.height/30), 'bold'), fill = 'gray15')
    canvas.create_text(app.width*33//36, app.height*17//18, text= "Zero-Player", font = ('Comic Sans MS', -int(app.height/65), 'bold'), fill = 'gray15')

def drawPColor(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray10')
    canvas.create_rectangle(app.width//16, app.height//8, app.width*7//8, app.height*15//16, fill = 'gray20', width = 0)
    canvas.create_rectangle(app.width//6, app.height//20, app.width*15//16, app.height*13//16, fill = 'gray30', width = 0)
    canvas.create_rectangle(app.width//12, app.height//4, app.width*13//16, app.height*7//8, fill = 'gray40', width = 0)
    canvas.create_rectangle(app.width//5, app.height*2//15, app.width*14//16, app.height*11//16, fill = 'gray50', width = 0)
    canvas.create_rectangle(app.width*3//8, app.height*5//16, app.width*5//8, app.height*7//16, fill = 'gray75', outline = 'gray15', width = 5, activefill = 'indian red')
    canvas.create_rectangle(app.width*3//8, app.height*10//16, app.width*5//8, app.height*12//16, fill = 'gray75', outline = 'gray15', width = 5, activefill = 'indian red')
    canvas.create_text(app.width//2, app.height*6//16, text= "White", font = ('Comic Sans MS', -int(app.height/30), 'bold'), fill = 'gray15')
    canvas.create_text(app.width//2, app.height*11//16, text= "Black", font = ('Comic Sans MS', -int(app.height/30), 'bold'), fill = 'gray15')

def drawBoard(app, canvas):
    #create outline of the board
    if app.width <= app.height:
        size = app.width
    else:
        size = app.height
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray30')
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, app.height - app.margin, fill = 'gray15')
    #canvas.create_rectangle(app.margin, app.margin, 
    #size-app.margin, size-app.margin, outline='')
    #draw board and alternate between two colors, except when starting new row
    nextColor = False
    drawLet = True
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    j = 0
    k = 8
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if (nextColor):
                color = 'PaleGreen4'
                nextColor = False
                if app.moveNum != 0:
                    i = len(app.lastMove)
                    if (row, col) in app.lastMove[i-1]:
                        color = 'aquamarine4'
            else: 
                color = 'cornsilk2'
                nextColor = True
                if app.moveNum != 0:
                    i = len(app.lastMove)
                    if (row, col) in app.lastMove[i-1]:
                        color = 'medium aquamarine'
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1,fill = color, width = 0)
            if drawLet:
                canvas.create_text(x1 - (x1-x0)/2, size - app.margin*3/2, text = letters[j], font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
                j += 1
        #keep same color when starting new row
        if (nextColor): nextColor = False
        else: nextColor = True
        drawLet = False
        canvas.create_text(app.margin*3/2, y1 - (y1-y0)/2, text = str(k), font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
        k -= 1
    if (app.updateColor == True):
        x0, y0, x1, y1 = getCellBounds(app, app.clickedSquareRow, app.clickedSquareCol)
        canvas.create_rectangle(x0, y0, x1, y1,fill = 'khaki', width = 0)
    if (app.blackCheck and app.gameOver == False):
        canvas.create_text(size/2, size - app.margin/2, text= "Black is in check", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
    if (app.whiteCheck and app.gameOver == False):
        canvas.create_text(size/2, size - app.margin/2, text= "White is in check", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
    if (app.gameMode == '0p'):
        canvas.create_text(size/2, app.margin/2, text= "Press Spacebar to make computer move", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
    if (app.gameMode == '1p' and app.player == 'black' and app.moveNum == 0):
        canvas.create_text(size/2, app.margin/2, text= "Press Spacebar to make computer's first move", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
    if (app.gameOver):
        if app.winner == "White":
            canvas.create_text(size/2, size - app.margin/2, text= "White WINS", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
        elif app.winner == "Black":
            canvas.create_text(size/2, size - app.margin/2, text= "Black WINS", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')
        else:
            canvas.create_text(size/2, size - app.margin/2, text= "Stalemate (draw)", font = ('Comic Sans MS', -int(app.margin/2), 'bold'), fill = 'white')

def drawPieces(app, canvas):
    if app.width <= app.height:
        size = app.width
    else:
        size = app.height
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if (app.board[row][col] != 0):
                if (isinstance(app.board[row][col], Pawn) == True):
                    if (app.board[row][col].getColor() == "white"):
                        image = app.whitePawn
                    else:
                        image = app.blackPawn
                if isinstance(app.board[row][col], Knight):
                    if (app.board[row][col].getColor() == "white"):
                        image = app.whiteKnight
                    else:
                        image = app.blackKnight
                if (isinstance(app.board[row][col], Bishop) == True):
                    if (app.board[row][col].getColor() == "white"):
                        image = app.whiteBishop
                    else:
                        image = app.blackBishop
                if (isinstance(app.board[row][col], Rook) == True):
                    if (app.board[row][col].getColor() == "white"):
                        image = app.whiteRook
                    else:
                        image = app.blackRook
                if (isinstance(app.board[row][col], Queen) == True):
                    if (app.board[row][col].getColor() == "white"):
                        image = app.whiteQueen
                    else:
                        image = app.blackQueen
                if (isinstance(app.board[row][col], King) == True):
                    if (app.board[row][col].getColor() == "white"):
                        image = app.whiteKing
                    else:
                        image = app.blackKing
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                canvas.create_image((x1+x0)//2, (y1+y0)//2, 
                                    pilImage=image.resize((size//10,size//10)))

runApp(width=800, height=800)