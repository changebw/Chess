from functools import cache
import random
import math

def miniMax(board, depth, alpha, beta, maxPlayer, color):
    if (depth == 0):
        return None, board.getScore()
    elif board.checkmate(color):
        if (board.getWinner() == "White"):
            return None, 5000
        elif (board.getWinner() == "Black"):
            return None, -5000
        elif (board.getWinner() == "Draw"):
            return None, 0
    moves = board.allMoves(color)
    random.shuffle(moves)

    if maxPlayer:
        maxScore = -10000
        for move in moves:
            x, y = move[0]
            board.checkPromotion(x, y, move[1][0])
            wp, bp = board.getPromote()
            if wp or bp:
                board.setPromote(4)
            board.makeMove(move[0], move[1])
            score = miniMax(board, depth - 1, alpha, beta, False, "black")[1]
            board.undoMove()
            if (score > maxScore):
                maxScore = score
                best = move
            alpha = max(alpha, score)
            if (beta <= alpha):
                break
        return best, maxScore
    else:
        minScore = 10000
        for move in moves:
            x, y = move[0]
            board.checkPromotion(x, y, move[1][0])
            wp, bp = board.getPromote()
            if wp or bp:
                board.setPromote(4)
            board.makeMove(move[0], move[1])
            score = miniMax(board, depth - 1, alpha, beta, True, "white")[1]
            board.undoMove()
            if (score < minScore):
                minScore = score
                best = move
            beta = min(beta, score)
            if (beta <= alpha):
                break
        return best, minScore