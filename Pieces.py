import pygame
from HasPiece import *

class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.lastPlacedX = x
        self.lastPlacedY = y
    
    def draw(self, screen):
        screen.blit(self.image, (self.x*60, self.y*60))
    
    # Checks if piece is on the baord
    def inBoard(self, x, y):
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            return True
        else:
            return False


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.image = pygame.image.load("icons/Rook " + self.color + ".png")

    def validMoves(self, pieces):
        # Initiate default values
        moves = []
        x = self.x
        y = self.y
        right = True
        down = True
        left = True
        up = True
        # dx and dy are the moves the queen can make
        max_range = [x for x in range(1,8)]

        for move in max_range:
            # Checks if rook can move right, and if there is a piece on move, whether or not it should add it to the list
            if right and self.inBoard(x+move,y) and has_piece(x+move,y,pieces,self.color) is None:
                moves.append([x+right,y])
                
            elif right and self.inBoard(x+move,y) and has_piece(x+move,y,pieces,self.color) is not None:
                if isinstance(has_piece(x+move,y,pieces,self.color), Piece):
                    moves.append([x+move,y,'Attack'])
                right = False
                
            else:
                right = False
                
                
            # same logic applies on all other directions
                
                
            if down and self.inBoard(x,y+move) and has_piece(x,y+move,pieces,self.color) is None:
                moves.append([x,y+move])
                
            elif down and self.inBoard(x,y+move) and has_piece(x,y+move,pieces,self.color) is not None:
                if isinstance(has_piece(x,y+move,pieces,self.color), Piece):
                    moves.append([x,y+move,'Attack'])
                down = False
                
            else:
                down = False
                
                
            if left and self.inBoard(x-move,y) and has_piece(x-move,y,pieces,self.color) is None:
                moves.append([x-move,y])
                
            elif left and self.inBoard(x-move,y) and has_piece(x-move,y,pieces,self.color) is not None:
                if isinstance(has_piece(x-move,y,pieces,self.color), Piece):
                    moves.append([x-move,y,'Attack'])
                left = False
                
            else:
                left = False
                
                
            if up and self.inBoard(x,y-move) and has_piece(x,y-move,pieces,self.color) is None:
                moves.append([x,y-up])
                
            elif up and self.inBoard(x,y-move) and has_piece(x,y-move,pieces,self.color) is not None:
                if isinstance(has_piece(x,y-move,pieces,self.color), Piece):
                    moves.append([x,y-move,'Attack'])
                up = False
                
            else:
                up = False    
        return moves
    
class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.image = pygame.image.load("icons/Bishop " + self.color + ".png")

    def validMoves(self, pieces):
        # Initiate default values
        moves = []
        x = self.x
        y = self.y
        rightUp = True
        rightDown = True
        leftUp = True
        leftDown = True
        # dx and dy are the moves the queen can make
        max_range = [x for x in range(1,8)]

        for move in max_range:
            # Checks if bishop can move up and to the right, and if there is a piece on move, whether or not it should add it to the list
            if rightUp and self.inBoard(x+move, y-move) and has_piece(x+move, y-move, pieces, self.color) is None:
                moves.append([x+move, y-move])
            
            elif rightUp and self.inBoard(x+move, y-move) and has_piece(x+move, y-move, pieces, self.color) is not None:
                if isinstance(has_piece(x+move, y-move, pieces, self.color), Piece):
                    moves.append([x+move, y-move, 'Attack'])
                rightUp = False
            else:
                rightUp = False
            
            
            # same logic applies on all other directions
            
            
            if rightDown and self.inBoard(x+move, y+move) and has_piece(x+move, y+move, pieces, self.color) is None:
                moves.append([x+move, y+move])
            
            elif rightDown and self.inBoard(x+move, y+move) and has_piece(x+move, y+move, pieces, self.color) is not None:
                if isinstance(has_piece(x+move, y+move, pieces, self.color), Piece):
                    moves.append([x+move, y+move, 'Attack'])
                rightDown = False
            
            else:
                rightDown = False
                
                
            if leftUp and self.inBoard(x-move, y-move) and has_piece(x-move, y-move, pieces, self.color) is None:
                moves.append([x-move, y-move])
                
            elif leftUp and self.inBoard(x-move, y-move) and has_piece(x-move, y-move, pieces, self.color) is not None:
                if isinstance(has_piece(x-move, y-move, pieces, self.color), Piece):
                    moves.append([x-move, y-move, 'Attack'])
                leftUp = False
                
            else:
                leftUp = False
                
                
            if leftDown and self.inBoard(x-move, y+move) and has_piece(x-move, y+move, pieces, self.color) is None:
                moves.append([x-move, y+move])
                
            elif leftDown and self.inBoard(x-move, y+move) and has_piece(x-move, y+move, pieces, self.color) is not None:
                if isinstance(has_piece(x-move, y+move, pieces, self.color), Piece):
                    moves.append([x-move, y+move, 'Attack'])
                leftDown = False
            
            else:
                leftDown = False
        return moves

