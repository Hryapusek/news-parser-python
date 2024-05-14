from abc import ABC, abstractmethod
from datetime import datetime


class BaseParser(ABC):

    prefix = "Base"

    @staticmethod
    @abstractmethod
    def load_articles_urls(begin_date: datetime, end_date: datetime, stop_sign = None) \
                        -> dict[datetime, list[str]]:
        pass
