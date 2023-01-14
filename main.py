from src.chess import Chess
from src.configs import BaseConfig
from src.webdriver import WebDriver


if "__main__" == __name__:
    driver = WebDriver(name=BaseConfig.NAME, path=BaseConfig.PATH, log=BaseConfig.LOG_PATH)
    driver.start_browser()
    driver.get(url=BaseConfig.CHESS_URL)
    chess = Chess()
    while True:
        try:
            input("Press Enter to continue...")
            fen_position = driver.get_fen_position()
            print(fen_position)
            is_set = chess.set_fen_position(fen_position=fen_position)
            if is_set:
                best_move = chess.get_best_move()
                print(best_move)
                driver.move_chess(move=best_move)
        except Exception as exc:
            choose = input("Continue or Break: (c/b)")
            if choose.lower() == "c":
                continue
            else:
                print(exc)
                if driver:
                    driver.close()
                break
