import os
import subprocess

def suppress_console_run(*args, **kwargs):
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs['startupinfo'] = startupinfo
    
    return subprocess.run(*args, **kwargs)

subprocess.run = suppress_console_run

import string

russian_stopwords = open("./res/corpora/stopwords/russian").read().split()

from pymystem3 import Mystem
from string import punctuation


def normalize(text: str) -> list[str]:
    mystem = Mystem() 
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords
            and not string.ascii_letters in token
            and token != " "
            and token.strip() not in punctuation]
    return tokens

