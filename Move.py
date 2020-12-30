from Domain.Piece import Piece
from Exceptions.Exceptions import ChessExceptions
from Service.Board import Board


class CantMoveError(ChessExceptions):

    def __init__(self, msg: str):
        super().__init__(msg)


class Move:
    """
    This class controls the piece movement on the board.
    """

    def __init__(self, board: Board):
        self.__board = board
        self.__color_turn = "white"
        self.__draw = False
        self.__set_attacked = False
        self.is_passant = False
        self.passant_coordinate = None
        self.passant = None

        self.__draw_temp = False
        self.passant_temp = False

    @property
    def board(self) -> Board:
        return self.__board

    @property
    def color_turn(self) -> str:
        return self.__color_turn

    @color_turn.setter
    def color_turn(self, color: str) -> None:
        self.__color_turn = color

    @property
    def draw(self) -> bool:
        return self.__draw

    @draw.setter
    def draw(self, draw: bool) -> None:
        self.__draw = draw

    def __can_move(self, coordinate: tuple) -> bool:
        """
        If there is a piece on the coordinate (that board square = 1)
        AND the piece color is the same as `color_turn` than returns True
        and False otherwise.
        :param coordinate: (x, y) with x and y between 0 and 7.
        :return: bool.
        """
        if self.__board.is_piece(coordinate):
            piece = self.__board.get_piece(coordinate)
            if piece.piece_color == self.color_turn:
                return True
        return False

    def en_passant_helper2(self, coordinate: tuple, piece: Piece) -> list:
        en_passant_moves = list()
        pawn = self.__board.get_piece(coordinate)
        color = pawn.piece_color
        x, y = self.__board.get_coordinate(piece)
        opposite_color = {coordinate: "white" if pawn.piece_color == "black" else "black"}
        pos = {"white": (1, 2), "black": (-1, -2)}
        if piece.piece_type == 'p' and piece.piece_color == opposite_color[coordinate]:
            previous_position = self.__board.all_positions[len(self.__board.all_positions) - 2]
            for p in previous_position:
                try:
                    if p[1] == (x + pos[color][1], y) and p[0].piece_type == piece.piece_type and p[0].piece_color == piece.piece_color:
                        if self.__board.is_piece((x + pos[color][1], y)):
                            temp = self.__board.get_piece((x + pos[color][1], y))
                            if temp.piece_type != piece.piece_type or temp.piece_color != piece.piece_color:
                                en_passant_moves.append((x + pos[color][0], y))
                        else:
                            en_passant_moves.append((x + pos[color][0], y))
                except ValueError:
                    pass
        return en_passant_moves

    def en_passant_helper1(self, coordinate: tuple) -> list:
        x, y = coordinate
        if y <= 6:
            if self.__board.is_piece((x, y + 1)):
                piece = self.__board.get_piece((x, y + 1))
                return self.en_passant_helper2(coordinate, piece)

        if y >= 1:
            if self.__board.is_piece((x, y - 1)):
                piece = self.__board.get_piece((x, y - 1))
                return self.en_passant_helper2(coordinate, piece)
        return []

    def en_passant(self, coordinate: tuple) -> list:
        x, y = coordinate
        if (x == 4 and self.color_turn == "white") or (x == 3 and self.color_turn == "black"):
            return self.en_passant_helper1(coordinate)
        return []

    def __move_pawn_options(self, coordinate: tuple, same_color: bool = False) -> tuple:
        """
        Returns the list of coordinates that are available for
        the movement of the `pawn`.
        """
        all_possible_moves = list()
        move_options_list = list()
        piece = self.__board.get_piece(coordinate)
        x, y = coordinate
        if len(self.en_passant(coordinate)) and self.__set_attacked is True:
            if self.color_turn == "white":
                self.passant = (self.en_passant(coordinate)[0][0] - 1, self.en_passant(coordinate)[0][1])
            elif self.color_turn == "black":
                self.passant = (self.en_passant(coordinate)[0][0] + 1, self.en_passant(coordinate)[0][1])
            all_possible_moves = self.en_passant(coordinate)
            move_options_list = self.en_passant(coordinate)
        if self.color_turn == "white":
            if 1 <= x <= 6:
                all_possible_moves.append((x + 1, y))
                if x == 1:
                    all_possible_moves.append((x + 2, y))
                if not self.__board.is_piece((x + 1, y)):
                    move_options_list.append((x + 1, y))
                    if x == 1 and not self.__board.is_piece((x + 2, y)):
                        move_options_list.append((x + 2, y))
                if 7 >= y >= 1 and self.__board.is_piece((x + 1, y - 1)):
                    all_possible_moves.append((x + 1, y - 1))
                    if same_color:
                        move_options_list.append((x + 1, y - 1))
                    elif self.__board.get_piece((x + 1, y - 1)).piece_color != piece.piece_color:
                        move_options_list.append((x + 1, y - 1))
                if 0 <= y <= 6 and self.__board.is_piece((x + 1, y + 1)):
                    all_possible_moves.append((x + 1, y + 1))
                    if same_color:
                        move_options_list.append((x + 1, y + 1))
                    elif self.__board.get_piece((x + 1, y + 1)).piece_color != piece.piece_color:
                        move_options_list.append((x + 1, y + 1))
        else:
            if 1 <= x <= 6:
                all_possible_moves.append((x - 1, y))
                if x == 6:
                    all_possible_moves.append((x - 2, y))
                if not self.__board.is_piece((x - 1, y)):
                    move_options_list.append((x - 1, y))
                    if x == 6 and not self.__board.is_piece((x - 2, y)):
                        move_options_list.append((x - 2, y))
                if 7 >= y >= 1 and self.__board.is_piece((x - 1, y - 1)):
                    all_possible_moves.append((x - 1, y - 1))
                    if same_color:
                        move_options_list.append((x - 1, y - 1))
                    elif self.__board.get_piece((x - 1, y - 1)).piece_color != piece.piece_color:
                        move_options_list.append((x - 1, y - 1))
                if 0 <= y <= 6 and self.__board.is_piece((x - 1, y + 1)):
                    all_possible_moves.append((x - 1, y + 1))
                    if same_color:
                        move_options_list.append((x - 1, y + 1))
                    elif self.__board.get_piece((x - 1, y + 1)).piece_color != piece.piece_color:
                        move_options_list.append((x - 1, y + 1))

        return move_options_list, all_possible_moves

    def __can_promote(self, coordinate: tuple, new_coordinate: tuple) -> bool:
        return new_coordinate[0] in [0, 7] and new_coordinate in self.__move_pawn_options(coordinate)[0]

    def __promote(self, coordinate: tuple, new_coordinate: tuple) -> None:
        self.__board.remove_piece(coordinate)
        self.__board.place_piece(new_coordinate, Piece("queen", 'q', self.color_turn, True))

    def __move_knight_options(self, coordinate: tuple, same_color: bool = False) -> tuple:
        move_options_list = list()
        all_possible_moves = list()
        piece = self.__board.get_piece(coordinate)
        x, y = coordinate
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i != j != 0 != i and abs(i) + abs(j) == 3:
                    if 7 >= x + i >= 0 and 0 <= y + j <= 7:
                        all_possible_moves.append((x + i, y + j))
                        if same_color:
                            move_options_list.append((x + i, y + j))
                        else:
                            try:
                                if not self.__board.is_piece((x + i, y + j)) or self.__board.is_piece((x + i, y + j)) and self.__board.get_piece((x + i, y + j)).piece_color != piece.piece_color:
                                    move_options_list.append((x + i, y + j))
                            except IndexError:
                                pass
        return move_options_list, all_possible_moves

    def __move_bishop_options(self, coordinate: tuple, same_color: bool = False) -> tuple:
        move_options_list = list()
        all_possible_moves = list()
        piece = self.__board.get_piece(coordinate)
        x, y = coordinate
        up_left = up_right = down_left = down_right = True
        for i in range(1, 8):
            if 7 >= x + i >= 0 and 0 <= y + i <= 7:
                all_possible_moves.append((x + i, y + i))
                try:
                    if up_right:
                        if not self.__board.is_piece((x + i, y + i)):
                            move_options_list.append((x + i, y + i))
                        else:
                            if same_color:
                                move_options_list.append((x + i, y + i))
                            elif self.__board.get_piece((x + i, y + i)).piece_color != piece.piece_color:
                                move_options_list.append((x + i, y + i))
                            up_right = False
                except IndexError:
                    pass
            if 7 >= x - i >= 0 and 0 <= y - i <= 7:
                all_possible_moves.append((x - i, y - i))
                try:
                    if down_left:
                        if not self.__board.is_piece((x - i, y - i)):
                            move_options_list.append((x - i, y - i))
                        else:
                            if same_color:
                                move_options_list.append((x - i, y - i))
                            elif self.__board.get_piece((x - i, y - i)).piece_color != piece.piece_color:
                                move_options_list.append((x - i, y - i))
                            down_left = False
                except IndexError:
                    pass
            if 7 >= x + i >= 0 and 0 <= y - i <= 7:
                all_possible_moves.append((x + i, y - i))
                try:
                    if up_left:
                        if not self.__board.is_piece((x + i, y - i)):
                            move_options_list.append((x + i, y - i))
                        else:
                            if same_color:
                                move_options_list.append((x + i, y - i))
                            elif self.__board.get_piece((x + i, y - i)).piece_color != piece.piece_color:
                                move_options_list.append((x + i, y - i))
                            up_left = False
                except IndexError:
                    pass
            if 7 >= x - i >= 0 and 0 <= y + i <= 7:
                all_possible_moves.append((x - i, y + i))
                try:
                    if down_right:
                        if not self.__board.is_piece((x - i, y + i)):
                            move_options_list.append((x - i, y + i))
                        else:
                            if same_color:
                                move_options_list.append((x - i, y + i))
                            elif self.__board.get_piece((x - i, y + i)).piece_color != piece.piece_color:
                                move_options_list.append((x - i, y + i))
                            down_right = False
                except IndexError:
                    pass

        return move_options_list, all_possible_moves

    def __move_rook_options(self, coordinate: tuple, same_color: bool = False) -> tuple:
        move_options_list = list()
        all_possible_moves = list()
        piece = self.__board.get_piece(coordinate)
        x, y = coordinate
        up = down = left = right = True
        for i in range(1, 8):
            if 7 >= x + i >= 0 and 0 <= y <= 7:
                all_possible_moves.append((x + i, y))
                try:
                    if up:
                        if not self.__board.is_piece((x + i, y)):
                            move_options_list.append((x + i, y))
                        else:
                            if same_color:
                                move_options_list.append((x + i, y))
                            elif self.__board.get_piece((x + i, y)).piece_color != piece.piece_color:
                                move_options_list.append((x + i, y))
                            up = False
                except IndexError:
                    pass
            if 7 >= x - i >= 0 and 0 <= y <= 7:
                all_possible_moves.append((x - i, y))
                try:
                    if down:
                        if not self.__board.is_piece((x - i, y)):
                            move_options_list.append((x - i, y))
                        else:
                            if same_color:
                                move_options_list.append((x - i, y))
                            elif self.__board.get_piece((x - i, y)).piece_color != piece.piece_color:
                                move_options_list.append((x - i, y))
                            down = False
                except IndexError:
                    pass
            if 7 >= x >= 0 and 0 <= y + i <= 7:
                all_possible_moves.append((x, y + i))
                try:
                    if right:
                        if not self.__board.is_piece((x, y + i)):
                            move_options_list.append((x, y + i))
                        else:
                            if same_color:
                                move_options_list.append((x, y + i))
                            elif self.__board.get_piece((x, y + i)).piece_color != piece.piece_color:
                                move_options_list.append((x, y + i))
                            right = False
                except IndexError:
                    pass
            if 7 >= x >= 0 and 0 <= y - i <= 7:
                all_possible_moves.append((x, y - i))
                try:
                    if left:
                        if not self.__board.is_piece((x, y - i)):
                            move_options_list.append((x, y - i))
                        else:
                            if same_color:
                                move_options_list.append((x, y - i))
                            elif self.__board.get_piece((x, y - i)).piece_color != piece.piece_color:
                                move_options_list.append((x, y - i))
                            left = False
                except IndexError:
                    pass
        return move_options_list, all_possible_moves

    def __move_queen_options(self, coordinate: tuple, same_color: bool = False) -> tuple:
        return self.__move_bishop_options(coordinate, same_color)[0] + self.__move_rook_options(coordinate, same_color)[0], self.__move_bishop_options(coordinate, same_color)[1] + \
               self.__move_rook_options(coordinate, same_color)[1]

    def __move_king_options(self, coordinate: tuple, consider_castle: bool = True, same_color: bool = False) -> tuple:
        move_options_list = list()
        all_possible_moves = list()
        piece = self.__board.get_piece(coordinate)
        x, y = coordinate
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if 7 >= x + i >= 0 and 0 <= y + j <= 7:
                        all_possible_moves.append((x + i, y + j))
                        if same_color:
                            move_options_list.append((x + i, y + j))
                        else:
                            try:
                                if not self.__board.is_piece((x + i, y + j)) or self.__board.is_piece((x + i, y + j)) and self.__board.get_piece((x + i, y + j)).piece_color != piece.piece_color:
                                    move_options_list.append((x + i, y + j))
                            except IndexError:
                                pass
        if consider_castle:
            move_options_list += self.__castle_coordinates(coordinate)
        return move_options_list, all_possible_moves

    def is_protected(self, coordinate: tuple) -> bool:
        piece = self.__board.get_piece(coordinate)
        for p in self.__board.get_pieces(piece.piece_color):
            if coordinate in self.available_move_options(self.__board.get_coordinate(p), ignore_color=True, same_color=True):
                return True
        return False

    def is_square_attacked(self, coordinate: tuple, color: str) -> bool:
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    piece = self.__board.get_piece((i, j))
                    if piece.piece_color == color and coordinate in self.available_move_options((i, j), ignore_color=True, consider_castle=False):
                        return True
        return False

    def enemy_pieces_have_vision(self, king: Piece, enemy_color: str) -> list:
        vision = ['', '']
        x, y = self.__board.get_coordinate(king)
        for i in range(5, 7):
            if self.is_square_attacked((x, i), enemy_color):
                vision[0] = 'K'
        for i in range(1, 4):
            if self.is_square_attacked((x, i), enemy_color):
                vision[1] = 'q'
        return vision

    def __castle_options(self, coordinate: tuple) -> list:
        king = self.__board.get_piece(coordinate)
        result = ['', '']
        if king.piece_type == 'K' and king.has_moved is False:
            if not self.__board.get_piece((coordinate[0], 7)).has_moved:
                if not self.__board.is_piece((coordinate[0], 5)) and not self.__board.is_piece((coordinate[0], 6)):
                    result[0] = 'K'
            if not self.__board.get_piece((coordinate[0], 0)).has_moved:
                if not self.__board.is_piece((coordinate[0], 1)) and not self.__board.is_piece((coordinate[0], 2)) and not self.__board.is_piece((coordinate[0], 3)):
                    result[1] = 'q'
        return result

    def __castle_coordinates(self, coordinate: tuple) -> list:
        if self.check():
            return []
        move_options_list = list()
        piece = self.__board.get_piece(coordinate)
        opposite_color = {coordinate: "white" if self.color_turn == "black" else "black"}
        castle_options = self.__castle_options(coordinate)
        vision = self.enemy_pieces_have_vision(piece, opposite_color[coordinate])
        if castle_options[0] == 'K' and vision[0] == 'K':
            castle_options[0] = ''
        if castle_options[1] == 'q' and vision[1] == 'q':
            castle_options[1] = ''
        pos = {"white": 0, "black": 7}
        if castle_options[0] == 'K':
            move_options_list.append((pos[piece.piece_color], 6))
        if castle_options[1] == 'q':
            move_options_list.append((pos[piece.piece_color], 1))
            move_options_list.append((pos[piece.piece_color], 2))
        return move_options_list

    def __castle(self, coordinate: tuple, new_coordinate: tuple) -> dict:
        moves = dict()
        if new_coordinate[1] == 1:
            self.__board.update_piece_position(coordinate, (new_coordinate[0], 2))
            moves[coordinate] = (new_coordinate[0], 2)
        else:
            self.__board.update_piece_position(coordinate, new_coordinate)
            moves[coordinate] = new_coordinate
        if new_coordinate[1] in [1, 2]:
            self.__board.update_piece_position((coordinate[0], 0), (coordinate[0], 3))
            moves[(coordinate[0], 0)] = (coordinate[0], 3)
        elif new_coordinate[1] == 6:
            self.__board.update_piece_position((coordinate[0], 7), (coordinate[0], 5))
            moves[(coordinate[0], 7)] = (coordinate[0], 5)
        return moves

    def __is_draw_by_insufficient_material(self):
        white_pieces = self.__board.get_pieces("white")
        black_pieces = self.__board.get_pieces("black")
        if len(white_pieces) <= 2 and len(black_pieces) <= 2:
            if len(white_pieces) == 1 and len(black_pieces) == 1:
                return True
            if len(white_pieces) == 2 and len(black_pieces) == 1:
                if white_pieces[0].piece_type == 'K' and white_pieces[1].piece_type in ['k', 'b']:
                    return True
                if white_pieces[1].piece_type == 'K' and white_pieces[0].pice_type in ['k', 'b']:
                    return True
            if len(white_pieces) == 1 and len(black_pieces) == 2:
                if black_pieces[0].piece_type == 'K' and black_pieces[1].piece_type in ['k', 'b']:
                    return True
                if black_pieces[1].piece_type == 'K' and black_pieces[0].pice_type in ['k', 'b']:
                    return True
            if len(white_pieces) == 2 and len(black_pieces) == 2:
                if white_pieces[0].piece_type == 'K' and white_pieces[1].piece_type in ['k', 'b'] or white_pieces[1].piece_type == 'K' and white_pieces[0].piece_type in ['k', 'b']:
                    if black_pieces[0].piece_type == 'K' and black_pieces[1].pice_type in ['k', 'b']:
                        return True
                    if black_pieces[1].piece_type == 'K' and black_pieces[0].piece_type in ['k', 'b']:
                        return True
        return False

    def draw_the_game(self) -> None:
        if self.__is_draw_by_insufficient_material():
            self.draw = True

    def __set_attacked_pieces_by(self, coordinate: tuple) -> None:
        attacking_piece = self.__board.get_piece(coordinate)
        opposite_color = {coordinate: "white" if attacking_piece.piece_color == "black" else "black"}
        attacked_coordinates = self.available_move_options(coordinate, ignore_color=True)
        for coord in attacked_coordinates:
            if self.__board.is_piece(coord) and self.__board.get_piece(coord).piece_color == opposite_color[coordinate]:
                piece = self.__board.get_piece(coord)
                piece.attacking_pieces = attacking_piece

    def set_attacked_pieces(self) -> None:
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    piece = self.__board.get_piece((i, j))
                    pieces = list()
                    for attacking_piece in piece.attacking_pieces:
                        pieces.append(attacking_piece)
                    for p in pieces:
                        piece.remove_attacking_piece(p)
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    self.__set_attacked_pieces_by((i, j))

    def check(self) -> str:
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    piece = self.__board.get_piece((i, j))
                    if piece.piece_type == 'K' and piece.attacking_pieces.keys():
                        return piece.piece_color

    def get_coordinates_that_moves_king_out_of_check(self, king: Piece, moves: list) -> list:
        good_moves = list()
        attacking_pieces = king.attacking_pieces.keys()
        for piece in attacking_pieces:
            candidate_moves = list()
            attacking_moves = self.available_move_options(self.__board.get_coordinate(piece), ignore_color=True, option=1)
            for move in moves:
                if move not in attacking_moves:
                    candidate_moves.append(move)
            if not len(good_moves):
                good_moves += candidate_moves
            else:
                good_moves = list(set(good_moves).intersection(set(candidate_moves)))
        moves_place_king_check = self.moves_that_place_king_in_check(self.__board.get_coordinate(king))
        if len(moves_place_king_check):
            good_moves = list(set(good_moves).difference(set(moves_place_king_check)))
        return good_moves

    def block_check(self, king: Piece, coordinate: tuple) -> list:
        good_moves = list()
        available_moves = self.available_move_options(coordinate, ignore_color=True)
        attacking_pieces = king.attacking_pieces.keys()
        for piece in attacking_pieces:
            candidate_moves = list()
            for move in available_moves:
                if move in self.__board.get_path(self.__board.get_coordinate(king), self.__board.get_coordinate(piece)):
                    candidate_moves.append(move)
            if not len(good_moves):
                good_moves += candidate_moves
            else:
                good_moves = list(set(good_moves).intersection(set(candidate_moves)))
        moves_place_king_check = self.moves_that_place_king_in_check(self.__board.get_coordinate(self.__board.get_piece(coordinate)))
        if len(moves_place_king_check):
            good_moves = list(set(good_moves).difference(set(moves_place_king_check)))
        return good_moves

    def capture_checking_piece(self, king: Piece, coordinate: tuple) -> list:
        if self.moves_that_place_king_in_check(coordinate):
            return []
        good_moves = list()
        available_moves = self.available_move_options(coordinate, ignore_color=True)
        attacking_pieces = king.attacking_pieces.keys()
        for piece in attacking_pieces:
            candidate_moves = list()
            if self.__board.get_coordinate(piece) in available_moves:
                candidate_moves.append(self.__board.get_coordinate(piece))
            if not len(good_moves):
                good_moves += candidate_moves
            else:
                good_moves = list(set(good_moves).intersection(set(candidate_moves)))
        moves_place_king_check = self.moves_that_place_king_in_check(self.__board.get_coordinate(self.__board.get_piece(coordinate)))
        if len(moves_place_king_check):
            good_moves = list(set(good_moves).difference(set(moves_place_king_check)))
        return good_moves

    def check_options(self, coordinate: tuple) -> list:
        valid_moves = list()
        piece = self.__board.get_piece(coordinate)
        available_moves = self.available_move_options(coordinate)
        if piece.piece_type == 'K' and piece.piece_color == self.check():
            valid_moves += self.get_coordinates_that_moves_king_out_of_check(piece, available_moves)
        elif piece.piece_color == self.check():
            for i in range(8):
                for j in range(8):
                    king = self.__board.get_piece((i, j))
                    if king.piece_type == 'K' and king.piece_color == self.color_turn:
                        valid_moves += self.block_check(king, coordinate)
                        valid_moves += self.capture_checking_piece(king, coordinate)
        return valid_moves

    def all_legal_moves_check(self, king: Piece) -> list:
        in_check_moves = list()
        for i in range(8):
            for j in range(8):
                piece = self.__board.get_piece((i, j))
                if self.__board.is_piece((i, j)) and piece.piece_color != self.color_turn:
                    candidate_moves = list()
                    if self.is_protected((i, j)) and (i, j) in self.available_move_options(self.__board.get_coordinate(king), ignore_color=True):
                        candidate_moves.append((i, j))
                    for move in self.available_move_options((i, j), ignore_color=True):
                        if move in self.available_move_options(self.__board.get_coordinate(king)):
                            candidate_moves.append(move)
                    if not len(in_check_moves):
                        in_check_moves += candidate_moves
                    else:
                        in_check_moves = list(set(in_check_moves).union(set(candidate_moves)))
        return in_check_moves

    def all_possible_attacking_moves_check(self, king: Piece) -> list:
        in_check_moves = list()
        attacking_pieces = king.attacking_pieces.keys()
        for piece in attacking_pieces:
            coordinate = self.__board.get_coordinate(piece)
            candidate_moves = list()
            if self.is_protected(coordinate) and coordinate in self.available_move_options(self.__board.get_coordinate(king), ignore_color=True):
                candidate_moves.append(coordinate)
            for move in self.available_move_options(self.__board.get_coordinate(piece), ignore_color=True, option=1):
                if move in self.available_move_options(self.__board.get_coordinate(king)):
                    candidate_moves.append(move)
            if not len(in_check_moves):
                in_check_moves += candidate_moves
            else:
                in_check_moves = list(set(in_check_moves).union(set(candidate_moves)))
        return in_check_moves

    def check_pinned_pieces(self, king: Piece, coordinate: tuple) -> list:
        for i in range(8):
            for j in range(8):
                piece = self.__board.get_piece((i, j))
                if self.__board.is_piece((i, j)) and piece.piece_color != self.color_turn and piece.piece_type not in ['p', 'k', 'K']:
                    path = self.__board.get_path(self.__board.get_coordinate(king), (i, j))
                    if coordinate in path:
                        for coord in path:
                            if coordinate != coord and self.__board.is_piece(coord):
                                return []
                        moves = list()
                        if self.available_move_options(coordinate, ignore_color=True):
                            for move in self.available_move_options(coordinate, ignore_color=True):
                                if self.__board.get_coordinate(king) in self.available_move_options((i, j), ignore_color=True, option=1):
                                    if move not in path and move != (i, j):
                                        moves.append(move)
                        return moves
        return []

    def moves_that_place_king_in_check(self, coordinate: tuple) -> list:
        piece = self.__board.get_piece(coordinate)
        king = None
        for i in range(8):
            for j in range(8):
                if self.__board.get_piece((i, j)).piece_type == 'K' and self.__board.get_piece((i, j)).piece_color == self.color_turn:
                    king = self.__board.get_piece((i, j))
        if piece.piece_type == 'K':
            in_check_moves = list()
            in_check_moves += self.all_legal_moves_check(king)
            if self.check():
                in_check_moves += self.all_possible_attacking_moves_check(king)
            return in_check_moves
        else:
            return self.check_pinned_pieces(king, coordinate)

    def is_checkmate(self) -> bool:
        color = self.check()
        if color:
            for i in range(8):
                for j in range(8):
                    if self.__board.is_piece((i, j)) and self.__board.get_piece((i, j)).piece_color == color:
                        if len(self.check_options((i, j))):
                            return False
            return True
        return False

    def can_pieces_move(self, color: str) -> bool:
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    piece = self.__board.get_piece((i, j))
                    if piece.piece_type != 'K' and piece.piece_color == color and len(self.available_move_options((i, j), ignore_color=True)):
                        return True
        return False

    def is_stalemate(self) -> bool:
        king = None
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    piece = self.__board.get_piece((i, j))
                    if piece.piece_color == self.color_turn and piece.piece_type == 'K':
                        king = piece
        if not self.check() and not self.can_pieces_move(self.color_turn):
            moves1 = self.moves_that_place_king_in_check(self.__board.get_coordinate(king))
            moves2 = self.available_move_options(self.__board.get_coordinate(king), ignore_color=True)
            if len(set(moves1)) != len(set(moves2)):
                return False
            for move in moves1:
                if move not in moves2:
                    return False
            for move in moves2:
                if move not in moves1:
                    return False
            return True
        return False

    def save_position(self) -> None:
        self.__board.save_position()

    def three_fold_repetition(self) -> bool:
        return self.color_turn == "black" and self.__board.three_fold_repetition()

    def remove_piece(self, coordinate: tuple) -> Piece:
        return self.__board.remove_piece(coordinate)

    def available_move_options(self, coordinate: tuple, ignore_color: bool = False, option: int = 0, same_color: bool = False, consider_castle: bool = True) -> list:
        """
        Returns the list of coordinates that the piece placed on
        the `coordinates` can move on, if any.
        """
        if not self.__can_move(coordinate) and not ignore_color:
            return []
        piece = self.__board.get_piece(coordinate)
        if piece.piece_type == "p":
            return self.__move_pawn_options(coordinate, same_color)[option]
        elif piece.piece_type == "k":
            return self.__move_knight_options(coordinate, same_color)[option]
        elif piece.piece_type == "b":
            return self.__move_bishop_options(coordinate, same_color)[option]
        elif piece.piece_type == "r":
            return self.__move_rook_options(coordinate, same_color)[option]
        elif piece.piece_type == "q":
            return self.__move_queen_options(coordinate, same_color)[option]
        elif piece.piece_type == "K":
            return self.__move_king_options(coordinate, consider_castle=consider_castle, same_color=same_color)[option]

    def move(self, coordinate: tuple, new_coordinate: tuple) -> dict:
        """
        Moves the piece that is on `coordinates` to `new_coordinates` if
        possible.
        """
        self.__draw_temp = self.__draw
        self.passant_temp = self.passant
        moves = dict()
        if new_coordinate in self.available_move_options(coordinate) and not self.draw:
            if self.check():
                if new_coordinate in self.check_options(coordinate) and new_coordinate not in self.moves_that_place_king_in_check(coordinate):
                    self.__board.update_piece_position(coordinate, new_coordinate)
                    moves[coordinate] = new_coordinate
                else:
                    raise CantMoveError("Piece cannot move")
            elif new_coordinate in self.moves_that_place_king_in_check(coordinate):
                raise CantMoveError("Piece cannot move")
            elif new_coordinate in self.__castle_coordinates(coordinate):
                moves = self.__castle(coordinate, new_coordinate)
            elif self.__can_promote(coordinate, new_coordinate):
                self.__promote(coordinate, new_coordinate)
                moves[coordinate] = new_coordinate
            else:
                if self.passant:
                    self.__board.remove_piece(self.passant)
                    self.passant_coordinate = self.passant
                    self.is_passant = True
                    self.passant = None
                self.__board.update_piece_position(coordinate, new_coordinate)
                moves[coordinate] = new_coordinate

            self.__set_attacked = False
            self.set_attacked_pieces()
            self.__set_attacked = True
            if self.color_turn == "white":
                self.color_turn = "black"
            else:
                self.color_turn = "white"
            self.save_position()
            return moves
        raise CantMoveError("Piece cannot move")

    def get_all_legal_moves(self):
        moves = list()
        for i in range(8):
            for j in range(8):
                if self.__board.is_piece((i, j)):
                    piece = self.__board.get_piece((i, j))
                    if self.color_turn == piece.piece_color:
                        if len(self.available_move_options((i, j))):
                            moves.append({(i, j): self.available_move_options((i, j))})
        return moves

    def undo_move(self) -> None:
        previous_position = self.board.all_positions[len(self.board.all_positions) - 2]
        for i in range(8):
            for j in range(8):
                if self.board.is_piece((i, j)):
                    self.board.remove_piece((i, j))
        for p in previous_position:
            if p[0] is not None and p[1] is not None:
                piece = p[0]
                coordinate = p[1]
                self.board.place_piece(coordinate, piece)
        del self.board.all_positions[len(self.board.all_positions) - 1]

        self.__draw = self.__draw_temp
        self.passant = self.passant_temp
        self.__set_attacked = False
        self.set_attacked_pieces()
        self.__set_attacked = True
        if self.color_turn == "white":
            self.color_turn = "black"
        else:
            self.color_turn = "white"
