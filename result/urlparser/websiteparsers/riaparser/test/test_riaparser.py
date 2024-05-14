import unittest
from datetime import datetime
from ..ria_parser import RiaParser


class TestRiaParser(unittest.TestCase):

    def test_defaut(self):
        result = RiaParser.load_articles_urls(datetime(2024, 5, 13), datetime(2024, 5, 13))
        print(result)
