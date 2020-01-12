from classes import *
from modules import chess_ai, chess_processing, GUI



from classes.GamePosition import GamePosition
from classes.Piece import Piece
from classes.Shades import Shades
#from classes import GamePosition

#Import dependencies:
import pygame #Game library
from pygame.locals import * #For useful variables
import copy #Library used to make exact copies of lists.
import pickle #Library used to store dictionaries in a text file and read them from text files.
import random #Used for making random selections
from collections import defaultdict #Used for giving dictionary values default data types.
from collections import Counter #For counting elements in a list effieciently.
import threading #To allow for AI to think simultaneously while the GUI is coloring the chess_board.
import os #To allow path joining with cross-platform support


# make_move()
# import make_move from Gamal's code
#from modules.chess_processing import make_move as makemove

#pos_to_key()
# import pos_to_key from Gamal's code
#from modules.chess_processing import pos_to_key as pos2key

# is_check_mate()
# import is_check_mate from Gamal's code
#from modules.chess_processing import is_check_mate as is_check_mate

from modules.chess_processing import *
from modules.chess_ai import *




##############################////////GUI FUNCTIONS\\\\\\\\\\\\\#############################
def chess_coord_to_pixels(chess_coord):
    x,y = chess_coord

    if is_ai:
        if ai_player==0:
            return ((7-x)*square_width, (7-y)*square_height)
        else:
            return (x*square_width, y*square_height)

def pixel_coord_to_chess(pixel_coord):
    x,y = pixel_coord[0]/square_width, pixel_coord[1]/square_height

    if is_ai:
        if ai_player==0:
            return (7-x,7-y)
        else:
            return (x,y)

def get_piece(chess_coord):
    for piece in list_of_white_pieces+list_of_black_pieces:
        #piece.getInfo()[0] represents the chess coordinate occupied
        #by piece.
        if piece.getInfo()[0] == chess_coord:
            return piece
def create_pieces(chess_board):
    list_of_white_pieces = []
    list_of_black_pieces = []
    for i in range(8):
        for k in range(8):
            if chess_board[i][k]!=0:
                p = Piece.Piece(chess_board[i][k],(k,i),square_width,square_height)
                if chess_board[i][k][1]=='w':
                    list_of_white_pieces.append(p)
                else:
                    list_of_black_pieces.append(p)
    return [list_of_white_pieces,list_of_black_pieces]
def createShades(listofTuples):
    global list_of_shades
    #Empty the list
    list_of_shades = []
    if isTransition:
        #Nothing should be shaded when a piece is being animated:
        return
    if is_draw:
        #The game ended with a draw. Make yellow circle shades for
        #both the kings to show this is the case:
        coord = look_for(chess_board,'Kw')[0]
        shade = Shades.Shades(circle_image_yellow,coord)
        list_of_shades.append(shade)
        coord = look_for(chess_board,'Kb')[0]
        shade = Shades.Shades(circle_image_yellow,coord)
        list_of_shades.append(shade)
        #There is no need to go further:
        return
    if chessEnded:
        #The game has ended, with a checkmate because it cannot be a
        #draw if the code reached here.
        #Give the winning king a green circle shade:
        coord = look_for(chess_board,'K'+winner)[0]
        shade = Shades.Shades(circle_image_green_big,coord)
        list_of_shades.append(shade)
    #If either king is under attack, give them a red circle:
    if is_check(position,'white'):
        coord = look_for(chess_board,'Kw')[0]
        shade = Shades.Shades(circle_image_red,coord)
        list_of_shades.append(shade)
    if is_check(position,'black'):
        coord = look_for(chess_board,'Kb')[0]
        shade = Shades.Shades(circle_image_red,coord)
        list_of_shades.append(shade)
    #Go through all the target squares inputted:
    for pos in listofTuples:
        #If the target square is occupied, it can be captured.
        #For a capturable square, there is a different shade.
        #Create the appropriate shade for each target square:
        if is_occupied(chess_board,pos[0],pos[1]):
            img = circle_image_capture
        else:
            img = circle_image_green
        shade = Shades.Shades(img,pos)
        #Append:
        list_of_shades.append(shade)
