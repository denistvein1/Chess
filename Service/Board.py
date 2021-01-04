from Domain.Piece import Piece
from Repository.BoardRepository import BoardRepository


class Board:

    def __init__(self, board_repository: BoardRepository):
        self.__board_repository = board_repository
        self.__all_positions = list()

    @property
    def all_positions(self) -> list:
        return self.__all_positions

    def place_piece(self, coordinate: tuple, piece: Piece) -> None:
        self.__board_repository.place_piece(coordinate, piece)

    def get_piece(self, coordinate: tuple) -> Piece:
        return self.__board_repository.get_piece(coordinate)

    def get_coordinate(self, piece: Piece) -> tuple:
        return self.__board_repository.get_coordinate(piece)

    def remove_piece(self, coordinate: tuple) -> Piece:
        return self.__board_repository.remove_piece(coordinate)

    def update_piece_position(self, coordinate: tuple, new_coordinate: tuple) -> None:
        self.__board_repository.update_piece_position(coordinate, new_coordinate)

    def is_piece(self, coordinate: tuple) -> bool:
        return self.__board_repository[coordinate].piece.piece_type is not None

    def save_position(self) -> None:
        position = list()
        for i in range(8):
            for j in range(8):
                if self.is_piece((i, j)):
                    position.append((self.get_piece((i, j)), (i, j)))
        self.__all_positions.append(position)

    def equal_positions(self, position1: list, position2: list) -> bool:
        if len(position1) != len(position2):
            return False
        for i in range(len(position1)):
            if position1[i][0].is_not_equal(position2[i][0]) or position1[i][1] != position2[i][1]:
                return False
        return True

    def three_fold_repetition(self) -> bool:
        count = 0
        for position in self.__all_positions:
            if self.equal_positions(self.__all_positions[len(self.__all_positions) - 1], position):
                count += 1
        if count >= 3:
            return True
        return False

    def get_path(self, coordinate1: tuple, coordinate2: tuple) -> list:
        path = list()
        i_min = min(coordinate1[0], coordinate2[0])
        j_min = min(coordinate1[1], coordinate2[1])
        i_max = max(coordinate1[0], coordinate2[0])
        j_max = max(coordinate1[1], coordinate2[1])
        if coordinate1[0] + coordinate1[1] == coordinate2[0] + coordinate2[1]:
            for i in range(i_min + 1, i_max):
                path.append((i, j_max - i + i_min))
        elif coordinate1[0] - coordinate2[0] == coordinate1[1] - coordinate2[1]:
            for i in range(i_min + 1, i_max):
                path.append((i, j_min + i - i_min))
        elif coordinate1[0] == coordinate2[0]:
            for j in range(j_min + 1, j_max):
                path.append((coordinate1[0], j))
        elif coordinate1[1] == coordinate2[1]:
            for i in range(i_min + 1, i_max):
                path.append((i, coordinate1[1]))
        return path

    def get_pieces(self, color: str) -> list:
        pieces = list()
        for i in range(8):
            for j in range(8):
                if self.is_piece((i, j)):
                    piece = self.get_piece((i, j))
                    if piece.piece_color == color:
                        pieces.append(piece)
        return pieces

    def get_all_pieces(self) -> list:
        return self.get_pieces("white") + self.get_pieces("black")

    def __str__(self) -> str:
        board = ""
        for i in range(7, -1, -1):
            board += str(i + 1) + "  "
            for j in range(8):
                if self.is_piece((i, j)):
                    piece = self.get_piece((i, j))
                    board += piece.piece_type + piece.piece_color[0] + ' '
                else:
                    board += "0  "
            board += "\n"
        board += "   "
        for i in range(8):
            board += chr(ord('a') + i) + "  "
        return board
