from classes import *
from modules import *


#from classes import GamePosition

#Import dependencies:
import pygame #Game library
from pygame.locals import * #For useful variables
import copy #Library used to make exact copies of lists.
import pickle #Library used to store dictionaries in a text file and read them from text files.
import random #Used for making random selections
from collections import defaultdict #Used for giving dictionary values default data types.
from collections import Counter #For counting elements in a list effieciently.
import threading #To allow for AI to think simultaneously while the GUI is coloring the board.
import os #To allow path joining with cross-platform support


# make_move()
# import make_move from Gamal's code
from modules.chess_processing import make_move as makemove

#pos_to_key()
# import pos_to_key from Gamal's code
from modules.chess_processing import pos_to_key as pos2key

# is_check_mate()
# import isCheckmate from Gamal's code
from modules.chess_processing import is_check_mate as isCheckmate


#########MAIN FUNCTION####################################################
#Initialize the board:
board = [ ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'], #8
          ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'], #7
          [  0,    0,    0,    0,    0,    0,    0,    0],  #6
          [  0,    0,    0,    0,    0,    0,    0,    0],  #5
          [  0,    0,    0,    0,    0,    0,    0,    0],  #4
          [  0,    0,    0,    0,    0,    0,    0,    0],  #3
          ['Pw', 'Pw', 'Pw',  'Pw', 'Pw', 'Pw', 'Pw', 'Pw'], #2
          ['Rw', 'Nw', 'Bw',  'Qw', 'Kw', 'Bw', 'Nw', 'Rw'] ]#1
          # a      b     c     d     e     f     g     h

#In chess some data must be stored that is not apparent in the board:
player = 0 #This is the player that makes the next move. 0 is white, 1 is black
castling_rights = [[True, True],[True, True]]
#The above stores whether or not each of the players are permitted to castle on
#either side of the king. (Kingside, Queenside)
En_Passant_Target = -1 #This variable will store a coordinate if there is a square that can be
                       #en passant captured on. Otherwise it stores -1, indicating lack of en passant
                       #targets.
half_move_clock = 0 #This variable stores the number of reversible moves that have been played so far.
#Generate an instance of GamePosition class to store the above data:
position = GamePosition(board,player,castling_rights,En_Passant_Target, half_move_clock)
#Store the piece square tables here so they can be accessed globally by pieceSquareTable() function:
pawn_table = [  0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]
knight_table = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-90,-30,-30,-30,-30,-90,-50]
bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-90,-10,-10,-90,-10,-20]
rook_table = [0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]
queen_table = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, 70, -5,-10,-10,-20]
king_table = [-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20]
king_endgame_table = [-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50]

#Make the GUI:
#Start pygame
pygame.init()
#Load the screen with any arbitrary size for now:
screen = pygame.display.set_mode((600,600))

#Load all the images:
#Load the background chess board image:
background = pygame.image.load(os.path.join('Media', 'board.jpg')).convert()
#Load an image with all the pieces on it:
pieces_image = pygame.image.load(os.path.join('Media', 'Chess_Pieces_Sprite.png')).convert_alpha()
circle_image_green = pygame.image.load(os.path.join('Media', 'green_circle_small.png')).convert_alpha()
circle_image_capture = pygame.image.load(os.path.join('Media', 'green_circle_neg.png')).convert_alpha()
circle_image_red = pygame.image.load(os.path.join('Media', 'red_circle_big.png')).convert_alpha()
greenbox_image = pygame.image.load(os.path.join('Media', 'green_box.png')).convert_alpha()
circle_image_yellow = pygame.image.load(os.path.join('Media', 'yellow_circle_big.png')).convert_alpha()
circle_image_green_big = pygame.image.load(os.path.join('Media', 'green_circle_big.png')).convert_alpha()
yellowbox_image = pygame.image.load(os.path.join('Media', 'yellow_box.png')).convert_alpha()
#Menu pictures:
withfriend_pic = pygame.image.load(os.path.join('Media', 'withfriend.png')).convert_alpha()
withAI_pic = pygame.image.load(os.path.join('Media', 'withAI.png')).convert_alpha()
playwhite_pic = pygame.image.load(os.path.join('Media', 'playWhite.png')).convert_alpha()
playblack_pic = pygame.image.load(os.path.join('Media', 'playBlack.png')).convert_alpha()
flipEnabled_pic = pygame.image.load(os.path.join('Media', 'flipEnabled.png')).convert_alpha()
flipDisabled_pic = pygame.image.load(os.path.join('Media', 'flipDisabled.png')).convert_alpha()

