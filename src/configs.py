class BaseConfig:
    NAME = "chess"
    PATH = "/usr/local/bin/chromedriver"
    LOG_PATH = "logs"
    CHESS_URL = "https://www.chess.com/play/computer"
    WAIT_FIND_TIME = 5
    WAIT_CLICK_TIME = 1


class BasePattern:
    FEN = "fen=(?P<fen>.*)&board"


class BaseXpath:
    SHARE = "/html/body/div[3]/div/div[3]/div[2]/div[1]/button[2]"
    FEN = '//*[@id="board-layout-chessboard"]/div[7]/div[2]/div/div/section/div[2]/a'
    CLOSE = "/html/body/div[2]/div[2]/div[7]/div[2]/div/button"


class BaseStockFishConfig:
    PATH = "stockfish_src/stockfish_15.1_x64_bmi2"
    DEPTH = 18
    WTIME = 1000
    BTIME = 1000
    PARAMETERS = {
        "Debug Log File": "",
        "Contempt": 0,
        "Min Split Depth": 0,
        "Threads": 2,
        "Ponder": "false",
        "Hash": 32,
        "MultiPV": 1,
        "Skill Level": 20,
        "Move Overhead": 10,
        "Minimum Thinking Time": 20,
        "Slow Mover": 100,
        "UCI_Chess960": "false",
        "UCI_LimitStrength": "false",
        "UCI_Elo": 1350
    }


class BaseFen:
    START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
