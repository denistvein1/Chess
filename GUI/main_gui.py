from tkinter import *

from GUI.StartGUI import StartGUI
from Move import Move
from Repository.BoardRepository import BoardRepository
from Service.Board import Board
from AI import ChessAI


def main_gui() -> None:
    root = Tk()
    root.title("Chess")

    board_repository = BoardRepository()
    board = Board(board_repository)
    move = Move(board)
    chess_ai = ChessAI(move)
    start_gui = StartGUI(root, move, chess_ai)
    start_gui.play()

    root.mainloop()
