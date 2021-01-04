from Domain.Piece import Piece
from Domain.Square import Square
from Exceptions.Exceptions import ChessExceptions
from Helper import Helper


class PieceNotFoundError(ChessExceptions):

    def __init__(self, msg: str):
        super().__init__(msg)


class PlacePieceError(ChessExceptions):

    def __init__(self, msg: str):
        super().__init__(msg)


class BoardRepository:

    def __init__(self):
        self.__squares = Helper.initialize_squares()

    def __getitem__(self, coordinate: tuple) -> Square:
        return self.__squares[coordinate]

    def __setitem__(self, coordinate: tuple, square: Square) -> None:
        self.__squares[coordinate] = square

    @property
    def squares(self) -> dict:
        return self.__squares

    def place_piece(self, coordinate: tuple, piece: Piece) -> None:
        x, y = coordinate
        if not 0 <= x <= 7 or not 0 <= y <= 7:
            raise IndexError
        if self[coordinate].piece.piece_color == piece.piece_color:
            raise PlacePieceError("There is a piece of same color on {}".format(coordinate))
        self[coordinate].piece = piece

    def get_piece(self, coordinate: tuple) -> Piece:
        x, y = coordinate
        if not 0 <= x <= 7 or not 0 <= y <= 7:
            raise IndexError
        try:
            return self.__squares[coordinate].piece
        except KeyError:
            raise PieceNotFoundError("No piece at position {}".format(coordinate))

    def remove_piece(self, coordinate: tuple) -> Piece:
        x, y = coordinate
        if not 0 <= x <= 7 or not 0 <= y <= 7:
            raise IndexError
        piece = self.get_piece(coordinate)
        self[coordinate].piece = Piece(None, None, None)
        return piece

    def update_piece_position(self, coordinate: tuple, new_coordinate: tuple) -> None:
        piece = self.remove_piece(coordinate)
        self.place_piece(new_coordinate, Piece(piece.piece_name, piece.piece_type, piece.piece_color, has_moved=True))

    def get_coordinate(self, piece: Piece) -> tuple:
        for coordinate in self.squares.keys():
            if self[coordinate].piece == piece:
                return coordinate
        raise ValueError
