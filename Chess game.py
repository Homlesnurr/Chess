import pygame
import sys
import random

from Pieces import *
from HasPiece import *

# Initialize pygame
pygame.init()

# Set the size of the window
size = width, height = 480, 480

# Create the window
screen = pygame.display.set_mode(size)
seethrough = pygame.display.set_mode(size, pygame.SRCALPHA)

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
        elif x == 1:
            a = Pawn("Black", y, x)           
        elif x == 6:
            a = Pawn("White", y, x)
        elif x == 7:
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
        else:
            continue
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

# Checks for if the game is over:
def checks():
    # Defaults stalemate and checkmate to True, and changes it to False if there is a valid move
                    stalemate = True
                    checkmate = True
                    reportCheck = False
                    
                    # Looks if there are only 2 pieces left
                    if len(pieces) == 2:
                        return 'stalemate'
                    
                    # Checks if king is in check
                    for piece in pieces:
                        # Checks own pieces that have valid moves
                        if piece.color == turn and piece.validMoves(pieces):
                            # Looks through valid moves of own pieces
                            for move in piece.validMoves(pieces):
                                # If there is a king on the valid move, then it is in check
                                if isinstance(has_piece(move[0], move[1], pieces, turn), King):
                                    reportCheck = True
                                    break
                        
                        # Checks if other color has valid moves
                        if piece.color != turn and piece.validMoves(pieces):
                            # If there is a valid move, then it cant be checkmate
                            checkmate = False
                            # If there is not a valid move, then it is stalemate
                            stalemate = False
                        
                        # Checks if it is the last piece
                        if piece == pieces[-1]:
                            # If it is checkmate, then the game ends
                            if checkmate and reportCheck:
                                return 'checkmate'
                    
                            # If it is stalemate, then the game ends
                            elif stalemate and not reportCheck:
                                return 'stalemate'
                            
                            elif reportCheck:
                                return 'check'
                            
                            else:
                                return 'move'
# Run the game loop

active_piece = None
turn = 'White'
valid_moves = []
holding = False

running = True
end = False

stalemate = False
checkmate = False

reportCheck = False
reportCapture = False
reportMove = False

capture = [pygame.mixer.Sound('sfx/capture1.wav'), pygame.mixer.Sound('sfx/capture2.wav')]
castle = [pygame.mixer.Sound('sfx/castle1.wav'), pygame.mixer.Sound('sfx/castle2.wav')]
check = [pygame.mixer.Sound('sfx/check1.wav'), pygame.mixer.Sound('sfx/check2.wav')]
movesound = [pygame.mixer.Sound('sfx/move1.wav'), pygame.mixer.Sound('sfx/move2.wav')]
checkmatesound = pygame.mixer.Sound('sfx/checkmate.wav')
stalematesound = pygame.mixer.Sound('sfx/ough.ogg')


using_pawn = False

