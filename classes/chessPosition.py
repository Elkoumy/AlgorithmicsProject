
import copy
from modules.chess_processing import pos_to_key

class chessPosition:
    """
    chessPosition is used to store a chess position. this class contains set of features that determine the
    state of the game, like position of pieces on the board, whose has right to play next, etc.
    """

    def __init__(self, chess_board, player, castling_rights, EnP_Target, HMC, history={}):
        # 2d array for piece position
        self.chess_board = chess_board
        # who has right to play, 0 for white, and 1 for black
        self.player = player
        # castling rights
        self.castling = castling_rights
        # position coordinate that can be attacked by a passant.
        self.EnP = EnP_Target
        # Half move clock
        self.HMC = HMC
        # move history
        self.history = history


    def getchess_board(self):
        return self.chess_board
    def setchess_board(self,chess_board):
        self.chess_board = chess_board
    def get_player(self):
        return self.player
    def set_player(self,player):
        self.player = player
    def get_castle_rights(self):
        return self.castling
    def set_castle_rights(self,castling_rights):
        self.castling = castling_rights
    def get_EnP(self):
        return self.EnP
    def set_EnP(self, EnP_Target):
        self.EnP = EnP_Target
    def get_HMC(self):
        return self.HMC
    def set_HMC(self,HMC):
        self.HMC = HMC

    def check_repetition(self):
        """

        Returns: this function return true by checking the history if the values above a threshold.

        """
        return any(value>=3 for value in self.history.values())


    def add_to_history(self,position):
        """
         This function creates a unique key for a position to add it to the history dict.
        Args:
            position:

        Returns:

        """
        # from coordinates to unique key
        key = pos_to_key(position)
        # add key to history
        self.history[key] = self.history.get(key,0) + 1

    def get_history(self):
        """

        Returns: the history dict

        """
        return self.history

    def clone(self):
        """

        Returns: get clone from the current object

        """
        clone = chessPosition(copy.deepcopy(self.chess_board),
                             self.player,
                             copy.deepcopy(self.castling),
                             self.EnP,
                             self.HMC)
        return clone
