from src.chess import Chess
from src.configs import BaseConfig
from src.webdriver import WebDriver


if "__main__" == __name__:
    driver = WebDriver(name=BaseConfig.NAME, path=BaseConfig.PATH, log=BaseConfig.LOG_PATH)
    driver.start_browser()
    driver.get(url=BaseConfig.CHESS_URL)
    chess = Chess()
    is_white = True
    input("Press Enter to start game...")
    while True:
        try:
            if is_white:
                best_move = chess.get_best_move()
                is_valid = chess.set_move(best_move)
                print("Best move: ", best_move)
                if is_valid:
                    driver.move_chess(move=best_move)
            is_white = True
            while True:
                next_step = input("Input next step: ")
                if chess.set_move(next_step):
                    break

        except Exception as exc:
            choose = input("Continue or Break: (c/b)")
            if choose.lower() == "c":
                continue
            else:
                print(exc)
                if driver:
                    driver.close()
                break
