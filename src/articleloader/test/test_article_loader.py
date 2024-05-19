import time
import unittest

from articleloader.article_loader import ArticleLoader
from datetime import datetime


class TestArticleLoader(unittest.TestCase):

    def test_default(self):
        ArticleLoader.load_articles_from_internet(datetime(2024, 5, 13), datetime(2024, 5, 13))
        ArticleLoader.wait_for_finish()
