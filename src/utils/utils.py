from datetime import timedelta
import sys
import os

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def mute():
    sys.stdout = open(os.devnull, 'w')   