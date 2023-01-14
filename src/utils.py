from typing import Tuple
from urllib.parse import unquote


class PositionToCssSelector:
    SELECTOR_VALUE = ".square-{row}{col}"
    HINT_SELECTOR_VALUE = ".square-{row}{col}"
    MAPPING_ALPHABET_TO_DIGIT = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
    }

    @classmethod
    def to_css_selector(cls, position: str) -> str:
        row = cls.MAPPING_ALPHABET_TO_DIGIT.get(position[0])
        col = position[1]
        return cls.SELECTOR_VALUE.format(row=row, col=col)

    @classmethod
    def to_hint_selector(cls, position: str) -> str:
        row = cls.MAPPING_ALPHABET_TO_DIGIT.get(position[0])
        col = position[1]
        return cls.HINT_SELECTOR_VALUE.format(row=row, col=col)


class Utils:
    @staticmethod
    def url_decode(string: str) -> str:
        return unquote(string=string)

    @staticmethod
    def to_xy(position: str) -> Tuple[int, int]:
        x = int(position[0]) - 1
        y = int(position[1]) - 1
        return x, y
