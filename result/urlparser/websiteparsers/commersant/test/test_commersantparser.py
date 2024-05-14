import unittest
from datetime import datetime
from ..commersant_parser import CommersantParser


class TestCommersantParser(unittest.TestCase):

    def test_defaut(self):
        result = CommersantParser.load_articles_urls(datetime(2024, 5, 13), datetime(2024, 5, 13))
        print(result)