def drawchess_board():
    #Blit the background:
    screen.blit(background,(0,0))
    #Choose the order in which to blit the pieces.
    #If black is about to play for example, white pieces
    #should be blitted first, so that when black is capturing,
    #the piece appears above:
    if player==1:
        order = [list_of_white_pieces,list_of_black_pieces]
    else:
        order = [list_of_black_pieces,list_of_white_pieces]
    if isTransition:
        #If a piece is being animated, the player info is changed despite
        #white still capturing over black, for example. Reverse the order:
        order = list(reversed(order))
    #The shades which appear during the following three conditions need to be
    #blitted first to appear under the pieces:
    if is_draw or chessEnded or is_aiThink:
        #Shades
        for shade in list_of_shades:
            img,chess_coord = shade.getInfo()
            pixel_coord = chess_coord_to_pixels(chess_coord)
            screen.blit(img,pixel_coord)
    #Make shades to show what the previous move played was:
    if prevMove[0]!=-1 and not isTransition:
        x,y,x2,y2 = prevMove
        screen.blit(yellowbox_image,chess_coord_to_pixels((x,y)))
        screen.blit(yellowbox_image,chess_coord_to_pixels((x2,y2)))

    #Blit the Pieces:
    #Notw that one side has to be below the green circular shades to show
    #that they are being targeted, and the other side if dragged to such
    # a square should be blitted on top to show that it is capturing:

    #Potentially captured pieces:
    for piece in order[0]:

        chess_coord,subsection,pos = piece.getInfo()
        pixel_coord = chess_coord_to_pixels(chess_coord)
        if pos==(-1,-1):
            #Blit to default square:
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            #Blit to the specific coordinates:
            screen.blit(pieces_image,pos,subsection)
    #Blit the shades in between:
    if not (is_draw or chessEnded or is_aiThink):
        for shade in list_of_shades:
            img,chess_coord = shade.getInfo()
            pixel_coord = chess_coord_to_pixels(chess_coord)
            screen.blit(img,pixel_coord)
    #Potentially capturing pieces:
    for piece in order[1]:
        chess_coord,subsection,pos = piece.getInfo()
        pixel_coord = chess_coord_to_pixels(chess_coord)
        if pos==(-1,-1):
            #Default square
            screen.blit(pieces_image,pixel_coord,subsection)
        else:
            #Specifc pixels:
            screen.blit(pieces_image,pos,subsection)



#########MAIN FUNCTION####################################################
#Initialize the chess_board:
chess_board = [ ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'], #8
          ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'], #7
          [  0,    0,    0,    0,    0,    0,    0,    0],  #6
          [  0,    0,    0,    0,    0,    0,    0,    0],  #5
          [  0,    0,    0,    0,    0,    0,    0,    0],  #4
          [  0,    0,    0,    0,    0,    0,    0,    0],  #3
          ['Pw', 'Pw', 'Pw',  'Pw', 'Pw', 'Pw', 'Pw', 'Pw'], #2
          ['Rw', 'Nw', 'Bw',  'Qw', 'Kw', 'Bw', 'Nw', 'Rw'] ]#1
          # a      b     c     d     e     f     g     h

#In chess some data must be stored that is not apparent in the chess_board:
player = 0 #This is the player that makes the next move. 0 is white, 1 is black
castling_rights = [[True, True],[True, True]]
#The above stores whether or not each of the players are permitted to castle on
#either side of the king. (Kingside, Queenside)
En_Passant_Target = -1 #This variable will store a coordinate if there is a square that can be
                       #en passant captured on. Otherwise it stores -1, indicating lack of en passant
                       #targets.
