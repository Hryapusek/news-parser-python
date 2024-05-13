import requests
import html2text
import re

def extract_consecutive_russian_lines(text: str, threshold=3, russian_threshold=0.5):
    # Split the text into lines
    lines = text.split('\n')
    
    consecutive_count = 0
    consecutive_russian_lines = []
    reached_threshold = False
    
    for line in lines:
        # Calculate the percentage of Russian letters in the line
        total_letters = len(line)
        russian_letters = len(re.findall(r'[а-яА-ЯёЁ]', line))
        russian_percentage = russian_letters / total_letters if total_letters > 0 else 0
        
        # Check if the percentage of Russian letters exceeds the threshold
        if russian_percentage >= russian_threshold:
            consecutive_count += 1
            consecutive_russian_lines.append(line.strip())
            if consecutive_count >= threshold:
                reached_threshold = True
        elif reached_threshold:
            return consecutive_russian_lines
        else:
            consecutive_count = 0
            consecutive_russian_lines = []
    
    if reached_threshold:
        return consecutive_russian_lines

    return None

url = "https://ria.ru/20240513/volchansk-1945511904.html"

parser = html2text.HTML2Text()
parser.ignore_links = True

response = requests.get(url)
print(extract_consecutive_russian_lines(parser.handle(response.content.decode()), 4, 0.7))
