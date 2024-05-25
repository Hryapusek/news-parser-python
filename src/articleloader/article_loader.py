import copy
import os
import time
import random

from datetime import datetime, timedelta
from threading import Thread, Event
from concurrent.futures import Future, ProcessPoolExecutor, TimeoutError as FTimeoutError
from textprocess.text_processing import normalize

from urlparser.parse_tools import URLLoader
from urlparser.websiteparsers.article import Article
from utils.utils import daterange

from .exceptions import *

from urlparser.websiteparsers import * 

def _normalize_article(article: Article):
    return normalize(article.text)

def _process_url(filename, url, current_date_directory):
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
    if not text or text.startswith("**Соблюдение авторских"):
        return
    with open(os.path.join(current_date_directory, filename), "w", encoding="utf-16") as file:
        file.write(text)

class ArticleLoader:

    ARTICLES_FOLDER = os.path.join(os.path.curdir, "articles")
    ARTICLE_FILENAME_TEMPLATE = "article_%s.txt"
    ARTICLE_DATE_DIRECTORY_TEMPLATE = "%Y_%m_%d"

    __running_loader: Thread = None

    __need_to_stop = Event()

    __website_parsers: list[BaseParser] = [CommersantParser, MkParser, RiaParser]

    __date_articles: dict[datetime, list[Article]] = {}

    __begin_date = None
    __end_date = None

    __status = ""
    __percentage = 0

    @staticmethod
    def load_articles_from_saved_files(begin_date: datetime, end_date: datetime):
        __class__.__check_if_thread_already_alive()
        __class__.__need_to_stop.clear()
        __class__.__running_loader = Thread(target=ArticleLoader.__load_articles_from_saved_files, args=(begin_date, end_date), daemon=True)
        __class__.__running_loader.start()

    @staticmethod
    def load_articles_from_internet(begin_date: datetime, end_date: datetime):
        __class__.__check_if_thread_already_alive()
        __class__.__need_to_stop.clear()
        __class__.__running_loader = Thread(target=ArticleLoader.__load_articles_from_internet, args=(begin_date, end_date), daemon=True)
        __class__.__running_loader.start()

    @staticmethod
    def wait_for_finish():
        if __class__.__running_loader is None or not __class__.__running_loader.is_alive():
            raise NotRunningException()
        __class__.__running_loader.join()

    @staticmethod
    def __check_if_thread_already_alive():
        if __class__.__running_loader is not None and __class__.__running_loader.is_alive():
            raise AlreadyRunningException()

    @staticmethod
    def __normalize_text(MAX_PERCENTAGE: int):
        __class__.__set_status("Normalizing text", None)
        articles_count = 0
        all_articles = []
        with ProcessPoolExecutor(os.cpu_count()) as pool:
            futures: list[Future] = []
            for articles in __class__.__date_articles.values():
                if __class__.__need_to_stop.is_set(): pool.shutdown(False); return
                for article in articles:
                    if __class__.__need_to_stop.is_set(): pool.shutdown(False); return
                    futures.append(pool.submit(_normalize_article, article))
                    all_articles.append(article)
                    articles_count += 1
            for article, future in zip(all_articles, futures):
                while not __class__.__need_to_stop.is_set():
                    try:
                        article.tokens = future.result(1)
                        break
                    except FTimeoutError:
                        continue
                if __class__.__need_to_stop.is_set(): pool.shutdown(False);return
                add_percentage = MAX_PERCENTAGE / articles_count
                __class__.__set_status(None, __class__.__percentage + add_percentage)   

         
    @staticmethod
    def __set_status(new_status: str, percentage: int = None):
        if new_status is not None:
            __class__.__status = new_status
        if percentage is not None:
            __class__.__percentage = percentage

    @staticmethod
    def get_status() -> tuple[str, int]:
        return __class__.__status, __class__.__percentage


    @staticmethod
    def __load_articles_from_saved_files(begin_date: datetime, end_date: datetime):
        __class__.__set_status("Loading saved articles", 0)
        __class__.__read_from_files(begin_date, end_date, 20)
        __class__.__begin_date = begin_date
        __class__.__end_date = end_date
        __class__.__normalize_text(80)
        __class__.__set_status("Finished!", 100)

    @staticmethod
    def __load_articles_from_internet(begin_date: datetime, end_date: datetime):
        date_url: dict[datetime, set] = {}
        __class__.__set_status("Loading URLs from internet", 0)
        MAX_PERCENTAGE = 10
        with ProcessPoolExecutor(os.cpu_count()) as pool:
            futures: list[Future] = []
            for parser in __class__.__website_parsers:
                if __class__.__need_to_stop.is_set(): pool.shutdown(False);return
                futures.append(pool.submit(parser.load_articles_urls, begin_date, end_date))
                if __class__.__need_to_stop.is_set(): pool.shutdown(False);return
            loaded_date_urls_list = []
            for future in futures:
                while not __class__.__need_to_stop.is_set():
                    try:
                        loaded_date_urls_list.append(future.result(1))
                        break
                    except FTimeoutError:
                        continue
                if __class__.__need_to_stop.is_set(): pool.shutdown(False);return
                percentage = len(loaded_date_urls_list) / len(futures) * MAX_PERCENTAGE
                __class__.__set_status(None, percentage)
        __class__.__set_status("URLs loaded, articles loading start soon...", None)
        for loaded_date_urls in loaded_date_urls_list:
            for loaded_date in loaded_date_urls:
                if __class__.__need_to_stop.is_set(): return
                if loaded_date not in date_url:
                    date_url[loaded_date] = set()
                date_url[loaded_date] = date_url[loaded_date].union(loaded_date_urls[loaded_date])
        __class__.__write_to_files(date_url, 30)
        __class__.__read_from_files(begin_date, end_date, 50)
        __class__.__begin_date = begin_date
        __class__.__end_date = end_date
        __class__.__normalize_text(10)
        __class__.__set_status("Finished!", 100)

    @staticmethod
    def __read_from_files(begin_date: datetime, end_date: datetime, MAX_PERCENTAGE: int):
        date_articles = {}
        if __class__.__need_to_stop.is_set(): return
        if (end_date-begin_date).days == 0:
            MAX_DATE_PERCENTAGE = MAX_PERCENTAGE
        else:
            MAX_DATE_PERCENTAGE = MAX_PERCENTAGE/((end_date-begin_date).days)
        for current_date in daterange(begin_date, end_date + timedelta(1)):
            if __class__.__need_to_stop.is_set(): return
            __class__.__set_status(f"Reading articles for date {current_date}", None)
            current_date_directory = os.path.join(__class__.ARTICLES_FOLDER, current_date.strftime(__class__.ARTICLE_DATE_DIRECTORY_TEMPLATE))
            if not os.path.isdir(current_date_directory):
                # TODO: log later
                continue
            date_articles[current_date] = []
            for file in os.listdir(current_date_directory):
                if __class__.__need_to_stop.is_set(): return
                if not os.path.isfile(os.path.join(current_date_directory, file)):
                    continue
                with open(os.path.join(current_date_directory, file), encoding="utf-16") as article_file:
                    article = Article()
                    article.date = current_date
                    article.text = article_file.read().strip()
                    date_articles[current_date].append(article)
            __class__.__set_status(None, __class__.__percentage + MAX_DATE_PERCENTAGE)
        __class__.__date_articles = date_articles
        

    @staticmethod
    def __write_to_files(date_url: dict[datetime, set], MAX_PERCENTAGE: int):
        if not os.path.isdir(__class__.ARTICLES_FOLDER):
            os.mkdir(__class__.ARTICLES_FOLDER)
        if __class__.__need_to_stop.is_set(): return
        MAX_DATE_PERCENTAGE = MAX_PERCENTAGE/len(date_url)
        for date in date_url:
            __class__.__set_status(f"Loading urls for date {date}", None)
            if __class__.__need_to_stop.is_set(): return
            current_date_directory = os.path.join(__class__.ARTICLES_FOLDER, date.strftime(__class__.ARTICLE_DATE_DIRECTORY_TEMPLATE))
            counter = 0
            if not os.path.isdir(current_date_directory):
                os.mkdir(current_date_directory)
            
            with ProcessPoolExecutor(os.cpu_count()) as pool:
                futures: list[Future] = []
                if len(date_url[date]) > 50: # take random 50
                    urls = copy.deepcopy(date_url[date])
                    result_urls = []
                    for _ in range(50):
                        result_urls.append(random.choice(list(urls)))
                        urls.remove(result_urls[-1])
                else:
                    result_urls = date_url[date]
                for url in result_urls:
                    if __class__.__need_to_stop.is_set(): pool.shutdown(False); return
                    filename = __class__.ARTICLE_FILENAME_TEMPLATE % (counter)
                    while os.path.isfile(os.path.join(current_date_directory, filename)):
                        counter += 1
                        filename = __class__.ARTICLE_FILENAME_TEMPLATE % (counter)
                    counter += 1
                    futures.append(pool.submit(_process_url, filename, url, current_date_directory))
                for future in futures:
                    if __class__.__need_to_stop.is_set(): pool.shutdown(False); return
                    else:
                        future.result()
                        __class__.__set_status(None, __class__.__percentage + MAX_DATE_PERCENTAGE/len(futures))

    def get_dates() -> tuple[datetime, datetime]:
        return __class__.__begin_date, __class__.__end_date

    @staticmethod
    def is_finished():
        if __class__.__running_loader is None:
            raise NotRunningException()
        return not __class__.__running_loader.is_alive()

    @staticmethod
    def call_stop():
        if __class__.__need_to_stop.is_set():
            raise NotRunningException()
        __class__.__need_to_stop.set()

    @staticmethod
    def get_date_articles():
        return __class__.__date_articles

    @staticmethod
    def is_stop_called():
        return __class__.__need_to_stop.is_set()