half_move_clock = 0 #This variable stores the number of reversible moves that have been played so far.
#Generate an instance of GamePosition class to store the above data:
position = GamePosition.GamePosition(chess_board,player,castling_rights,En_Passant_Target, half_move_clock)
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
#Load the background chess chess_board image:
background = pygame.image.load(os.path.join('Media', 'board.png')).convert()
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
withAI_pic = pygame.image.load(os.path.join('Media', 'withAI.png')).convert_alpha()
playwhite_pic = pygame.image.load(os.path.join('Media', 'start.png')).convert_alpha()
playblack_pic = pygame.image.load(os.path.join('Media', 'playBlack.png')).convert_alpha()

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
# withfriend_pic = pygame.transform.scale(withfriend_pic,
#                                       (square_width*4,square_height*4))
withAI_pic = pygame.transform.scale(withAI_pic,
                                      (square_width*4,square_height*4))
playwhite_pic = pygame.transform.scale(playwhite_pic,
                                      (square_width*4,square_height*4))
playblack_pic = pygame.transform.scale(playblack_pic,
                                      (square_width*4,square_height*4))
# flipEnabled_pic = pygame.transform.scale(flipEnabled_pic,
#                                       (square_width*4,square_height*4))
# flipDisabled_pic = pygame.transform.scale(flipDisabled_pic,
#                                       (square_width*4,square_height*4))



#Make a window of the same size as the background, set its title, and
#load the background image onto it (the chess_board):
screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Shallow Green')
screen.blit(background,(0,0))

#Generate a list of pieces that should be drawn on the chess_board:
list_of_white_pieces,list_of_black_pieces = create_pieces(chess_board)
#(the list contains references to objects of the class Piece)
#Initialize a list of shades:
list_of_shades = []

clock = pygame.time.Clock() #Helps controlling fps of the game.
isDown = False #Variable that shows if the mouse is being held down
               #onto a piece
isClicked = False #To keep track of whether a piece was clicked in order
#to indicate intention to move by the user.
isTransition = False #Keeps track of whether or not a piece is being animated.
is_draw = False #Will store True if the game ended with a draw
chessEnded = False #Will become True once the chess game ends by checkmate, stalemate, etc.
isRecord = False #Set this to True if you want to record moves to the Opening Book. Do not
#set this to True unless you're 100% sure of what you're doing. The program will never modify
#this value.
is_aiThink = False #Stores whether or not the AI is calculating the best move to be played.
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
#allow drawchess_board() to create Shades on the squares.
#Initialize some more values:
#For animating AI thinking graphics:
ax,ay=0,0
numm = 0
#For showing the menu and keeping track of user choices:
isMenu = True
is_ai = True
isFlip = -1
ai_player = -1
#Finally, a variable to keep false until the user wants to quit:
gameEnded = False
#########################INFINITE LOOP#####################################
#The program remains in this loop until the user quits the application
while not gameEnded:

    if isMenu:
        #Menu needs to be shown right now.
        #Blit the background:
        screen.blit(background,(0,0))
        if is_ai==True:
            screen.blit(playwhite_pic,(square_width*2,square_height*2))
        if isFlip!=-1:
            drawchess_board()
            isMenu = False
            if is_ai and ai_player==0:
                colorsign=1
                bestMoveReturn = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,6,-1000000,1000000,colorsign,bestMoveReturn))
                move_thread.start()
                is_aiThink = True
            continue
        for event in pygame.event.get():
            if event.type==QUIT:
                gameEnded = True
                break
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                ai_player = 1
                isFlip = False
                is_ai = True
        pygame.display.update()