#Getting sizes:
#Get background size:
size_of_bg = background.get_rect().size
#Get size of the individual squares
square_width =int( size_of_bg[0]/8)
square_height = int(size_of_bg[1]/8)


#Rescale the images so that each piece can fit in a square:
pieces_image = pygame.transform.scale(pieces_image,
                                      (square_width*6,square_height*2))
circle_image_green = pygame.transform.scale(circle_image_green,
                                      (square_width, square_height))
circle_image_capture = pygame.transform.scale(circle_image_capture,
                                      (square_width, square_height))
circle_image_red = pygame.transform.scale(circle_image_red,
                                      (square_width, square_height))
greenbox_image = pygame.transform.scale(greenbox_image,
                                      (square_width, square_height))
yellowbox_image = pygame.transform.scale(yellowbox_image,
                                      (square_width, square_height))
circle_image_yellow = pygame.transform.scale(circle_image_yellow,
                                             (square_width, square_height))
circle_image_green_big = pygame.transform.scale(circle_image_green_big,
                                             (square_width, square_height))
withfriend_pic = pygame.transform.scale(withfriend_pic,
                                      (square_width*4,square_height*4))
withAI_pic = pygame.transform.scale(withAI_pic,
                                      (square_width*4,square_height*4))
playwhite_pic = pygame.transform.scale(playwhite_pic,
                                      (square_width*4,square_height*4))
playblack_pic = pygame.transform.scale(playblack_pic,
                                      (square_width*4,square_height*4))
flipEnabled_pic = pygame.transform.scale(flipEnabled_pic,
                                      (square_width*4,square_height*4))
flipDisabled_pic = pygame.transform.scale(flipDisabled_pic,
                                      (square_width*4,square_height*4))



#Make a window of the same size as the background, set its title, and
#load the background image onto it (the board):
screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Shallow Green')
screen.blit(background,(0,0))

#Generate a list of pieces that should be drawn on the board:
listofWhitePieces,listofBlackPieces = createPieces(board)
#(the list contains references to objects of the class Piece)
#Initialize a list of shades:
listofShades = []

clock = pygame.time.Clock() #Helps controlling fps of the game.
isDown = False #Variable that shows if the mouse is being held down
               #onto a piece
isClicked = False #To keep track of whether a piece was clicked in order
#to indicate intention to move by the user.
isTransition = False #Keeps track of whether or not a piece is being animated.
isDraw = False #Will store True if the game ended with a draw
chessEnded = False #Will become True once the chess game ends by checkmate, stalemate, etc.
isRecord = False #Set this to True if you want to record moves to the Opening Book. Do not
#set this to True unless you're 100% sure of what you're doing. The program will never modify
#this value.
isAIThink = False #Stores whether or not the AI is calculating the best move to be played.
# Initialize the opening book dictionary, and set its values to be lists by default:
openings = defaultdict(list)
#If openingTable.txt exists, read from it and load the opening moves to the local dictionary.
#If it doesn't, create a new one to write to if Recording is enabled:
try:
    file_handle = open('openingTable.txt', 'r+')
    openings = pickle.loads(file_handle.read())
except:
    if isRecord:
        file_handle = open('openingTable.txt', 'w')

