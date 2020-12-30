from Helper import Helper
from Move import Move


class Game:

    def __init__(self, move: Move):
        self.__move = move

    @property
    def move(self) -> Move:
        return self.__move

    def print_moves(self):
        print(self.move.get_all_legal_moves())

    def make_move(self, undo: bool = False) -> None:
        if undo:
            self.move.undo_move()
            return
        print(self.move.color_turn)
        old_square = input("old: ")
        new_square = input("new: ")
        old_coordinate = Helper.square_name_to_coordinate(old_square)
        new_coordinate = Helper.square_name_to_coordinate(new_square)

        self.move.move((old_coordinate[0], old_coordinate[1]), (new_coordinate[0], new_coordinate[1]))
        self.move.save_position()