#        clock.tick(60)
        continue
    #Menu part was done if this part reached.
    #If the AI is currently thinking the move to play
    #next, show some fancy looking squares to indicate
    #that.
    #Do it every 6 frames so it's not too fast:
    numm+=1
    if is_aiThink and numm%6==0:
        ax+=1
        if ax==8:
            ay+=1
            ax=0
        if ay==8:
            ax,ay=0,0
        if ax%4==0:
            createShades([])
        #If the AI is white, start from the opposite side (since the chess_board is flipped)
        if ai_player==0:
            list_of_shades.append(Shades.Shades(greenbox_image,(7-ax,7-ay)))
        else:
            list_of_shades.append(Shades.Shades(greenbox_image,(ax,ay)))

    for event in pygame.event.get():
        #Deal with all the user inputs:

        if event.type==QUIT:
            #Window was closed.
            gameEnded = True

            break
        #Under the following conditions, user input should be
        #completely ignored:
        if chessEnded or isTransition or is_aiThink:
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
            if not is_occupied_by(chess_board,x,y,'wb'[player]):
                continue
            #Now we're sure the user is holding their mouse on a
            #piecec that is theirs.
            #Get reference to the piece that should be dragged around or selected:
            dragPiece = get_piece(chess_coord)
            print(dragPiece)
            #Find the possible squares that this piece could attack:
            listofTuples = find_possible_squares(position,x,y)
            #Highlight all such squares:
            createShades(listofTuples)
            #A green box should appear on the square which was selected, unless
            #it's a king under check, in which case it shouldn't because the king
            #has a red color on it in that case.
            if ((dragPiece.pieceinfo[0]=='K') and
                (is_check(position,'white') or is_check(position,'black'))):
                None
            else:
                list_of_shades.append(Shades.Shades(greenbox_image,(x,y)))
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
                        if is_occupied_by(chess_board,x2,y2,'wb'[player]):
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
            make_move(position,x,y,x2,y2)
            #Update this move to be the 'previous' move (latest move in fact), so that
            #yellow shades can be shown on it.
            prevMove = [x,y,x2,y2]
            #Update which player is next to play:
            player = position.getplayer()
            #Add the new position to the history for it:
            position.addtoHistory(position)
            #Check for possibilty of draw:
            HMC = position.getHMC()
            if HMC>=100 or is_stalemate(position) or position.checkRepition():
                #There is a draw:
                is_draw = True
                chessEnded = True
            #Check for possibilty of checkmate:
            if is_check_mate(position,'white'):
                winner = 'b'
                chessEnded = True
            if is_check_mate(position,'black'):
                winner = 'w'
                chessEnded = True
            #If the AI option was selecteed and the game still hasn't finished,
            #let the AI start thinking about its next move:
            if is_ai and not chessEnded:
                if player==0:
                    colorsign = 1
                else:
                    colorsign = -1
                bestMoveReturn = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,colorsign,bestMoveReturn))
                move_thread.start()
                is_aiThink = True
            #Move the piece to its new destination:
            dragPiece.setcoord((x2,y2))
            #There may have been a capture, so the piece list should be regenerated.
            #However, if animation is ocurring, the the captured piece should still remain visible.
            if not isTransition:
                list_of_white_pieces,list_of_black_pieces = create_pieces(chess_board)
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
            list_of_white_pieces,list_of_black_pieces = create_pieces(chess_board)
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
    if is_aiThink and not isTransition:
        if not move_thread.isAlive():
            #The AI has made a decision.
            #It's no longer thinking
            is_aiThink = False
            #Destroy any shades:
            createShades([])
            #Get the move proposed:
            #[x,y],[x2,y2] = bestMoveReturn
            print(f"BestMoveReturn: {bestMoveReturn}")
            p1, p2 = bestMoveReturn
            x,y = p1
            x2,y2 = p2
            #Do everything just as if the user made a move by click-click movement:
            make_move(position,x,y,x2,y2)
            prevMove = [x,y,x2,y2]
            player = position.getplayer()
            HMC = position.getHMC()
            position.addtoHistory(position)
            if HMC>=100 or is_stalemate(position) or position.checkRepition():
                is_draw = True
                chessEnded = True
            if is_check_mate(position,'white'):
                winner = 'b'
                chessEnded = True
            if is_check_mate(position,'black'):
                winner = 'w'
                chessEnded = True
            #Animate the movement:
            isTransition = True
            movingPiece = get_piece((x,y))
            origin = chess_coord_to_pixels((x,y))
            destiny = chess_coord_to_pixels((x2,y2))
            movingPiece.setpos(origin)
            step = (destiny[0]-origin[0],destiny[1]-origin[1])

    #Update positions of all images:
    drawchess_board()
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
