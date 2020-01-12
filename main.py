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
def create_shades(list_of_tuples):
    global list_of_shades
    #Empty the list
    list_of_shades = []
    if is_transition:
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
    if chess_ended:
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
    for pos in list_of_tuples:
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
    if is_transition:
        #If a piece is being animated, the player info is changed despite
        #white still capturing over black, for example. Reverse the order:
        order = list(reversed(order))
    #The shades which appear during the following three conditions need to be
    #blitted first to appear under the pieces:
    if is_draw or chess_ended or is_aiThink:
        #Shades
        for shade in list_of_shades:
            img,chess_coord = shade.getInfo()
            pixel_coord = chess_coord_to_pixels(chess_coord)
            screen.blit(img,pixel_coord)
    #Make shades to show what the previous move played was:
    if prev_move[0]!=-1 and not is_transition:
        x,y,x2,y2 = prev_move
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
    if not (is_draw or chess_ended or is_aiThink):
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

size_of_bg = background.get_rect().size

square_width =int( size_of_bg[0]/8)
square_height = int(size_of_bg[1]/8)



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

withAI_pic = pygame.transform.scale(withAI_pic,
                                      (square_width*4,square_height*4))
playwhite_pic = pygame.transform.scale(playwhite_pic,
                                      (square_width*4,square_height*4))
playblack_pic = pygame.transform.scale(playblack_pic,
                                      (square_width*4,square_height*4))


screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Shallow Green')
screen.blit(background,(0,0))


list_of_white_pieces,list_of_black_pieces = create_pieces(chess_board)

list_of_shades = []

clock = pygame.time.Clock()
is_down = False #Variable that shows if the mouse is being held down
               #onto a piece
