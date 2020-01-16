
class pieceDisplay:
    """
    pieceDisplay: this is a helper class for the GUI, store information about the object which is should
    be displayed

    """
    def __init__(self,pieceDisplayinfo,chess_coord,square_width,square_height):
        """

        Args:
            pieceDisplayinfo:
            chess_coord: hold information about the piece and it's a string such as "Qw" for the queen and white
            square_width:
            square_height:
        """
        # size of the square on the board
        self.square_width = square_width
        self.square_height = square_height
        # chess pieces
        pieceDisplay = pieceDisplayinfo[0]
        # pieces colors
        color = pieceDisplayinfo[1]

        if pieceDisplay=='K':
            index = 0
        elif pieceDisplay=='Q':
            index = 1
        elif pieceDisplay=='B':
            index = 2
        elif pieceDisplay == 'N':
            index = 3
        elif pieceDisplay == 'R':
            index = 4
        elif pieceDisplay == 'P':
            index = 5
        left_x = self.square_width*index
        if color == 'w':
            left_y = 0
        else:
            left_y = self.square_height

        self.pieceDisplayinfo = pieceDisplayinfo

        self.subsection = (left_x,left_y,self.square_width,self.square_height)
        #chess position representation
        self.chess_coord = chess_coord
        self.pos = (-1,-1)

    #The methods are self explanatory:
    def get_info(self):
        return [self.chess_coord, self.subsection,self.pos]
    def set_pos(self,pos):
        self.pos = pos
    def get_pos(self):
        return self.pos
    def set_coord(self,coord):
        self.chess_coord = coord
    def __repr__(self):
        return self.pieceDisplayinfo+'('+str(self.chess_coord[0])+','+str(self.chess_coord[1])+')'
