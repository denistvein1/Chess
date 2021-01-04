import random

from Domain.Piece import Piece
from Move import Move, CantMoveError


class ChessAI:

    def __init__(self, move: Move):
        self.__move = move

    @property
    def move(self) -> Move:
        return self.__move

    def get_piece_value(self, piece: Piece) -> float:
        color_factor = {"white": 1, "black": -1}
        if piece.piece_type == 'p':
            return 10.0 * color_factor[piece.piece_color]
        elif piece.piece_type == 'k':
            return 30.0 * color_factor[piece.piece_color]
        elif piece.piece_type == 'b':
            return 30.0 * color_factor[piece.piece_color]
        elif piece.piece_type == 'r':
            return 50.0 * color_factor[piece.piece_color]
        elif piece.piece_type == 'q':
            return 90.0 * color_factor[piece.piece_color]
        elif piece.piece_type == 'K':
            return 900.0 * color_factor[piece.piece_color]

    def get_absolute_value(self, coordinate: tuple) -> float:
        if self.move.board.is_piece(coordinate):
            piece = self.move.board.get_piece(coordinate)
            return self.get_piece_value(piece)
        else:
            return 0.0

    def heuristic(self) -> float:
        evaluation = 0.0
        for i in range(8):
            for j in range(8):
                evaluation += self.get_absolute_value((i, j))
        return evaluation

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0:
            return -self.heuristic()
        possible_moves = self.__move.get_all_legal_moves()
        if is_maximizing:
            best_move = -9999
            for move in possible_moves:
                coordinate = list(move.keys())[0]
                new_coordinates = list(move.values())[0]
                for new_coordinate in new_coordinates:
                    try:
                        self.__move.move(coordinate, new_coordinate)
                        best_move = max(best_move, self.minimax(depth - 1, alpha, beta, not is_maximizing))
                        self.__move.undo_move()
                    except CantMoveError:
                        pass
                    alpha = max(alpha, best_move)
                    if beta <= alpha:
                        return best_move
            return best_move
        else:
            best_move = 9999
            for move in possible_moves:
                coordinate = list(move.keys())[0]
                new_coordinates = list(move.values())[0]
                for new_coordinate in new_coordinates:
                    try:
                        self.__move.move(coordinate, new_coordinate)
                        best_move = min(best_move, self.minimax(depth - 1, alpha, beta, not is_maximizing))
                        self.__move.undo_move()
                    except CantMoveError:
                        pass
                    beta = min(beta, best_move)
                    if beta <= alpha:
                        return best_move
            return best_move

    def minimax_root(self, depth, is_maximizing):
        possible_moves = self.__move.get_all_legal_moves()
        random.shuffle(possible_moves)
        best_move = -9999
        best_move_final = None
        for move in possible_moves:
            coordinate = list(move.keys())[0]
            new_coordinates = list(move.values())[0]
            for new_coordinate in new_coordinates:
                try:
                    self.__move.move(coordinate, new_coordinate)
                    value = max(best_move, self.minimax(depth - 1, -10000, 10000, not is_maximizing))
                    self.__move.undo_move()
                    if value > best_move:
                        best_move = value
                        best_move_final = {coordinate: new_coordinate}
                except CantMoveError:
                    pass
                # except PlacePieceError:
                #     pass
        return best_move_final
