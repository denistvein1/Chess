from Domain.Piece import Piece


class Square:

    def __init__(self, coordinate: tuple, piece: Piece):
        if not 0 <= coordinate[0] <= 7 or not 0 <= coordinate[1] <= 7:
            raise ValueError
        self.__coordinate = coordinate
        self.__piece = piece

    @property
    def coordinate(self) -> tuple:
        return self.__coordinate

    @property
    def piece(self) -> Piece:
        return self.__piece

    @piece.setter
    def piece(self, piece: Piece) -> None:
        self.__piece = piece
