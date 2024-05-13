import requests
import html2text
import re
from .exceptions import *


class URLLoader:

    @staticmethod
    def load_text_from_url(url: str) -> str | None:
        """
        Returns:
            Text if there is some, None otherwise

        Raises:
            - ErrorResponseCodeException: if could not load given url
        """
        response = requests.get(url)
        if not response.ok:
            raise ErrorResponseCodeException(response.status_code, response.content.decode())
        
        parser = html2text.HTML2Text()
        parser.ignore_links = True

        response = requests.get(url)
        result = __class__.__extract_consecutive_russian_lines(parser.handle(response.content.decode()), 4, 0.7)
        if not result:
            return None
        return " ".join(result)

    @staticmethod
    def __extract_consecutive_russian_lines(text: str, threshold=3, russian_threshold=0.5, max_skipped_lines=5):
        # Split the text into lines
        lines = text.split('\n')
        
        consecutive_count = 0
        consecutive_russian_lines = []
        temp_consecutive_russian_lines = []
        reached_threshold = False
        skipped_after_threashold_reached = 0
        
        for line in lines:
            # Calculate the percentage of Russian letters in the line
            total_letters = len(line)
            russian_letters = len(re.findall(r'[а-яА-ЯёЁ]', line))
            russian_percentage = russian_letters / total_letters if total_letters > 0 else 0
            
            # Check if the percentage of Russian letters exceeds the threshold
            if russian_percentage >= russian_threshold:
                skipped_after_threashold_reached = 0
                consecutive_count += 1
                temp_consecutive_russian_lines.append(line.strip())
                if consecutive_count >= threshold:
                    consecutive_russian_lines.extend(temp_consecutive_russian_lines)
                    temp_consecutive_russian_lines = []
                    reached_threshold = True
            elif reached_threshold:
                temp_consecutive_russian_lines = []
                consecutive_count = 0
                skipped_after_threashold_reached += 1
                if skipped_after_threashold_reached >= max_skipped_lines:
                    return consecutive_russian_lines
            else:
                consecutive_count = 0
                temp_consecutive_russian_lines = []
        
        if reached_threshold:
            return consecutive_russian_lines

        return None
