from datetime import datetime
from threading import Thread, Event

from .exceptions import AlreadyRunningException

from urlparser.websiteparsers import * 

class ArticleLoader:
    
    __running_loader = Thread()

    __need_to_stop = Event()

    __website_parsers: list[BaseParser] = [CommersantParser, MkParser, RiaParser]

    @staticmethod
    def load_articles(begin_date: datetime, end_date: datetime):
        if __class__.running_loader.is_alive():
            raise AlreadyRunningException()
        
