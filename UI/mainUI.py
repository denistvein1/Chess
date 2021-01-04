from AI import ChessAI
from Move import Move
from Repository.BoardRepository import BoardRepository
from Service.Board import Board
from UI.GameUI import Game

board_repository = BoardRepository()
board = Board(board_repository)
move = Move(board)
chess_ai = ChessAI(move)
game = Game(move, chess_ai)


def main_ui() -> None:
    while True:
        print(board)
        game.make_move()


