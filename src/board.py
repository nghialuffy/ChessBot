from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from src.utils import Utils


@dataclass
class ChessBoard:
    data: list[list] = field(default_factory=list)
    is_white = True

    def __post_init__(self):
        self.init_board()

    def init_board(self):
        for i in range(8):
            self.data.append([])
            for j in range(8):
                self.data[i].append("")

    def print_board(self):
        if self.is_white:
            row_range = range(8, 0, -1)
        else:
            row_range = range(1, 9)
        for i in row_range:
            for j in range(8, 0, -1):
                print(self.data[i - 1][j - 1] or " ", end=" ")
            print("")

    def add_chess(self, chess: str, pos: str):
        x, y = Utils.to_xy(pos)
        self.data[y][x] = chess

    def get_board(self):
        return self.data
