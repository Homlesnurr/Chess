import pygame

def has_piece(x, y, pieces, color):
    for piece in pieces:
        if int(piece.lastPlacedX) == x and int(piece.lastPlacedY) == y and color != piece.color:
            return piece
        elif int(piece.lastPlacedX) == x and int(piece.lastPlacedY) == y and color == piece.color:
            return False
    return None