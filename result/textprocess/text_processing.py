import nltk
import string
nltk.download("stopwords")

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

mystem = Mystem() 
russian_stopwords = stopwords.words("russian")

class TextProcessor:
    @staticmethod
    def normalize(text: str) -> list[str]:
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                and not string.ascii_letters in token
                and token != " " 
                and token.strip() not in punctuation]
        return tokens