class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.image = pygame.image.load("icons/Knight " + self.color + ".png")

    def validMoves(self, pieces):
        # Initiate default values
        moves = []
        moves = []
        x = self.x
        y = self.y
        
        # dx1 and dy1 are the first set of moves
        dx1 = [-1,1]
        dy1 = [-2,2]
        
        # dx2 and dy2 are the second set of moves
        dx2 = [-2,2]
        dy2 = [-1,1]
        
        # Looks for where knight can move
        for moveX in dx1:
            for moveY in dy1:
                if self.inBoard(x + moveX, y + moveY) and has_piece(x + moveX, y + moveY, pieces, self.color) == None:
                    moves.append([x + moveX, y + moveY])
                elif self.inBoard(x + moveX, y + moveY) and has_piece(x + moveX, y + moveY, pieces, self.color):
                    moves.append([x + moveX, y + moveY, 'Attack'])
                else:
                    pass
                
        for moveX in dx2:
            for moveY in dy2:
                if self.inBoard(x + moveX, y + moveY) and has_piece(x + moveX, y + moveY, pieces, self.color) == None:
                    moves.append([x + moveX, y + moveY])
                elif self.inBoard(x + moveX, y + moveY) and has_piece(x + moveX, y + moveY, pieces, self.color):
                    moves.append([x + moveX, y + moveY, 'Attack'])
                else:
                    pass
           
        return moves

class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.image = pygame.image.load("icons/Queen " + self.color + ".png")

    def validMoves(self, pieces):
        # Initiate default values
        moves = []
        x = self.x
        y = self.y
        right = True
        left = True
        up = True
        down = True
        rightUp = True
        rightDown = True
        leftUp = True
        leftDown = True
        # dx and dy are the moves the queen can make
        max_range = [x for x in range(1,8)]
        
        for move in max_range:
            # Checks there is no piece on move
            if right and self.inBoard(x+move, y) and has_piece(x+move, y, pieces, self.color) is None:
                moves.append([x+move, y])
            # Checks if there is a piece on move, and if it is an enemy piece
            elif right and self.inBoard(x+move, y) and has_piece(x+move, y, pieces, self.color) is not None:
                if isinstance(has_piece(x+move, y, pieces, self.color), Piece):
                    moves.append([x+move, y, 'Attack'])
                right = False
            
            else:
                right = False    
            
            
            # same logic for all other directions
            
            
            if rightDown and self.inBoard(x+move, y+move) and has_piece(x+move, y+move, pieces, self.color) is None:
                moves.append([x+move, y+move])
            
            elif rightDown and self.inBoard(x+move, y+move) and has_piece(x+move, y+move, pieces, self.color) is not None:
                if isinstance(has_piece(x+move, y+move, pieces, self.color), Piece):
                    moves.append([x+move, y+move, 'Attack'])
                rightDown = False
            
            else:
                rightDown = False    
            
            
            if down and self.inBoard(x, y+move) and has_piece(x, y+move, pieces, self.color) is None:
                moves.append([x, y+move])
            
            elif down and self.inBoard(x, y+move) and has_piece(x, y+move, pieces, self.color) is not None:
                if isinstance(has_piece(x, y+move, pieces, self.color), Piece):
                    moves.append([x, y+move, 'Attack'])
                down = False
            
            else:
                down = False
             
                
            if leftDown and self.inBoard(x-move, y+move) and has_piece(x-move, y+move, pieces, self.color) is None:
                moves.append([x-move, y+move])
            
            elif leftDown and self.inBoard(x-move, y+move) and has_piece(x-move, y+move, pieces, self.color) is not None:    
                if isinstance(has_piece(x-move, y+move, pieces, self.color), Piece):
                    moves.append([x-move, y+move, 'Attack'])
                leftDown = False
            
            else:
                leftDown = False
             
                
            if left and self.inBoard(x-move, y) and has_piece(x-move, y, pieces, self.color) is None:
                moves.append([x-move, y])
            
            
            elif left and self.inBoard(x-move, y) and has_piece(x-move, y, pieces, self.color) is not None:
                if isinstance(has_piece(x-move, y, pieces, self.color), Piece):
                    moves.append([x-move, y, 'Attack'])
                left = False
            
            else:
                left = False
            
            
            if leftUp and self.inBoard(x-move, y-move) and has_piece(x-move, y-move, pieces, self.color) is None:
                moves.append([x-move, y-move])
            
            elif leftUp and self.inBoard(x-move, y-move) and has_piece(x-move, y-move, pieces, self.color) is not None:
                if isinstance(has_piece(x-move, y-move, pieces, self.color), Piece):
                    moves.append([x-move, y-move, 'Attack'])
                leftUp = False
            
            else:
                leftUp = False
                
                
            if up and self.inBoard(x, y-move) and has_piece(x, y-move, pieces, self.color) is None:
                moves.append([x, y-move])
            
            elif up and self.inBoard(x, y-move) and has_piece(x, y-move, pieces, self.color) is not None:
                if isinstance(has_piece(x, y-move, pieces, self.color), Piece):
                    moves.append([x, y-move, 'Attack'])
                up = False
            
            else:
                up = False
        
        
            if rightUp and self.inBoard(x+move, y-move) and has_piece(x+move, y-move, pieces, self.color) is None:
                moves.append([x+move, y-move])
                
            elif rightUp and self.inBoard(x+move, y-move) and has_piece(x+move, y-move, pieces, self.color) is not None:
                if isinstance(has_piece(x+move, y-move, pieces, self.color), Piece):
                    moves.append([x+move, y-move, 'Attack'])
                rightUp = False
            
            else:
                rightUp = False
        
        return moves
            

