from tkinter import PhotoImage

from Domain.Piece import Piece, PIECE_TYPES, PIECE_COLORS
from Domain.Square import Square


class Helper:

    @staticmethod
    def get_piece_type_color_number_by_square_name(square_name: str) -> tuple:
        if square_name[1] == '2':
            return 'p', "white", square_name
        elif square_name[1] == '7':
            return 'p', "black", square_name
        elif square_name in ["B1", "G1"]:
            return 'k', "white", square_name
        elif square_name in ["B8", "G8"]:
            return 'k', "black", square_name
        elif square_name in ["A1", "H1"]:
            return 'r', "white", square_name
        elif square_name in ["A8", "H8"]:
            return 'r', "black", square_name
        elif square_name in ["C1", "F1"]:
            return 'b', "white", square_name
        elif square_name in ["C8", "F8"]:
            return 'b', "black", square_name
        elif square_name == "D1":
            return 'q', "white", square_name
        elif square_name == "D8":
            return 'q', "black", square_name
        elif square_name == "E1":
            return 'K', "white", square_name
        elif square_name == "E8":
            return 'K', "black", square_name
        else:
            return None, None, None

    @staticmethod
    def get_image_path_by_piece_type_color_number(piece_type: str, piece_color: str, piece_number: str):
        if piece_type not in PIECE_TYPES or piece_color not in PIECE_COLORS:
            raise ValueError
        if piece_type is None and piece_color is None:
            raise FileNotFoundError
        temp = piece_number + ".png"
        if piece_color == "white":
            if piece_type == 'p':
                return "pieces/white_pawn_" + temp
            elif piece_type == 'k':
                return "pieces/white_knight_" + temp
            elif piece_type == 'b':
                return "pieces/white_bishop_" + temp
            elif piece_type == 'r':
                return "pieces/white_rook_" + temp
            elif piece_type == 'q':
                return "pieces/white_queen_" + temp
            elif piece_type == 'K':
                return "pieces/white_king_" + temp
        else:
            if piece_type == 'p':
                return "pieces/black_pawn_" + temp
            elif piece_type == 'k':
                return "pieces/black_knight_" + temp
            elif piece_type == 'b':
                return "pieces/black_bishop_" + temp
            elif piece_type == 'r':
                return "pieces/black_rook_" + temp
            elif piece_type == 'q':
                return "pieces/black_queen_" + temp
            elif piece_type == 'K':
                return "pieces/black_king_" + temp

    @staticmethod
    def get_gui_coordinate_by_square_name(square_name: str) -> tuple:
        chess_board = PhotoImage(file="./chess_board.png")
        chess_board_width = chess_board.width()
        chess_board_height = chess_board.height()
        square_width = chess_board_width / 8
        square_height = chess_board_height / 8

        for h in range(8):
            for w in range(8):
                if ord(square_name[0]) - 65 == w and int(square_name[1]) == h + 1:
                    return w * square_width + square_width / 2, (7 - h) * square_height + square_height / 2

    @staticmethod
    def get_square_name_by_gui_coordinate(coordinate: tuple) -> str:
        chess_board = PhotoImage(file="./chess_board.png")
        square_width = chess_board.width() / 8
        square_height = chess_board.height() / 8
        width, height = coordinate
        square_name = []

        for i in range(1, 9):
            if (i - 1) * square_width <= width < i * square_width:
                square_name.append(chr(ord('A') + i - 1))
        for i in range(1, 9):
            if (i - 1) * square_height <= height < i * square_height:
                square_name.append(str(9 - i))
        if not len(square_name):
            square_name.append('H')
            square_name.append('1')
        elif len(square_name) == 1:
            try:
                int(square_name[0])
                square_name.insert(0, 'H')
            except ValueError:
                square_name.append('1')
        return str(square_name[0] + square_name[1])

    @staticmethod
    def get_all_square_names() -> list:
        square_names = list()
        for i in range(8):
            for j in range(8):
                square_names.append(Helper.square_coordinate_to_name((i, j)))
        return square_names

    @staticmethod
    def square_coordinate_to_name(coordinate: tuple) -> str:
        y, x = coordinate
        default = "A1"
        name = ""
        name += chr(ord(default[0]) + x)
        name += chr(ord(default[1]) + y)
        return name

    @staticmethod
    def square_name_to_coordinate(square_name: str) -> tuple:
        x = y = 0
        x += ord(square_name[0].upper()) - 65
        y += ord(square_name[1]) - 49
        return y, x

    @staticmethod
    def initialize_squares() -> dict:
        squares = dict()

        for i in range(2, 6):
            for j in range(8):
                squares[(i, j)] = Square((i, j), Piece(None, None, None))

        for i in range(8):
            squares[(1, i)] = Square((1, i), Piece("pawn", "p", "white"))
            squares[(6, i)] = Square((6, i), Piece("pawn", "p", "black"))

        squares[(0, 0)] = Square((0, 0), Piece("rook", "r", "white"))
        squares[(0, 7)] = Square((0, 7), Piece("rook", "r", "white"))
        squares[(7, 0)] = Square((7, 0), Piece("rook", "r", "black"))
        squares[(7, 7)] = Square((7, 7), Piece("rook", "r", "black"))

        squares[(0, 1)] = Square((0, 1), Piece("knight", "k", "white"))
        squares[(0, 6)] = Square((0, 6), Piece("knight", "k", "white"))
        squares[(7, 1)] = Square((7, 1), Piece("knight", "k", "black"))
        squares[(7, 6)] = Square((7, 6), Piece("knight", "k", "black"))

        squares[(0, 2)] = Square((0, 2), Piece("bishop", "b", "white"))
        squares[(0, 5)] = Square((0, 5), Piece("bishop", "b", "white"))
        squares[(7, 2)] = Square((7, 2), Piece("bishop", "b", "black"))
        squares[(7, 5)] = Square((7, 5), Piece("bishop", "b", "black"))

        squares[(0, 3)] = Square((0, 3), Piece("queen", "q", "white"))
        squares[(0, 4)] = Square((0, 4), Piece("king", "K", "white"))
        squares[(7, 3)] = Square((7, 3), Piece("queen", "q", "black"))
        squares[(7, 4)] = Square((7, 4), Piece("king", "K", "black"))
        return squares
