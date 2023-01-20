from __future__ import annotations

import re

from stockfish import Stockfish

from src.board import ChessBoard
from src.configs import BaseFen
from src.configs import BasePattern
from src.configs import BaseStockFishConfig
from src.utils import Utils


class Chess:
    def __init__(self, is_white: bool = True):
        self._stockfish = Stockfish(
            path=BaseStockFishConfig.PATH,
            depth=BaseStockFishConfig.DEPTH,
            parameters=BaseStockFishConfig.PARAMETERS,
        )
        self._move_list = []
        self._is_white = is_white

    def reset(self):
        self._stockfish.set_fen_position(BaseFen.START)

    def set_move(self, move: str):
        if move and self._stockfish.is_move_correct(move_value=move):
            self._move_list.append(move)
            self._stockfish.set_position(self._move_list)
            print(self._move_list)
            return True
        return False

    def get_best_move(self):
        return self._stockfish.get_best_move(
            wtime=BaseStockFishConfig.WTIME, btime=BaseStockFishConfig.BTIME
        )

    def set_skill_level(self, skill_level: int = 20):
        self._stockfish.set_skill_level(skill_level=skill_level)

    def get_computer_move(self, pieces: list):
        previous_board = self.create_board_from_stock_fish(
            stock_fish=self._stockfish,
        )
        current_board = self.create_board_from_pieces(pieces=pieces)
        computer_move = self.compare_to_board(
            previous_board=previous_board,
            current_board=current_board,
            is_white=self._is_white,
        )
        return computer_move

    @classmethod
    def compare_to_board(
        cls,
        previous_board: ChessBoard,
        current_board: ChessBoard,
        is_white: bool = True,
    ) -> str:
        previous_data = previous_board.get_board()
        current_data = current_board.get_board()
        from_position = ""
        to_position = ""
        is_current_castling = cls.is_current_castling(
            previous_data=previous_data,
            current_data=current_data,
            is_white=is_white,
        )
        # Handle when castling
        if is_current_castling:
            is_compute_white = not is_white
            if is_compute_white:
                if current_data[0][6] == "K":
                    from_position = "e1"
                    to_position = "g1"
                else:
                    from_position = "e1"
                    to_position = "c1"
            else:
                if current_data[7][6] == "k":
                    from_position = "e8"
                    to_position = "g8"
                else:
                    from_position = "e8"
                    to_position = "c8"

            return from_position + to_position

        # Not castling
        for i in range(8):
            for j in range(8):
                if previous_data[i][j] != current_data[i][j]:
                    # Get from position
                    if current_data[i][j] == "":
                        from_position = Utils.to_square(x=j, y=i)

                    # Get to position
                    if current_data[i][j] != "":
                        to_position = Utils.to_square(x=j, y=i)
        return from_position + to_position

    @classmethod
    def is_current_castling(
        cls, previous_data: list, current_data: list, is_white: bool = True
    ) -> bool:
        is_checking_white = not is_white
        if is_checking_white:
            if previous_data[0][4] == "K" and current_data[0][6] == "K":
                return True
            if previous_data[0][4] == "K" and current_data[0][2] == "K":
                return True
        else:
            if previous_data[7][4] == "k" and current_data[7][6] == "k":
                return True
            if previous_data[7][4] == "k" and current_data[7][2] == "k":
                return True
        return False

    @classmethod
    def create_board_from_pieces(cls, pieces: list) -> ChessBoard:
        board = ChessBoard()
        for piece in pieces:
            piece_string = piece.get_attribute("class")
            match = re.search(pattern=BasePattern.CHESS, string=piece_string)
            if match:
                class_name = match.group("chess")
            else:
                continue
            if not class_name:
                print(piece.get_attribute("class"))
            class_chess = class_name[:1]
            if class_chess == "b":
                type_chess = class_name[1:2]
            else:
                type_chess = class_name[1:2].upper()
            pos = re.search(
                pattern=BasePattern.SQUARE,
                string=piece_string,
            ).group("square")
            board.add_chess(chess=type_chess, pos=pos)

        return board

    @classmethod
    def create_board_from_stock_fish(cls, stock_fish: Stockfish) -> ChessBoard:
        board = ChessBoard()
        for i in range(8):
            for j in range(8):
                square = Utils.to_square(x=i, y=j)
                piece_as_char = stock_fish.get_what_is_on_square(square=square)
                piece_as_char = piece_as_char.value if piece_as_char else ""
                pos = Utils.to_position(x=i, y=j)
                board.add_chess(chess=piece_as_char, pos=pos)
        return board
