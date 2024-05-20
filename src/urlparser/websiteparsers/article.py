
from datetime import datetime


class Article:
    def __init__(self) -> None:
        self.text: str = []
        self.date: datetime = None
        self.tokens: list[str] = None