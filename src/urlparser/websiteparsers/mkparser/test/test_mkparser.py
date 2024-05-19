import unittest
from datetime import datetime
from ..mk_parser import MkParser


class TestMkParser(unittest.TestCase):

    def test_defaut(self):
        result = MkParser.load_articles_urls(datetime(2024, 5, 13), datetime(2024, 5, 13))
        print(result)