is_clicked = False #To keep track of whether a piece was clicked in order
#to indicate intention to move by the user.
is_transition = False #Keeps track of whether or not a piece is being animated.
is_draw = False #Will store True if the game ended with a draw
chess_ended = False #Will become True once the chess game ends by checkmate, stalemate, etc.
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
prev_move = [-1,-1,-1,-1] #Also a global varible that stores the last move played, to
#allow drawchess_board() to create Shades on the squares.
#Initialize some more values:
#For animating AI thinking graphics:
ax,ay=0,0
numm = 0
#For showing the menu and keeping track of user choices:
is_menu = True
is_ai = True
is_flip = -1
ai_player = -1
#Finally, a variable to keep false until the user wants to quit:
game_ended = False
#########################INFINITE LOOP#####################################
#The program remains in this loop until the user quits the application
while not game_ended:

    if is_menu:
        #Menu needs to be shown right now.
        #Blit the background:
        screen.blit(background,(0,0))
        if is_ai==True:
            screen.blit(playwhite_pic,(square_width*2,square_height*2))
        if is_flip!=-1:
            drawchess_board()
            is_menu = False
            if is_ai and ai_player==0:
                color_sign=1
                best_move_return = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,6,-1000000,1000000,color_sign,best_move_return))
                move_thread.start()
                is_aiThink = True
            continue
        for event in pygame.event.get():
            if event.type==QUIT:
                game_ended = True
                break
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                ai_player = 1
                is_flip = False
                is_ai = True
        pygame.display.update()
        continue

    numm+=1
    if is_aiThink and numm%6==0:
        ax+=1
        if ax==8:
            ay+=1
            ax=0
        if ay==8:
            ax,ay=0,0
        if ax%4==0:
            create_shades([])
        if ai_player==0:
            list_of_shades.append(Shades.Shades(greenbox_image,(7-ax,7-ay)))
        else:
            list_of_shades.append(Shades.Shades(greenbox_image,(ax,ay)))

    for event in pygame.event.get():

        if event.type==QUIT:
            game_ended = True

            break
        if chess_ended or is_transition or is_aiThink:
            continue
        if not is_down and event.type == MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            chess_coord = pixel_coord_to_chess(pos)
            chess_coord=(int(chess_coord[0]),int(chess_coord[1]))

            x =chess_coord[0]
            y = chess_coord[1]

            if not is_occupied_by(chess_board,x,y,'wb'[player]):
                continue

            drag_piece = get_piece(chess_coord)
            print(drag_piece)
            list_of_tuples = find_possible_squares(position,x,y)

            create_shades(list_of_tuples)

            if ((drag_piece.pieceinfo[0]=='K') and
                (is_check(position,'white') or is_check(position,'black'))):
                None
            else:
                list_of_shades.append(Shades.Shades(greenbox_image,(x,y)))
            is_down = True
        if (is_down or is_clicked) and event.type == MOUSEBUTTONUP:
            is_down = False
            drag_piece.setpos((-1,-1))
            pos = pygame.mouse.get_pos()
            chess_coord = pixel_coord_to_chess(pos)
            chess_coord = (int(chess_coord[0]), int(chess_coord[1]))
            x2 = chess_coord[0]
            y2 = chess_coord[1]

            is_transition = False
            if (x,y)==(x2,y2):

                if not is_clicked:

                    is_clicked = True
                    prevPos = (x,y)
                else:

                    x,y = prevPos
                    if (x,y)==(x2,y2):

                        is_clicked = False

                        create_shades([])
                    else:
                        if is_occupied_by(chess_board,x2,y2,'wb'[player]):

                            is_clicked = True
                            prevPos = (x2,y2)
                        else:
                            is_clicked = False
                            create_shades([])
                            is_transition = True


            if not (x2,y2) in list_of_tuples:
                is_transition = False
                continue

            if isRecord:
                key = pos_to_key(position)
                if [(x,y),(x2,y2)] not in openings[key]:
                    openings[key].append([(x,y),(x2,y2)])

            make_move(position,x,y,x2,y2)
            prev_move = [x,y,x2,y2]

            player = position.get_player()
            position.add_to_history(position)

            HMC = position.getHMC()
            if HMC>=100 or is_stalemate(position) or position.check_repitition():
                is_draw = True
                chess_ended = True

            if is_check_mate(position,'white'):
                winner = 'b'
                chess_ended = True
            if is_check_mate(position,'black'):
                winner = 'w'
                chess_ended = True

            if is_ai and not chess_ended:
                if player==0:
                    color_sign = 1
                else:
                    color_sign = -1
                best_move_return = []
                move_thread = threading.Thread(target = negamax,
                            args = (position,3,-1000000,1000000,color_sign,best_move_return))
                move_thread.start()
                is_aiThink = True
            drag_piece.setcoord((x2,y2))
            if not is_transition:
                list_of_white_pieces,list_of_black_pieces = create_pieces(chess_board)
            else:
                moving_piece = drag_piece
                origin = chess_coord_to_pixels((x,y))
                destiny = chess_coord_to_pixels((x2,y2))
                moving_piece.setpos(origin)
                step = (destiny[0]-origin[0],destiny[1]-origin[1])

            #Either way shades should be deleted now:
            create_shades([])
    #If an animation is supposed to happen, make it happen:
    if is_transition:
        p,q = moving_piece.getpos()
        dx2,dy2 = destiny
        n= 30.0
        if abs(p-dx2)<=abs(step[0]/n) and abs(q-dy2)<=abs(step[1]/n):
            #The moving piece has reached its destination:
            #Snap it back to its grid position:
            moving_piece.setpos((-1,-1))
            #Generate new piece list in case one got captured:
            list_of_white_pieces,list_of_black_pieces = create_pieces(chess_board)
            #No more transitioning:
            is_transition = False
            create_shades([])
        else:
            #Move it closer to its destination.
            moving_piece.setpos((p+step[0]/n,q+step[1]/n))
    #If a piece is being dragged let the dragging piece follow the mouse:
    if is_down:
        m,k = pygame.mouse.get_pos()
        drag_piece.setpos((m-square_width/2,k-square_height/2))
    #If the AI is thinking, make sure to check if it isn't done thinking yet.
    #Also, if a piece is currently being animated don't ask the AI if it's
    #done thining, in case it replied in the affirmative and starts moving
    #at the same time as your piece is moving:
    if is_aiThink and not is_transition:
        if not move_thread.isAlive():
            #The AI has made a decision.
            #It's no longer thinking
            is_aiThink = False
            #Destroy any shades:
            create_shades([])
            #Get the move proposed:
            #[x,y],[x2,y2] = best_move_return
            print(f"best_move_return: {best_move_return}")
            p1, p2 = best_move_return
            x,y = p1
            x2,y2 = p2
            #Do everything just as if the user made a move by click-click movement:
            make_move(position,x,y,x2,y2)
            prev_move = [x,y,x2,y2]
            player = position.get_player()
            HMC = position.getHMC()
            position.add_to_history(position)
            if HMC>=100 or is_stalemate(position) or position.check_repitition():
                is_draw = True
                chess_ended = True
            if is_check_mate(position,'white'):
                winner = 'b'
                chess_ended = True
            if is_check_mate(position,'black'):
                winner = 'w'
                chess_ended = True
            #Animate the movement:
            is_transition = True
            moving_piece = get_piece((x,y))
            origin = chess_coord_to_pixels((x,y))
            destiny = chess_coord_to_pixels((x2,y2))
            moving_piece.setpos(origin)
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
