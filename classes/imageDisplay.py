class imageDispaly:
    """
    imageDispaly: is a helper class for the GUI, it represents the color image that is displayed on any square
    """

    # Self explanatory:
    def __init__(self, image, coord):
        self.image = image
        self.pos = coord

    def get_info(self):
        return [self.image, self.pos]



