PIECE_NAMES = [None, "pawn", "knight", "bishop", "rook", "queen", "king"]
PIECE_TYPES = [None, "p", "k", "b", "r", "q", "K"]
PIECE_COLORS = [None, "white", "black"]


class Piece:
    """
    Piece class having some certain characteristics specific to chess
    and a coordinate on the board.
    """

    def __init__(self, piece_name, piece_type, piece_color, has_moved: bool = False):
        if piece_name not in PIECE_NAMES or piece_type not in PIECE_TYPES or piece_color not in PIECE_COLORS:
            raise ValueError
        self.__name = piece_name
        self.__type = piece_type
        self.__piece_color = piece_color
        self.__has_moved = has_moved
        self.__attacking_pieces = dict()

    @property
    def piece_name(self):
        return self.__name

    @property
    def piece_type(self):
        return self.__type

    @property
    def piece_color(self):
        return self.__piece_color

    @property
    def has_moved(self) -> bool:
        return self.__has_moved

    @has_moved.setter
    def has_moved(self, has_moved: bool) -> None:
        self.__has_moved = has_moved

    @property
    def attacking_pieces(self) -> dict:
        return self.__attacking_pieces

    @attacking_pieces.setter
    def attacking_pieces(self, attacking_piece) -> None:
        if attacking_piece not in self.__attacking_pieces:
            self.__attacking_pieces[attacking_piece] = attacking_piece

    def remove_attacking_piece(self, attacking_piece) -> None:
        del self.__attacking_pieces[attacking_piece]

    def is_equal(self, other) -> bool:
        if type(other) != Piece:
            return False
        if self.piece_name == other.piece_name and self.piece_type == other.piece_type and self.piece_color == other.piece_color and self.has_moved == other.has_moved:
            for piece in self.attacking_pieces.keys():
                if piece not in other.attacking_pieces.keys():
                    return False
                if self.attacking_pieces[piece] != other.attacking_pieces[piece]:
                    return False
            return True
        return False

    def is_not_equal(self, other) -> bool:
        return not self.__eq__(other)
