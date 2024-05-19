import asyncio
import os
from datetime import datetime, timedelta
from threading import Thread, Event
from concurrent.futures import Future, ThreadPoolExecutor
import threading

from urlparser.parse_tools import URLLoader
from urlparser.websiteparsers.article import Article
from utils.utils import daterange

from .exceptions import AlreadyRunningException

from urlparser.websiteparsers import * 

class ArticleLoader:

    ARTICLES_FOLDER = os.path.join(os.path.curdir, "articles")
    ARTICLE_FILENAME_TEMPLATE = "article_%s.txt"
    ARTICLE_DATE_DIRECTORY_TEMPLATE = "%Y_%m_%d"

    __running_loader = Thread()

    __need_to_stop = Event()

    __website_parsers: list[BaseParser] = [CommersantParser, MkParser, RiaParser]

    __date_articles: dict[datetime, Article] = {}

    @staticmethod
    def load_articles_from_internet(begin_date: datetime, end_date: datetime):
        if __class__.__running_loader.is_alive():
            raise AlreadyRunningException()
        __class__.__need_to_stop.clear()
        __class__.__running_loader = Thread(target=ArticleLoader.__load_articles_from_internet, args=(begin_date, end_date))
        __class__.__running_loader.start()

    @staticmethod
    def wait_for_finish():
        __class__.__running_loader.join()

    @staticmethod
    def __load_articles_from_internet(begin_date: datetime, end_date: datetime):
        date_url: dict[datetime, set] = {}
        for parser in __class__.__website_parsers:
            if __class__.__need_to_stop.is_set():
                return
            result = parser.load_articles_urls(begin_date, end_date)
            if __class__.__need_to_stop.is_set():
                return
            for date in result:
                if date not in date_url:
                    date_url[date] = set()
                date_url[date] = date_url[date].union(result[date])
        __class__.__write_to_files(date_url)
        __class__.__read_from_files(begin_date, end_date)

    @staticmethod
    def __read_from_files(begin_date: datetime, end_date: datetime):
        date_articles = {}
        for current_date in daterange(begin_date, end_date + timedelta(1)):
            current_date_directory = os.path.join(__class__.ARTICLES_FOLDER, current_date.strftime(__class__.ARTICLE_DATE_DIRECTORY_TEMPLATE))
            if not os.path.isdir(current_date_directory):
                # TODO: log later
                continue
            date_articles[current_date] = []
            for file in os.listdir(current_date_directory):
                with open(os.path.join(current_date_directory, file), encoding="utf-16") as article_file:
                    article = Article()
                    article.date = current_date
                    article.text = article_file.read().strip()
                    date_articles[current_date].append(article)
        __class__.__date_articles = date_articles
            
    def process_url(filename, url, current_date_directory):
        if __class__.__need_to_stop.is_set(): return
        import time
        start_time = time.time()
        try:
            text = URLLoader.load_text_from_url(url)
        except Exception:
            try:
                text = URLLoader.load_text_from_url(url)
            except Exception:
                print(f"Failed to load text from URL after retrying, elapsed time: {time.time() - start_time:.2f} seconds")
                return
        print(f"Successfully loaded text from URL, elapsed time: {time.time() - start_time:.2f} seconds")
        if __class__.__need_to_stop.is_set(): return
        if not text:
            return
        with open(os.path.join(current_date_directory, filename), "w", encoding="utf-16") as file:
            file.write(text)

    @staticmethod
    def __write_to_files(date_url):
        if not os.path.isdir(__class__.ARTICLES_FOLDER):
            os.mkdir(__class__.ARTICLES_FOLDER)
        for date in date_url:
            current_date_directory = os.path.join(__class__.ARTICLES_FOLDER, date.strftime(__class__.ARTICLE_DATE_DIRECTORY_TEMPLATE))
            counter = 0
            if not os.path.isdir(current_date_directory):
                os.mkdir(current_date_directory)
            
            with ThreadPoolExecutor(os.cpu_count()) as pool:
                futures: list[Future] = []
                for url in date_url[date]:
                    if __class__.__need_to_stop.is_set(): break
                    filename = __class__.ARTICLE_FILENAME_TEMPLATE % (counter)
                    while os.path.isfile(os.path.join(current_date_directory, filename)):
                        counter += 1
                        filename = __class__.ARTICLE_FILENAME_TEMPLATE % (counter)
                    counter += 1
                    futures.append(pool.submit(__class__.process_url, filename, url, current_date_directory))
                for future in futures:
                    future.result()
                    
                    
                

    @staticmethod
    def is_finished():
        return not __class__.__running_loader.is_alive()

    @staticmethod
    def call_stop():
        __class__.__need_to_stop.set()