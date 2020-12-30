from tkinter import *
from tkinter import messagebox

from AI import ChessAI
from GUI.GUI import GUI
from Helper import Helper
from Move import Move, CantMoveError


class StartGUI(GUI):
    w_queens = 0
    b_queens = 0

    def __init__(self, root: Tk, move: Move, chess_ai: ChessAI):
        super().__init__(move)
        self.__root = root
        self.__chess_ai = chess_ai
        self.__active_images = dict()
        self.__is_piece_selected = False
        self.__old_square_drag_release = None
        self.__old_square_click = None

    @property
    def root(self) -> Tk:
        return self.__root

    def create_img(self, square_name: str, coordinate: tuple) -> None:
        piece_type, piece_color, piece_number = self._square_type_color_number[square_name]
        self._all_images[(piece_type, piece_color, piece_number)] = PhotoImage(file=Helper.get_image_path_by_piece_type_color_number(piece_type, piece_color, piece_number))
        self.__active_images[square_name] = self.widgets["game_canvas"].create_image(coordinate[0], coordinate[1], image=self._all_images[piece_type, piece_color, piece_number])

    def drag_image(self, mouse) -> None:
        square_name = Helper.get_square_name_by_gui_coordinate((mouse.x, mouse.y))

        if self.__active_images[square_name] is not None and not self.__is_piece_selected:
            self.__is_piece_selected = True
            self.__old_square_drag_release = square_name
            self.__old_square_click = None
        elif self.__is_piece_selected:
            self.create_img(self.__old_square_drag_release, (mouse.x, mouse.y))

    def click(self, mouse) -> None:
        square_name = Helper.get_square_name_by_gui_coordinate((mouse.x, mouse.y))
        coordinate = Helper.square_name_to_coordinate(square_name)
        available_moves = self._move.available_move_options(coordinate)

        if len(self._grey_dot_images.keys()) and self.__old_square_click:
            self.main_move_function_gui(mouse, self.__old_square_click, self.unselect_piece_click)
        elif self.__active_images[square_name]:
            piece_type, piece_color, piece_number = self._square_type_color_number[square_name]
            if piece_color == self._move.color_turn:
                self.__old_square_click = square_name

        self.delete_grey_dots()
        if self._move.check():
            available_moves = self._move.check_options(coordinate)
        if len(self._move.moves_that_place_king_in_check(coordinate)):
            available_moves = list((set(available_moves)).difference(set(self._move.moves_that_place_king_in_check(coordinate))))
        for move in available_moves:
            square = Helper.square_coordinate_to_name(move)
            gui_coordinate = Helper.get_gui_coordinate_by_square_name(square)
            self._grey_dot_images[square] = self.widgets["game_canvas"].create_image(gui_coordinate[0], gui_coordinate[1], image=self._grey_dot_image)

    def main_move_function_gui(self, mouse, square, unselect_piece) -> None:
        if square is None:
            return
        old_coordinate = Helper.square_name_to_coordinate(square)
        new_coordinate = Helper.square_name_to_coordinate(Helper.get_square_name_by_gui_coordinate((mouse.x, mouse.y)))
        try:
            moves = self._move.move(old_coordinate, new_coordinate)
        except CantMoveError:
            gui_coordinate = Helper.get_gui_coordinate_by_square_name(Helper.square_coordinate_to_name(old_coordinate))
            self.create_img(square, gui_coordinate)
            unselect_piece()
            return
        self.update_square(moves)
        self.delete_grey_dots()
        self.remove_check()
        self.check()
        unselect_piece()
        self.stalemate()
        self.checkmate()
        self.draw()
        self.three_fold_repetition()
        self.main_move_function_ai()

    def main_move_function_ai(self):
        move = self.__chess_ai.minimax_root(1, True)
        self._move.move(list(move.keys())[0], list(move.values())[0])
        self.update_square(move)
        self.remove_check()
        self.check()
        self.stalemate()
        self.checkmate()
        self.draw()
        self.three_fold_repetition()

    def release(self, mouse) -> None:
        self.main_move_function_gui(mouse, self.__old_square_drag_release, self.unselect_piece_drag_release)

    def check(self) -> None:
        color = self._move.check()
        if color is not None:
            for square in Helper.get_all_square_names():
                piece_type, piece_color, piece_number = self._square_type_color_number[square]
                if piece_type == 'K' and piece_color == color:
                    gui_coordinate = Helper.get_gui_coordinate_by_square_name(square)
                    self._red_dot_images[square] = self.widgets["game_canvas"].create_image(gui_coordinate[0], gui_coordinate[1], image=self._red_dot_image)

    def remove_check(self) -> None:
        for square in self._red_dot_images.keys():
            self.widgets["game_canvas"].delete(self._red_dot_images[square])

    def unselect_piece_drag_release(self) -> None:
        self.__is_piece_selected = False
        self.__old_square_drag_release = None

    def unselect_piece_click(self) -> None:
        self.__old_square_click = None

    def delete_grey_dots(self) -> None:
        try:
            for square in self._grey_dot_images.keys():
                self.widgets["game_canvas"].delete(self._grey_dot_images[square])
        except TclError:
            pass

    def update_square(self, moves: dict) -> None:
        for move in moves.keys():
            old_square = Helper.square_coordinate_to_name(move)
            new_square = Helper.square_coordinate_to_name(moves[move])
            self.update_image(old_square, new_square)

    def update_image(self, old_square: str, new_square: str) -> None:
        piece_type, piece_color, piece_number = self._square_type_color_number[old_square]
        piece_type, piece_number = self.check_promotion(new_square, piece_type, piece_color, piece_number)
        new_coordinate = Helper.get_gui_coordinate_by_square_name(new_square)

        if self._move.is_passant:
            passant_square = Helper.square_coordinate_to_name(self._move.passant_coordinate)
            self.widgets["game_canvas"].delete(self.__active_images[passant_square])
            self.__active_images[passant_square] = None
            self._square_type_color_number[passant_square] = None, None, None
            self._move.is_passant = False
            self._move.passant_coordinate = None

        self.widgets["game_canvas"].delete(self.__active_images[old_square])
        self.widgets["game_canvas"].delete(self.__active_images[new_square])
        self.__active_images[old_square] = None
        self.__active_images[new_square] = None

        self._all_images[(piece_type, piece_color, piece_number)] = PhotoImage(file=Helper.get_image_path_by_piece_type_color_number(piece_type, piece_color, piece_number))
        self.__active_images[new_square] = self.widgets["game_canvas"].create_image(new_coordinate[0], new_coordinate[1], image=self._all_images[piece_type, piece_color, piece_number])
        self._square_type_color_number[old_square] = None, None, None
        self._square_type_color_number[new_square] = piece_type, piece_color, piece_number

    def draw(self) -> None:
        if not self._move.draw:
            self._move.draw_the_game()
            if self._move.draw:
                draw_messagebox = messagebox.showinfo("Draw", "Draw by insufficient material!")
                Label(self.root, text=draw_messagebox).grid(row=0, column=0)
                self.root.destroy()

    def checkmate(self) -> None:
        if self._move.is_checkmate():
            checkmate_messagebox = messagebox.showinfo("Checkmate", "Checkmate!")
            Label(self.root, text=checkmate_messagebox).grid(row=0, column=0)
            self.root.destroy()

    def stalemate(self) -> None:
        if self._move.is_stalemate():
            stalemate_messagebox = messagebox.showinfo("Stalemate", "Stalemate!")
            Label(self.root, text=stalemate_messagebox).grid(row=0, column=0)
            self.root.destroy()

    def three_fold_repetition(self) -> None:
        if self._move.three_fold_repetition():
            three_fold_repetition_messagebox = messagebox.showinfo("Draw", "Draw by repetition!")
            Label(self.root, text=three_fold_repetition_messagebox).grid(row=0, column=0)
            self.root.destroy()

    @staticmethod
    def check_promotion(new_square: str, piece_type: str, piece_color: str, piece_number: str) -> tuple:
        if new_square[1] in ['1', '8'] and piece_type == 'p':
            if piece_color == "white":
                StartGUI.w_queens += 1
                return 'q', "R{}".format(StartGUI.w_queens)
            else:
                StartGUI.b_queens += 1
                return 'q', "R{}".format(StartGUI.b_queens)
        return piece_type, piece_number

    def position_pieces(self) -> None:
        for square_name in Helper.get_all_square_names():
            piece_type, piece_color, piece_number = Helper.get_piece_type_color_number_by_square_name(square_name)
            coordinate = Helper.get_gui_coordinate_by_square_name(square_name)
            try:
                self.__active_images[square_name] = self.widgets["game_canvas"].create_image(coordinate[0], coordinate[1], image=self._all_images[piece_type, piece_color, piece_number])
            except KeyError:
                self.__active_images[square_name] = None

    def play(self) -> None:
        self.destroyer()
        self.generator(self.root)

        game_canvas = self.widgets["game_canvas"]
        game_canvas.grid(row=0, column=0)
        game_canvas.create_image(0, 0, image=self._chess_board_image, anchor=NW)
        self.position_pieces()
        game_canvas.bind('<Button-1>', self.click)
        game_canvas.bind('<B1-Motion>', self.drag_image)
        game_canvas.bind('<ButtonRelease-1>', self.release)