searched = {} #Global variable that allows negamax to keep track of nodes that have
#already been evaluated.
prevMove = [-1,-1,-1,-1] #Also a global varible that stores the last move played, to
#allow drawBoard() to create Shades on the squares.
#Initialize some more values:
#For animating AI thinking graphics:
ax,ay=0,0
numm = 0
#For showing the menu and keeping track of user choices:
isMenu = True
isAI = -1
isFlip = -1
AIPlayer = -1
#Finally, a variable to keep false until the user wants to quit:
gameEnded = False
#########################INFINITE LOOP#####################################
#The program remains in this loop until the user quits the application
while not gameEnded:
    if isMenu:
        #Menu needs to be shown right now.
        #Blit the background:
        screen.blit(background,(0,0))
        if isAI==-1:
            #The user has not selected between playing against the AI
            #or playing against a friend.
            #So allow them to choose between playing with a friend or the AI:
            screen.blit(withfriend_pic,(0,square_height*2))
            screen.blit(withAI_pic,(square_width*4,square_height*2))
        elif isAI==True:
            #The user has selected to play against the AI.
            #Allow the user to play as white or black:
            screen.blit(playwhite_pic,(0,square_height*2))
            screen.blit(playblack_pic,(square_width*4,square_height*2))
        elif isAI==False:
            #The user has selected to play with a friend.
            #Allow choice of flipping the board or not flipping the board:
            screen.blit(flipDisabled_pic,(0,square_height*2))
            screen.blit(flipEnabled_pic,(square_width*4,square_height*2))
        if isFlip!=-1:
            #All settings have already been specified.
            #Draw all the pieces onto the board:
            drawBoard()
            #Don't let the menu ever appear again:
            isMenu = False
            #In case the player chose to play against the AI and decided to
            #play as black, call upon the AI to make a move:
            if isAI and AIPlayer==0:
                colorsign=1
                bestMoveReturn = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,colorsign,bestMoveReturn))
                move_thread.start()
                isAIThink = True
            continue
        for event in pygame.event.get():
            #Handle the events while in menu:
            if event.type==QUIT:
                #Window was closed.
                gameEnded = True
                break
            if event.type == MOUSEBUTTONUP:
                #The mouse was clicked somewhere.
                #Get the coordinates of click:
                pos = pygame.mouse.get_pos()
                #Determine if left box was clicked or right box.
                #Then choose an appropriate action based on current
                #state of menu:
                if (pos[0]<square_width*4 and
                pos[1]>square_height*2 and
                pos[1]<square_height*6):
                    #LEFT SIDE CLICKED
                    if isAI == -1:
                        isAI = False
                    elif isAI==True:
                        AIPlayer = 1
                        isFlip = False
                    elif isAI==False:
                        isFlip = False
                elif (pos[0]>square_width*4 and
                pos[1]>square_height*2 and
                pos[1]<square_height*6):
                    #RIGHT SIDE CLICKED
                    if isAI == -1:
                        isAI = True
                    elif isAI==True:
                        AIPlayer = 0
                        isFlip = False
                    elif isAI==False:
                        isFlip=True

        #Update the display:
        pygame.display.update()

        #Run at specific fps:
        clock.tick(60)
        continue
    #Menu part was done if this part reached.
    #If the AI is currently thinking the move to play
    #next, show some fancy looking squares to indicate
    #that.
    #Do it every 6 frames so it's not too fast:
    numm+=1
    if isAIThink and numm%6==0:
        ax+=1
        if ax==8:
            ay+=1
            ax=0
        if ay==8:
            ax,ay=0,0
        if ax%4==0:
            createShades([])
        #If the AI is white, start from the opposite side (since the board is flipped)
        if AIPlayer==0:
            listofShades.append(Shades(greenbox_image,(7-ax,7-ay)))
        else:
            listofShades.append(Shades(greenbox_image,(ax,ay)))

    for event in pygame.event.get():
        #Deal with all the user inputs:
        if event.type==QUIT:
            #Window was closed.
            gameEnded = True

            break
        #Under the following conditions, user input should be
        #completely ignored:
        if chessEnded or isTransition or isAIThink:
            continue
        #isDown means a piece is being dragged.
        if not isDown and event.type == MOUSEBUTTONDOWN:
            #Mouse was pressed down.
            #Get the oordinates of the mouse
            pos = pygame.mouse.get_pos()
            #convert to chess coordinates:
            chess_coord = pixel_coord_to_chess(pos)
            chess_coord=(int(chess_coord[0]),int(chess_coord[1]))

            x =chess_coord[0]
            y = chess_coord[1]

            #If the piece clicked on is not occupied by your own piece,
            #ignore this mouse click:
            if not isOccupiedby(board,x,y,'wb'[player]):
                continue
            #Now we're sure the user is holding their mouse on a
            #piecec that is theirs.
            #Get reference to the piece that should be dragged around or selected:
            dragPiece = getPiece(chess_coord)
            print(dragPiece)
            #Find the possible squares that this piece could attack:
            listofTuples = findPossibleSquares(position,x,y)
            #Highlight all such squares:
            createShades(listofTuples)
            #A green box should appear on the square which was selected, unless
            #it's a king under check, in which case it shouldn't because the king
            #has a red color on it in that case.
            if ((dragPiece.pieceinfo[0]=='K') and
                (isCheck(position,'white') or isCheck(position,'black'))):
                None
            else:
                listofShades.append(Shades(greenbox_image,(x,y)))
            #A piece is being dragged:
            isDown = True
        if (isDown or isClicked) and event.type == MOUSEBUTTONUP:
            #Mouse was released.
            isDown = False
            #Snap the piece back to its coordinate position
            dragPiece.setpos((-1,-1))
            #Get coordinates and convert them:
            pos = pygame.mouse.get_pos()
            chess_coord = pixel_coord_to_chess(pos)
            chess_coord = (int(chess_coord[0]), int(chess_coord[1]))
            x2 = chess_coord[0]
            y2 = chess_coord[1]
            #Initialize:
            isTransition = False
            if (x,y)==(x2,y2): #NO dragging occured
                #(ie the mouse was held and released on the same square)
                if not isClicked: #nothing had been clicked previously
                    #This is the first click
                    isClicked = True
                    prevPos = (x,y) #Store it so next time we know the origin
                else: #Something had been clicked previously
                    #Find out location of previous click:
                    x,y = prevPos
                    if (x,y)==(x2,y2): #User clicked on the same square again.
                        #So
                        isClicked = False
                        #Destroy all shades:
                        createShades([])
                    else:
                        #User clicked elsewhere on this second click:
                        if isOccupiedby(board,x2,y2,'wb'[player]):
                            #User clicked on a square that is occupied by their
                            #own piece.
                            #This is like making a first click on your own piece:
                            isClicked = True
                            prevPos = (x2,y2) #Store it
                        else:
                            #The user may or may not have clicked on a valid target square.
                            isClicked = False
                            #Destory all shades
                            createShades([])
                            isTransition = True #Possibly if the move was valid.


            if not (x2,y2) in listofTuples:
                #Move was invalid
                isTransition = False
                continue
            #Reaching here means a valid move was selected.
            #If the recording option was selected, store the move to the opening dictionary:
            if isRecord:
                key = pos2key(position)
                #Make sure it isn't already in there:
                if [(x,y),(x2,y2)] not in openings[key]:
                    openings[key].append([(x,y),(x2,y2)])

            #Make the move:
            makemove(position,x,y,x2,y2)
            #Update this move to be the 'previous' move (latest move in fact), so that
            #yellow shades can be shown on it.
            prevMove = [x,y,x2,y2]
            #Update which player is next to play:
            player = position.getplayer()
            #Add the new position to the history for it:
            position.addtoHistory(position)
            #Check for possibilty of draw:
            HMC = position.getHMC()
            if HMC>=100 or isStalemate(position) or position.checkRepition():
                #There is a draw:
                isDraw = True
                chessEnded = True
            #Check for possibilty of checkmate:
            if isCheckmate(position,'white'):
                winner = 'b'
                chessEnded = True
            if isCheckmate(position,'black'):
                winner = 'w'
                chessEnded = True
            #If the AI option was selecteed and the game still hasn't finished,
            #let the AI start thinking about its next move:
            if isAI and not chessEnded:
                if player==0:
                    colorsign = 1
                else:
                    colorsign = -1
                bestMoveReturn = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,colorsign,bestMoveReturn))
                move_thread.start()
                isAIThink = True
            #Move the piece to its new destination:
            dragPiece.setcoord((x2,y2))
            #There may have been a capture, so the piece list should be regenerated.
            #However, if animation is ocurring, the the captured piece should still remain visible.
            if not isTransition:
                listofWhitePieces,listofBlackPieces = createPieces(board)
            else:
                movingPiece = dragPiece
                origin = chess_coord_to_pixels((x,y))
                destiny = chess_coord_to_pixels((x2,y2))
                movingPiece.setpos(origin)
                step = (destiny[0]-origin[0],destiny[1]-origin[1])

            #Either way shades should be deleted now:
            createShades([])
    #If an animation is supposed to happen, make it happen:
    if isTransition:
        p,q = movingPiece.getpos()
        dx2,dy2 = destiny
        n= 30.0
        if abs(p-dx2)<=abs(step[0]/n) and abs(q-dy2)<=abs(step[1]/n):
            #The moving piece has reached its destination:
            #Snap it back to its grid position:
            movingPiece.setpos((-1,-1))
            #Generate new piece list in case one got captured:
            listofWhitePieces,listofBlackPieces = createPieces(board)
            #No more transitioning:
            isTransition = False
            createShades([])
        else:
            #Move it closer to its destination.
            movingPiece.setpos((p+step[0]/n,q+step[1]/n))
    #If a piece is being dragged let the dragging piece follow the mouse:
    if isDown:
        m,k = pygame.mouse.get_pos()
        dragPiece.setpos((m-square_width/2,k-square_height/2))
    #If the AI is thinking, make sure to check if it isn't done thinking yet.
    #Also, if a piece is currently being animated don't ask the AI if it's
    #done thining, in case it replied in the affirmative and starts moving
    #at the same time as your piece is moving:
    if isAIThink and not isTransition:
        if not move_thread.isAlive():
            #The AI has made a decision.
            #It's no longer thinking
            isAIThink = False
            #Destroy any shades:
            createShades([])
            #Get the move proposed:
            [x,y],[x2,y2] = bestMoveReturn
            #Do everything just as if the user made a move by click-click movement:
            makemove(position,x,y,x2,y2)
            prevMove = [x,y,x2,y2]
            player = position.getplayer()
            HMC = position.getHMC()
            position.addtoHistory(position)
            if HMC>=100 or isStalemate(position) or position.checkRepition():
                isDraw = True
                chessEnded = True
            if isCheckmate(position,'white'):
                winner = 'b'
                chessEnded = True
            if isCheckmate(position,'black'):
                winner = 'w'
                chessEnded = True
            #Animate the movement:
            isTransition = True
            movingPiece = getPiece((x,y))
            origin = chess_coord_to_pixels((x,y))
            destiny = chess_coord_to_pixels((x2,y2))
            movingPiece.setpos(origin)
            step = (destiny[0]-origin[0],destiny[1]-origin[1])

    #Update positions of all images:
    drawBoard()
    #Update the display:
    pygame.display.update()

    #Run at specific fps:
    clock.tick(60)

#Out of loop. Quit pygame:
pygame.quit()
#In case recording mode was on, save the openings dictionary to a file:
if isRecord:
    file_handle.seek(0)
    pickle.dump(openings,file_handle)
    file_handle.truncate()
    file_handle.close()
