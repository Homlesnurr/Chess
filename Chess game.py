import pygame
import sys

from Pieces import *
from HasPiece import *

# Initialize pygame
pygame.init()

# Set the size of the window
size = width, height = 480, 480

# Create the window
screen = pygame.display.set_mode(size)

pieces = []

for x in range(8):
    for y in range(8):
        if x == 0:
            if y == 0 or y == 7:
                a = Rook("Black", y, x)
            if y == 1 or y == 6:
                a = Knight("Black", y, x)
            if y == 2 or y == 5:
                a = Bishop("Black", y, x)
            if y == 3:
                a = Queen("Black", y, x)
            if y == 4:
                a = King("Black", y, x)
        if x == 1:
            a = Pawn("Black", y, x)
        if x == 6:
            a = Pawn("White", y, x)
        if x == 7:
            if y == 0 or y == 7:
                a = Rook("White", y, x)
            if y == 1 or y == 6:
                a = Knight("White", y, x)
            if y == 2 or y == 5:
                a = Bishop("White", y, x)
            if y == 3:
                a = Queen("White", y, x)
            if y == 4:
                a = King("White", y, x)
        pieces.append(a)

# Create a 2D list to represent the chess board
board = [[0 for x in range(8)] for y in range(8)]
# Fill the board with white and black squares
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            board[row][col] = 1
        else:
            board[row][col] = 0
 
# Updates "isMoved" value if it exists
def updateState():
    # Reset passant pieces
    for piece in pieces:
        try:
            if piece.enpassant == True:
                piece.enpassant = False
        except:
            pass
        
    if active_piece.__class__ == Pawn:
        if active_piece.y == active_piece.lastPlacedY + 2 or active_piece.y == active_piece.lastPlacedY - 2:
            active_piece.moved(True)
            active_piece.enpassant = True
        else:
            active_piece.moved(False)
    elif active_piece.__class__ == King:
        active_piece.disableCastle()
                    
# Run the game loop

active_piece = None
turn = 'White'
valid_moves = []
attacking_moves = []
holding = False
sfx1 = pygame.mixer.Sound('sfx/sfx1.ogg')
sfx1.set_volume(0.2)
using_pawn = False

