
"""

@author: nesma
"""

##############################////////GUI FUNCTIONS\\\\\\\\\\\\\#############################
def chess_coord_to_pixels(chess_coord):
    x,y = chess_coord
    #There are two sets of coordinates that this function could choose to return.
    #One is the coordinates that would be usually returned, the other is one that
    #would be returned if the chess_board were to be flipped.
    #Note that square width and height variables are defined in the main function and 
    #so are accessible here as global variables.
    if isAI:
        if AIPlayer==0:
            #This means you're playing against the AI and are playing as black:
            return ((7-x)*square_width, (7-y)*square_height)
        else:
            return (x*square_width, y*square_height)
#    #Being here means two player game is being played.
#    #If the flipping mode is enabled, and the player to play is black,
#    #the chess_board should flip, but not until the transition animation for
#    #white movement is complete:
#    if not is_flip or player==0 ^ is_transition:
#        return (x*square_width, y*square_height)
#    else:
#        return ((7-x)*square_width, (7-y)*square_height)
def pixel_coord_to_chess(pixel_coord):
    x,y = pixel_coord[0]/square_width, pixel_coord[1]/square_height
    #See comments for chess_coord_to_pixels() for an explanation of the
    #conditions seen here:
    if isAI:
        if AIPlayer==0:
            return (7-x,7-y)
        else:
            return (x,y)
#    if not is_flip or player==0 ^ is_transition:
#        return (x,y)
#    else:
#        return (7-x,7-y)
def get_piece(chess_coord):
    for piece in list_of_white_pieces+list_of_black_pieces:
        #piece.getInfo()[0] represents the chess coordinate occupied
        #by piece.
        if piece.getInfo()[0] == chess_coord:
            return piece
def create_pieces(chess_board):
    #Initialize containers:
    list_of_white_pieces = []
    list_of_black_pieces = []
    #Loop through all squares:
    for i in range(8):
        for k in range(8):
            if chess_board[i][k]!=0:
                #The square is not empty, create a piece object:
                p = Piece(chess_board[i][k],(k,i),square_width,square_height)
                #Append the reference to the object to the appropriate
                #list:
                if chess_board[i][k][1]=='w':
                    list_of_white_pieces.append(p)
                else:
                    list_of_black_pieces.append(p)
    #Return both:
    return [list_of_white_pieces,list_of_black_pieces]
def createShades(listofTuples):
    global listofShades
    #Empty the list
    listofShades = []
    if is_transition:
        #Nothing should be shaded when a piece is being animated:
        return
    if isDraw:
        #The game ended with a draw. Make yellow circle shades for
        #both the kings to show this is the case:
        coord = lookfor(chess_board,'Kw')[0]
        shade = Shades(circle_image_yellow,coord)
        listofShades.append(shade)
        coord = lookfor(chess_board,'Kb')[0]
        shade = Shades(circle_image_yellow,coord)
        listofShades.append(shade)
        #There is no need to go further:
        return
    if chessEnded:
        #The game has ended, with a checkmate because it cannot be a 
        #draw if the code reached here.
        #Give the winning king a green circle shade:
        coord = lookfor(chess_board,'K'+winner)[0]
        shade = Shades(circle_image_green_big,coord)
        listofShades.append(shade)
    #If either king is under attack, give them a red circle:
    if isCheck(position,'white'):
        coord = lookfor(chess_board,'Kw')[0]
        shade = Shades(circle_image_red,coord)
        listofShades.append(shade)
    if isCheck(position,'black'):
        coord = lookfor(chess_board,'Kb')[0]
        shade = Shades(circle_image_red,coord)
        listofShades.append(shade)
    #Go through all the target squares inputted:
    for pos in listofTuples:
        #If the target square is occupied, it can be captured.
        #For a capturable square, there is a different shade.
        #Create the appropriate shade for each target square:
        if isOccupied(chess_board,pos[0],pos[1]):
            img = circle_image_capture
        else:
            img = circle_image_green
        shade = Shades(img,pos)
        #Append:
        listofShades.append(shade)
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
    if isDraw or chessEnded or isAIThink:
        #Shades
        for shade in listofShades:
            img,chess_coord = shade.getInfo()
            pixel_coord = chess_coord_to_pixels(chess_coord)
            screen.blit(img,pixel_coord)
    #Make shades to show what the previous move played was:
    if prevMove[0]!=-1 and not is_transition:
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
    if not (isDraw or chessEnded or isAIThink):
        for shade in listofShades:
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
