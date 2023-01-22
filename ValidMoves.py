import pygame


def validMoves(type, piece, color, pieces):
    if type == "Pawn":
        print('Pawn selected')
        if piece.isMoved == False:
            print('Pawn is not moved')
    
    elif type == "Bishop":
        pass
    
    elif type == "Knight":
        pass
    
    elif type == "Rook":
        pass
    
    elif type == "Queen":
        pass
    
    elif type == "King":
        print('King selected')
        if piece.castle == False:
            print('King can\'t Castle')