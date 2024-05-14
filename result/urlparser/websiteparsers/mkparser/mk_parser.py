import copy
from datetime import datetime

import requests
from ..base_parser import BaseParser
from utils.utils import *
import bs4


class MkParser(BaseParser):
    
    __url = "https://www.mk.ru/news/2024/5/12/"
    __url_template = "https://www.mk.ru/news/%s/%s/%s/"


    @staticmethod
    def load_articles_urls(begin_date: datetime, end_date: datetime) -> dict[datetime, list[str]]:
        result_urls: dict[datetime, list[str]] = {}
        for current_date in daterange(begin_date, end_date + timedelta(1)):
            result_urls[current_date] = __class__.__get_urls(current_date)
        return result_urls



    def __get_url(date_time: datetime):
        year_str = date_time.strftime("%Y")
        month_str = date_time.strftime("%m").lstrip('0')
        day_str = date_time.strftime("%d").lstrip('0')
        return __class__.__url_template % (year_str, month_str, day_str)
    
    
    def __get_urls(date_time: datetime) -> list[str]:
        """
        Raises:
            - HttpError if something goes wrong
        """
        urls = []
        url = __class__.__get_url(date_time)
        response = requests.get(url)
        if not response.ok:
            response = requests.get(url)
            if not response.ok:
                return None
        parser = bs4.BeautifulSoup(response.content.decode(), "html.parser")
        list_tag = parser.find("ul", {'class': 'news-listing__day-list'}, recursive=True)
        list_items: list[bs4.element.Tag] = list_tag.find_all("li", {'class': 'news-listing__item'}, recursive=True)
        for item in list_items:
            urls.append(item.find("a", {'class': "news-listing__item-link"}).attrs.get('href', None))
        return urls