class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.image = pygame.image.load("icons/King " + self.color + ".png")
        self.castle = True
    
    def validMoves(self, pieces):
        # Initiate default values
        moves = []
        moves = []
        x = self.x
        y = self.y
        
        # dx and dy are the moves the king can make
        dx = [-1, 0, 1]
        dy = [-1, 0, 1]
        
        # Looks for where king can move
        for moveX in dx:
            for moveY in dy:
                if self.inBoard(x + moveX, y + moveY) and has_piece(x + moveX, y + moveY, pieces, self.color) == None:
                    moves.append([x + moveX, y + moveY])
                elif self.inBoard(x + moveX, y + moveY) and has_piece(x + moveX, y + moveY, pieces, self.color):
                    moves.append([x + moveX, y + moveY, 'Attack'])
                else:
                    pass
        return moves
    
    def disableCastle(self):
        self.castle = False

class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.image = pygame.image.load("icons/Pawn " + self.color + ".png")
        self.isMoved = False
        self.enpassant = False
    
    def validMoves(self, pieces):
        # Initiate default values
        moves = []
        x = self.x
        y = self.y
        dy = 0
        
        # attack is where the Pawn can attack pieces
        attack = [-1, 1]
        for possible in attack:         
            # Check if there is peice diagonally
            if self.inBoard(x+possible, y-1) and has_piece(x+possible, y-1, pieces, self.color) and self.color == 'White':
                moves.append([x+possible, y-1, 'Attack'])
            elif self.inBoard(x+possible, y+1) and has_piece(x+possible, y+1, pieces, self.color) and self.color == 'Black':
                moves.append([x+possible, y+1, 'Attack'])
            
            # Checks for en passant
            pos_piece = has_piece(x+possible, y, pieces, self.color)
            if self.inBoard(x+possible, y) and pos_piece and pos_piece.__class__.__name__ == 'Pawn' and pos_piece.enpassant == True:
                if self.color == 'White':
                    moves.append([x+possible, y-1, 'Attack'])
                else:
                    moves.append([x+possible, y+1, 'Attack'])

        
        # First move if pawn is White
        if self.isMoved == False and self.color == 'White':            
            # Checks if each square in front of pawn is not occupied
            while self.inBoard(x, y-1+dy) and has_piece(x, y-1+dy, pieces, 'any') == None and dy > -2:
                dy -= 1
                moves.append([x, y+dy])
            
            # Returns possible moves
            return moves
                
        # Black variation
        elif self.isMoved == False and self.color == 'Black':            
            while self.inBoard(x, y+1+dy) and has_piece(x, y+1+dy, pieces, 'any') == None and dy < 2:
                dy += 1
                moves.append([x, y+dy])
            return moves
        
       
        # Possible moves after Pawn is moved
        elif self.color == 'White':
            # Checks if Pawn can move one forward
            if has_piece(x, y-1, pieces, self.color) == None:
                moves.append([x, y-1])
            
            # Returns possible moves
            return moves
        # Black variation
        elif self.color == 'Black':
            if has_piece(x, y+1, pieces, self.color) == None:
                moves.append([x, y+1])
            return moves

    def moved(self, double):
        self.isMoved = True
        if double == True:
            self.enpassant = True
        else:
            self.enpassant = False