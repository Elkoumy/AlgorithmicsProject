#Shades - This is used for GUI. A shade is a transparent colored image that is displayed on
# a specific square of the chess chess_board, in order to show various things to the user such as
# the squares to which a piece may move, the square that is currently selected, etc. The class
# stores a reference to the image that the instance of the class should display when needed. It
# also stores the coordinates at which the shade would be applied.

class Shades:
    #Self explanatory:
    def __init__(self,image,coord):
        self.image = image
        self.pos = coord
    def get_info(self):
        return [self.image,self.pos]

        

