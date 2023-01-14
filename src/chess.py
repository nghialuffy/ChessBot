from stockfish import Stockfish

from src.configs import BaseStockFishConfig, BaseFen


class Chess:
    def __init__(self):
        self._stockfish = Stockfish(
            path=BaseStockFishConfig.PATH,
            depth=BaseStockFishConfig.DEPTH,
            parameters=BaseStockFishConfig.PARAMETERS
        )

    def reset(self):
        self._stockfish.set_fen_position(BaseFen.START)

    def set_fen_position(self, fen_position):
        should_set = fen_position and self._stockfish.is_fen_valid(fen=fen_position)
        if should_set:
            self._stockfish.set_fen_position(fen_position)
            return True
        return False

    def get_best_move(self):
        return self._stockfish.get_best_move(wtime=BaseStockFishConfig.WTIME, btime=BaseStockFishConfig.BTIME)

    def set_position(self, move):
        should_move = move and self._stockfish.is_move_correct(move_value=move)
        if should_move:
            self._stockfish.set_position(move)

    def set_master_level(self):
        self._stockfish.set_skill_level(20)