while True:
    for event in pygame.event.get():
        
        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and valid_moves:
            # Get the mouse position
            mouse_pos = event.pos
            
            # Change the x/y screen coordinates to grid coordinates
            column = mouse_pos[0] // (width // 8)
            row = mouse_pos[1] // (height // 8)
            
            if [column, row] in valid_moves and [column, row] not in attacking_moves:
                updateState()
                active_piece.lastPlacedX = column
                active_piece.lastPlacedY = row
                active_piece.x = column
                active_piece.y = row
                active_piece = None
                turn = 'White' if turn == 'Black' else 'Black'
                valid_moves, attacking_moves = [], []
            
            elif [column, row] not in valid_moves and [column, row] not in attacking_moves and has_piece(column, row, pieces, turn) is None:
                active_piece = None
                valid_moves, attacking_moves = [], []
            else:
                # makes active_piece if it is a piece, and if the piece is the correct color
                piece_select = has_piece(column, row, pieces, 'nuthin')
                
                # Make it so you're holding the piece (reset when you release mouse1)
                holding = True if piece_select else False
                
                # Changes active piece if you click on a different piece and it is the correct color, otherwise it stays the same
                if active_piece:
                    active_piece = piece_select if piece_select is not None and piece_select.color == turn else active_piece
                else:
                    active_piece = piece_select if piece_select is not None and piece_select.color == turn else None
                
                # Changes using_pawn to true if the active piece is a pawn
                if active_piece.__class__ == Pawn:
                    using_pawn = True
                else:
                    using_pawn = False
                
                # Reveal available places piece can move 
                if active_piece is not None and active_piece.validMoves(pieces):
                    valid_moves, attacking_moves = active_piece.validMoves(pieces) 
                elif active_piece is not None and not active_piece.validMoves(pieces):
                    valid_moves, attacking_moves = [], []
                else:
                    valid_moves, attacking_moves
        
        # Check for mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN and not valid_moves:
            # Sets holding to true so that the piece can be moved
            holding = True
            
            # Get the mouse position
            mouse_pos = event.pos
            
            # Change the x/y screen coordinates to grid coordinates
            column = mouse_pos[0] // (width // 8)
            row = mouse_pos[1] // (height // 8)
            
            # makes active_piece if it is a piece, and if the piece is the correct color
            piece_select = has_piece(column, row, pieces, 'nuthin')
            active_piece = piece_select if piece_select is not None and piece_select.color == turn else None
            
            # Changes using_pawn to true if the active piece is a pawn
            if active_piece.__class__ == Pawn:
                using_pawn = True
            else:
                using_pawn = False
            
            # Reveal available places piece can move 
            valid_moves, attacking_moves = active_piece.validMoves(pieces) if active_piece is not None and active_piece.validMoves(pieces) else valid_moves, attacking_moves


        # moves the piece when mouse1 is held down
        elif event.type == pygame.MOUSEMOTION and active_piece is not None and holding:
            # Finds the exact x/y coordinates 
            mouse_pos = event.pos
            column = mouse_pos[0] / (width / 8)
            row = mouse_pos[1] / (height / 8)
            
            # Moves active_piece to x/y coordinates
            active_piece.x = column
            active_piece.y = row

        # Places piece on square, and removes the piece already on the square, if it exists AND it is holding a piece
        elif event.type == pygame.MOUSEBUTTONUP and active_piece is not None:
            # Resets holding
            holding = False
            
            # Gets x/y grid position, and makes it "attacked_square"
            mouse_pos = event.pos
            column = mouse_pos[0] // (width // 8)
            row = mouse_pos[1] // (height // 8)
            if [column, row] not in valid_moves and [column, row] not in attacking_moves:
                active_piece.x = active_piece.lastPlacedX
                active_piece.y = active_piece.lastPlacedY
            
            else:
                # Checks if there is a piece on the square
                attacked_square = has_piece(column, row, pieces, turn)
                attacked_Piece = attacked_square if isinstance(attacked_square, Piece) else None
                
                # Removes attacked_Piece if theres a piece of the opposite color
                if attacked_Piece is not None:
                    pieces.remove(attacked_Piece)
                    pygame.mixer.Sound.play(sfx1)
                
                # Checks if pawn is attacking enpassant
                elif active_piece.__class__.__name__ == 'Pawn':
                    for piece in pieces:
                        if piece.__class__.__name__ == 'Pawn' and piece.enpassant == True:
                            if turn == 'White':
                                if piece.x == column and piece.y == row+1:
                                    pieces.remove(piece)
                                    pygame.mixer.Sound.play(sfx1)
                            elif turn == 'Black':
                                if piece.x == column and piece.y == row-1:
                                    pieces.remove(piece)
                                    pygame.mixer.Sound.play(sfx1)                                    
                    
                # Changes active piece location to where mouse1 was released
                active_piece.x = column
                active_piece.y = row
                
                # Next turn if piece is placed in a new position
                if turn == 'White' and (active_piece.x != active_piece.lastPlacedX or active_piece.y != active_piece.lastPlacedY):
                    turn = 'Black'
                    updateState()
                    active_piece.lastPlacedX = active_piece.x
                    active_piece.lastPlacedY = active_piece.y
                    # There is no active_piece anymore, so it is set to None
                    active_piece = None
                elif turn == 'Black' and (active_piece.x != active_piece.lastPlacedX or active_piece.y != active_piece.lastPlacedY):
                    turn = 'White'
                    updateState()
                    active_piece.lastPlacedX = active_piece.x
                    active_piece.lastPlacedY = active_piece.y
                    # There is no active_piece anymore, so it is set to None
                    active_piece = None
                valid_moves, attacking_moves = [], []
                

            
             
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        


    # Draw the chess board
    for row in range(8):
        for col in range(8):
            if board[row][col] == 1:
                color = (238,238,210) # white
            else:
                color = (118,150,86) # black
            pygame.draw.rect(screen, color, (col*60, row*60, 60, 60))

    # Draw pieces on table
    for piece in pieces:
        if active_piece is not None and active_piece is piece and isinstance(piece.x, float) and isinstance(piece.y, float):
            piece.x -= 0.6
            piece.y -= 0.6
            piece.draw(screen)
            piece.x += 0.6
            piece.y += 0.6
        else:
            piece.draw(screen)
    
    # Draw valid moves
    try:
        
        for move in valid_moves:
            # Draws a red circle if there is a piece on the square, and a grey circle if there is not 
            if has_piece(move[0], move[1], pieces, turn):
                pygame.draw.circle(screen, color=(255,0,0), center=(move[0]*60 + 30, move[1]*60 + 30), radius=10, width=3)
                
            else:
                pygame.draw.circle(screen, color=(55,55,55), center=(move[0]*60 + 30, move[1]*60 + 30), radius=10, width=3)
            
            # Draws a red circle if en passant is possible
            if turn == 'White': # turn variable is changed, so turn == 'White' means its checking valid move for black
                # Checks if there is a pawn in the square behind the move, and if the piece being used is a pawn, and if it is en passant
                if has_piece(move[0], move[1]+1, pieces, turn).__class__.__name__ == 'Pawn' and using_pawn and has_piece(move[0], move[1]+1, pieces, turn).enpassant:
                    pygame.draw.circle(screen, color=(255,0,0), center=(move[0]*60 + 30, move[1]*60 + 30), radius=10, width=3)
            
            elif turn == 'Black': # turn variable is changed, so turn == 'Black' means its checking valid move for white
                # Checks if there is a pawn in the square behind the move, and if the piece being used is a pawn, and if it is en passant
                if has_piece(move[0], move[1]-1, pieces, turn).__class__.__name__ == 'Pawn' and using_pawn and has_piece(move[0], move[1]-1, pieces, turn).enpassant:
                    pygame.draw.circle(screen, color=(255,0,0), center=(move[0]*60 + 30, move[1]*60 + 30), radius=10, width=3)
        
    except:
        print('no nuthin here cuh')
        pygame.quit()
    # Update the display
    pygame.display.flip()
