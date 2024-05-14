import copy
from datetime import datetime

import requests
from ..base_parser import BaseParser
from utils.utils import *
import bs4


class RiaParser(BaseParser):
    
    __url = "https://ria.ru/services/20240513/more.html?date=20240513T150600"
    __url_template = "https://ria.ru/services/%Y%m%d/more.html?date=%Y%m%dT%H%M%S"



    @staticmethod
    def load_articles_urls(begin_date: datetime, end_date: datetime) -> dict[datetime, list[str]]:
        result_urls: dict[datetime, list[str]] = {}
        for current_date in daterange(begin_date, end_date + timedelta(1)):
            result_urls[current_date] = []
            current_time_lower_threshold = current_date.replace(hour=00, minute=00, second=00)
            current_date_time = current_date.replace(hour=23, minute=59, second=59)
            while current_date_time >= current_time_lower_threshold:
                current_urls, last_time = __class__.__get_urls(current_date_time)
                last_time: datetime
                result_urls[current_date].extend(current_urls)
                current_date_time = current_date_time.replace(hour=last_time.hour, minute=last_time.minute, second=0)
                if len(current_urls) < 20:
                    break
        return result_urls



    def __get_url(date_time: datetime):
        return date_time.strftime(__class__.__url_template)
    
    
    def __get_urls(date_time: datetime) -> tuple[list[str], datetime]:
        """
        Raises:
            - HttpError if something goes wrong
        """
        urls = []
        url = __class__.__get_url(date_time)
        response = requests.get(url)
        if not response.ok:
            return None
        parser = bs4.BeautifulSoup(response.content.decode(), "html.parser")
        list_items: list[bs4.element.Tag] = parser.find_all("div", {'class': 'list-item'}, recursive=True)
        last_time = None
        for item in list_items:
            time_tag = item.find("div", {'class': "list-item__date"})
            content_tag = item.find("div", {'class': "list-item__content"})
            urls.append(content_tag.find_next("a").attrs.get('href', None))
            last_time = datetime.strptime(time_tag.text.split(',')[-1].strip(), "%H:%M")
        return urls, last_time
