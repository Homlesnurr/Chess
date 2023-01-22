import pygame

def has_piece(x, y, pieces, color):
    for piece in pieces:
        if int(piece.x) == x and int(piece.y) == y and color != piece.color:
            return piece
    return None