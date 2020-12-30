from Move import Move
from Repository.BoardRepository import BoardRepository
from Service.Board import Board
from UI.GameUI import Game

board_repository = BoardRepository()
board = Board(board_repository)
move = Move(board)
game = Game(move)


def main_ui() -> None:
    for i in range(1, 100):
        print(board)
        print()
        game.make_move()


main_ui()