while running:
    for event in pygame.event.get():
        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and not end:
            # Sets holding to true so that the piece can be moved
            holding = True
            
            # Get the mouse position
            mouse_pos = event.pos
            
            # Change the x/y screen coordinates to grid coordinates
            column = mouse_pos[0] // (width // 8)
            row = mouse_pos[1] // (height // 8)
            
            # Checks if the piece is a piece
            piece_select = has_piece(column, row, pieces, 'nuthin')
            
            # makes active_piece if it is a piece, and if the piece is the correct color
            # active_piece = piece_select if piece_select is a piece, and piece_select is the correct color
            if isinstance(piece_select, Piece) and piece_select.color == turn:
                active_piece = piece_select  
            # if clicked square is a valid move for the active piece, move the piece
            elif [column, row] in valid_moves and isinstance(active_piece, Piece):
                pass
            else:
                None
            
            
            # Changes using_pawn to true if the active piece is a pawn
            if active_piece.__class__ == Pawn:
                using_pawn = True
            else:
                using_pawn = False
            
            # Reveal available places piece can move 
            if active_piece is not None and active_piece.validMoves(pieces):
                valid_moves = active_piece.validMoves(pieces)  
            elif active_piece is not None and active_piece.validMoves(pieces):
                pass
            else:
                valid_moves = []

        # moves the piece when mouse1 is held down
        elif event.type == pygame.MOUSEMOTION and not end and active_piece is not None and holding:
            # Finds the exact x/y coordinates 
            mouse_pos = event.pos
            column = mouse_pos[0] / (width / 8)
            row = mouse_pos[1] / (height / 8)
            
            # Moves active_piece to x/y coordinates
            active_piece.x = column
            active_piece.y = row

        # Places piece on square, and removes the piece already on the square, if it exists AND it is holding a piece
        elif event.type == pygame.MOUSEBUTTONUP and not end and active_piece is not None:
            # Resets holding
            holding = False
            
            # Gets x/y grid position, and makes it "attacked_square"
            mouse_pos = event.pos
            column = mouse_pos[0] // (width // 8)
            row = mouse_pos[1] // (height // 8)
            
            
            # Checks if where mouse is holding over is in valid_moves
            in_valid_moves = False
            for i in valid_moves:
                if i[0] == column and i[1] == row:
                    in_valid_moves = True
                    break
            
            # Moves piece back to original position if it is not a valid move        
            if in_valid_moves == False and active_piece and has_piece(column, row, pieces, turn) is None:
                active_piece.x = active_piece.lastPlacedX
                active_piece.y = active_piece.lastPlacedY
                active_piece = None
                valid_moves = []
            
            # Moves piece back to original position if it is not a valid move
            elif in_valid_moves == False and isinstance(has_piece(column, row, pieces, 'any'), Piece):
                active_piece.x = active_piece.lastPlacedX
                active_piece.y = active_piece.lastPlacedY
            
            else:
                # Checks if there is a piece on the square
                attacked_square = has_piece(column, row, pieces, turn)
                attacked_Piece = attacked_square if isinstance(attacked_square, Piece) else None
                
                # Removes attacked_Piece if theres a piece of the opposite color
                if isinstance(attacked_Piece, Piece):
                    pieces.remove(attacked_Piece)
                    reportCapture = True
                
                # Checks if pawn is attacking enpassant
                elif active_piece.__class__.__name__ == 'Pawn':
                    for piece in pieces:
                        if piece.__class__.__name__ == 'Pawn' and piece.enpassant == True:
                            if turn == 'White':
                                if piece.x == column and piece.y == row+1:
                                    pieces.remove(piece)
                                    reportCapture = True
                            elif turn == 'Black':
                                if piece.x == column and piece.y == row-1:
                                    pieces.remove(piece)
                                    reportCapture = True                                    
                    
                # Changes active piece location to where mouse1 was released
                active_piece.x = column
                active_piece.y = row
                reportMove = True
                
                
                # Next turn if piece is placed in a new position
                if turn == 'White' and (active_piece.x != active_piece.lastPlacedX or active_piece.y != active_piece.lastPlacedY):
                    active_piece.lastPlacedX = active_piece.x
                    active_piece.lastPlacedY = active_piece.y
                    
                    # Looks for check, checkmate, and stalemate
                    check_state = checks()
                    
                    turn = 'Black'
                    updateState()
                    # There is no active_piece anymore, so it is set to None
                    active_piece = None
                elif turn == 'Black' and (active_piece.x != active_piece.lastPlacedX or active_piece.y != active_piece.lastPlacedY):
                    active_piece.lastPlacedX = active_piece.x
                    active_piece.lastPlacedY = active_piece.y
                    
                    # Looks for check, checkmate, and stalemate
                    check_state = checks()
                            
                    turn = 'White'
                    updateState()
                    # There is no active_piece anymore, so it is set to None
                    active_piece = None
                valid_moves= []
                
                    
                # Plays sounds
                if check_state == 'checkmate':
                    pygame.mixer.Sound.play(checkmatesound)
                    end = True
                elif check_state == 'stalemate':
                    pygame.mixer.Sound('sfx/ough.ogg')
                    end = True
                elif check_state == 'check':
                    pygame.mixer.Sound.play(random.choice(check))
                elif check_state == 'move':
                    pygame.mixer.Sound.play(random.choice(movesound))
                
                reportCheck = False
                reportCapture = False
                reportMove = False
                
                if end:
                    if check_state == 'checkmate':
                        if turn == 'White':
                            print('Black wins!')
                        else:
                            print('White wins!')
                    else:
                        print('You both lose :P')            
             
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
    for move in valid_moves:
        if len(move) == 3:
            pygame.draw.circle(screen, color=(255,0,0), center=(move[0]*60 + 30, move[1]*60 + 30), radius=10, width=3)
        else:
            pygame.draw.circle(screen, color=(55,55,55), center=(move[0]*60 + 30, move[1]*60 + 30), radius=10, width=3)


    pygame.display.flip()
