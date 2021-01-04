import timeit

from AI import ChessAI
from Helper import Helper
from Move import Move


class Game:

    def __init__(self, move: Move, chess_ai: ChessAI):
        self.__move = move
        self.__chess_ai = chess_ai

    @property
    def move(self) -> Move:
        return self.__move

    def print_moves(self):
        print(self.move.get_all_legal_moves())

    def make_move(self) -> None:
        print(self.move.color_turn)
        old_square = input("old: ")
        new_square = input("new: ")
        old_coordinate = Helper.square_name_to_coordinate(old_square)
        new_coordinate = Helper.square_name_to_coordinate(new_square)

        self.move.move((old_coordinate[0], old_coordinate[1]), (new_coordinate[0], new_coordinate[1]))
        t1 = timeit.default_timer()
        move = self.__chess_ai.minimax_root(2, True)
        t2 = timeit.default_timer()
        print(t2 - t1)
        self.move.move(list(move.keys())[0], list(move.values())[0])
