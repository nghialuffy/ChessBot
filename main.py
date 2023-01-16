from __future__ import annotations

import time

from src.chess import Chess
from src.configs import BaseConfig
from src.webdriver import WebDriver


if "__main__" == __name__:
    driver = WebDriver(
        name=BaseConfig.NAME,
        path=BaseConfig.PATH,
        log=BaseConfig.LOG_PATH,
    )
    driver.start_browser()
    driver.get(url=BaseConfig.CHESS_URL)
    input("Press Enter to start game...")
    while True:
        try:
            is_white_str = input("Is white? (y/n): ")
            is_white = is_white_str.lower() == "y"
            chess = Chess(is_white=is_white)
            level = int(input("Level (1-20): "))
            chess.set_skill_level(skill_level=level)
            input("Press Enter to start auto play chess...")
            while True:
                if is_white:
                    # Move chess
                    best_move = chess.get_best_move()
                    print("Bot will move: ", best_move)
                    is_valid = chess.set_move(move=best_move)
                    if is_valid:
                        driver.move_chess(move=best_move)

                    time.sleep(BaseConfig.WAIT_CLICK_TIME)
                    # Get computer move
                    retry = 50
                    while True:
                        retry -= 1
                        pieces = driver.get_all_pieces()
                        computer_move = chess.get_computer_move(pieces=pieces)
                        if retry == 1:
                            computer_move = input(
                                "Please input computer move: ",
                            )
                            retry = 50
                        is_computer_move_valid = chess.set_move(
                            move=computer_move,
                        )
                        if is_computer_move_valid:
                            print("Computer move: ", computer_move)
                            break
                else:
                    # Get computer move
                    retry = 50
                    while True:
                        retry -= 1
                        pieces = driver.get_all_pieces()
                        computer_move = chess.get_computer_move(pieces=pieces)
                        if retry == 1:
                            computer_move = input(
                                "Please input computer move: ",
                            )
                            retry = 50
                        is_computer_move_valid = chess.set_move(
                            move=computer_move,
                        )
                        if is_computer_move_valid:
                            print("Computer move: ", computer_move)
                            break

                    time.sleep(BaseConfig.WAIT_CLICK_TIME)
                    # Move chess
                    best_move = chess.get_best_move()
                    print("Bot will move: ", best_move)
                    is_valid = chess.set_move(move=best_move)
                    if is_valid:
                        driver.move_chess(move=best_move)

                # Wait for next move
                time.sleep(BaseConfig.WAIT_CLICK_TIME)
        except Exception as exc:
            print(exc)
            choose = input("Continue or Break: (c/b): ")
            if choose.lower() == "c":
                continue
            else:
                if driver:
                    driver.close()
                break
