from tkinter import *
from tkinter.font import Font

from Helper import Helper
from Move import Move


class GUI:

    def __init__(self, move: Move):
        self.__widgets = dict()
        self._chess_board_image = PhotoImage(file="./chess_board.png")
        self._grey_dot_image = PhotoImage(file="./grey_dot.png")
        self._red_dot_image = PhotoImage(file="./red_dot.png")
        self._all_images = dict()
        self._grey_dot_images = dict()
        self._red_dot_images = dict()
        self._square_type_color_number = dict()
        self._move = move

    @property
    def widgets(self) -> dict:
        return self.__widgets

    @staticmethod
    def button_font() -> Font:
        return Font(family="Helvetica", size=20, weight="bold")

    @staticmethod
    def text_font() -> Font:
        return Font(family="Helvetica", size=20, weight="bold")

    def generator(self, root: Tk) -> None:
        game_canvas = Canvas(root, height=830, width=830)
        self.widgets["game_canvas"] = game_canvas

        chess_board = Label(root, image=self._chess_board_image)
        self.widgets["chess_board"] = chess_board

        self.initialize_images()

    def initialize_images(self) -> None:
        for square_name in Helper.get_all_square_names():
            piece_type, piece_color, piece_number = Helper.get_piece_type_color_number_by_square_name(square_name)
            self._square_type_color_number[square_name] = piece_type, piece_color, piece_number
            try:
                self._all_images[(piece_type, piece_color, piece_number)] = PhotoImage(file=Helper.get_image_path_by_piece_type_color_number(piece_type, piece_color, piece_number))
            except FileNotFoundError:
                pass
            self.initialize_r_queens()

    def initialize_r_queens(self) -> None:
        for i in range(1, 9):
            self._all_images[('q', 'white', "R{}".format(i))] = PhotoImage(file="pieces/white_queen_R{}.png".format(i))
            self._all_images[('q', 'black', "R{}".format(i))] = PhotoImage(file="pieces/black_queen_R{}.png".format(i))

    def destroyer(self) -> None:
        for widget in self.widgets.values():
            widget.destroy()
