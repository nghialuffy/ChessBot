from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions, FirefoxProfile, Firefox, Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import pickle, time, re
from urllib.parse import unquote
from typing import Tuple

from src.configs import BaseConfig, BaseXpath, BasePattern
from src.fen import FenService
from src.utils import PositionToCssSelector, Utils


class WebDriver:
    def __init__(self, name: str, path: str, log: str):
        self._name = name
        self._path = path
        self._log = log
        self._driver = None

    def start_browser(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"user-data-dir={self._name}_user")
        chrome_options.add_argument("window-size=1400,1000")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
        chrome_options.add_argument("Cache-Control=no-cache")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--dns-prefetch-disable')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.page_load_strategy = 'none'
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self._driver = webdriver.Chrome(executable_path=self._path, options=chrome_options)

    def get(self, url: str):
        self._driver.get(url)

    def get_element_by_xpath(self, xpath: str) -> WebElement:
        wait = WebDriverWait(self._driver, BaseConfig.WAIT_FIND_TIME)
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return self._driver.find_element(By.XPATH, xpath)

    def get_element_by_css_selector(self, css_selector: str) -> WebElement:
        wait = WebDriverWait(self._driver, BaseConfig.WAIT_FIND_TIME)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        return self._driver.find_element(By.CSS_SELECTOR, css_selector)

    def move_chess(self, move: str):
        actions = ActionChains(driver=self._driver)
        from_pos = move[:2]
        to_pos = move[2:]
        from_selector = PositionToCssSelector.to_css_selector(position=from_pos)
        to_selector = PositionToCssSelector.to_hint_selector(position=to_pos)

        from_element = self.get_element_by_css_selector(css_selector=from_selector)
        from_element.click()

        time.sleep(BaseConfig.WAIT_CLICK_TIME)
        to_element = self.get_element_by_css_selector(css_selector=to_selector)
        actions.move_to_element(to_element).click_and_hold(to_element).perform()

    def get_fen_position(self, is_white: bool = True) -> str:
        fen_position = ""
        pieces = self.get_all_pieces()
        if pieces:
            fen_service = FenService(pieces=pieces, is_white=is_white)
            fen_service.handle()
            # fen_service.print_board()
            fen_position = fen_service.get_fen()
        return fen_position

    def get_all_pieces(self):
        wait = WebDriverWait(self._driver, BaseConfig.WAIT_FIND_TIME)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, BaseConfig.PEACE)))
        return self._driver.find_elements(By.CLASS_NAME, BaseConfig.PEACE)

    def close(self):
        self._driver.close()
