import asyncio
import time
import unittest

from articleloader.article_loader import ArticleLoader
from datetime import datetime


class TestArticleLoader(unittest.TestCase):

    def test_default(self):
        ArticleLoader.load_articles_from_internet(datetime(2024, 5, 13), datetime(2024, 5, 13))
        asyncio.run(asyncio.sleep(0.1))
        while not ArticleLoader.is_finished():
            print(*ArticleLoader.get_status())
            asyncio.run(asyncio.sleep(0.1))
        print(*ArticleLoader.get_status())

    def test_stop(self):
        ArticleLoader.load_articles_from_internet(datetime(2024, 5, 13), datetime(2024, 5, 13))
        asyncio.run(asyncio.sleep(20))
        ArticleLoader.call_stop()
        ArticleLoader.wait_for_finish()