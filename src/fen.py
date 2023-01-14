import re

from src.configs import BasePattern
from src.utils import Utils


class KingMove:
    white = False
    black = False


class FenService:
    def __init__(self, pieces: list, is_white: bool = True):
        self._pieces = pieces
        self._board = []
        self._is_white = is_white
        self._init_board()

    def _init_board(self):
        for i in range(8):
            self._board.append([])
            for j in range(8):
                self._board[i].append("")

    def print_board(self):
        if self._is_white:
            row_range = range(8, 0, -1)
        else:
            row_range = range(1, 9)
        for i in row_range:
            for j in range(8, 0, -1):
                print(self._board[i-1][j-1] or " ", end=" ")
            print("")

    def _add_chess(self, chess: str, pos: str):
        x, y = Utils.to_xy(pos)
        self._board[y][x] = chess

    def handle(self):
        for piece in self._pieces:
            piece_string = piece.get_attribute("class")
            class_name = re.search(pattern=BasePattern.CHESS, string=piece_string).group("chess")
            class_chess = class_name[:1]
            if class_chess == "b":
                type_chess = class_name[1:2]
            else:
                type_chess = class_name[1:2].upper()
            pos = re.search(pattern=BasePattern.SQUARE, string=piece_string).group("square")
            self._add_chess(chess=type_chess, pos=pos)

    def get_fen(self):
        fen = ""
        for i in range(8, 0, -1):
            count = 0
            for j in range(8):
                if self._board[i-1][j]:
                    if count > 0:
                        fen += str(count)
                        count = 0
                    fen += self._board[i-1][j]
                else:
                    count += 1
            if count > 0:
                fen += str(count)
            if i > 1:
                fen += "/"
        if self._is_white:
            fen += " w"
        else:
            fen += " b"

        white_king = ""
        if not KingMove.white:
            if self._board[0][4] == "K" and self._board[0][7] == "R":
                white_king += "K"
            if self._board[0][4] == "K" and self._board[0][0] == "R":
                white_king += "Q"
            KingMove.white = not bool(white_king)

        black_king = ""
        if not KingMove.black:
            if self._board[7][4] == "k" and self._board[7][7] == "r":
                black_king += "k"
            if self._board[7][4] == "k" and self._board[7][0] == "r":
                black_king += "q"
            KingMove.black = not bool(black_king)
        if white_king:
            fen += " " + (white_king or " - ") + (black_king or " - ") + " "
        else:
            fen += " " + (black_king or " - ") + (white_king or " - ") + " "
        # TODO: handle when castling
        return fen
