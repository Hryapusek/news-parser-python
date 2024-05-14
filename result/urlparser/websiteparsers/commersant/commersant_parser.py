import copy
from datetime import datetime

import requests
from ..base_parser import BaseParser
from utils.utils import *
import bs4


class CommersantParser(BaseParser):

    prefix = "commersant"

    __url = "https://www.kommersant.ru/listpage/lazyloaddocs?regionid=0&listtypeid=4&listid=86&date=14.05.2024&intervaltype=1&idafter=6691521"
    __url_template = "https://www.kommersant.ru/listpage/lazyloaddocs"
    __url__params = {
        "regionid": 0,
        "listtypeid": 4,
        "listid": 86,
        "date": "%d.%m.%Y",
        "intervaltype": 1,
        "idafter": None,
    }

    @staticmethod
    def load_articles_urls(
        begin_date: datetime, end_date: datetime
    ) -> dict[datetime, list[str]]:
        result_urls: dict[datetime, list[str]] = {}
        for current_date in daterange(begin_date, end_date + timedelta(1)):
            result_urls[current_date] = __class__.__get_urls(current_date)
        return result_urls

    def __get_urls(date_time: datetime) -> list[str]:
        """
        Raises:
            - HttpError if something goes wrong
        """
        urls = []
        finish = False
        last_doc_id = None
        while not finish:
            params = copy.deepcopy(__class__.__url__params)
            params["date"] = date_time.strftime(params["date"])
            if last_doc_id:
                params["idafter"] = last_doc_id
            response = requests.get(__class__.__url_template, params)
            if not response.ok:
                response = requests.get(__class__.__url_template, params)
                if not response.ok:
                    break
            response_json = response.json()
            finish = not response_json["HasNextPage"]
            for item in response_json["Items"]:
                last_doc_id = item["DocsID"]
                urls.append("https://www.kommersant.ru/doc/" + str(item["DocsID"]))

        return urls
