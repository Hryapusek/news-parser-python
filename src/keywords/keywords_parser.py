import functools
import re

from textprocess.text_processing import TextProcessor

class SubCategory:
    def __init__(self) -> None:
        self.name: str = ""
        self.keywords: list[str] = []

class Category:
    def __init__(self) -> None:
        self.name: str = ""
        self.subcategories: list[SubCategory] = []

class KeywordsParser:

    @staticmethod
    def parse_file(file_path):
        categories = []

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

            # Define regular expressions to match sections and subsections
            section_pattern = r'#\[(.*?)\]'
            subsection_pattern = r'##\[(.*?)\]'

            # Find all matches for sections
            sections = re.findall(section_pattern, text, re.DOTALL)
            
            # Iterate over sections
            for section_name in sections:
                section = Category()
                section.name = section_name

                # Find all matches for subsections within this section
                subsections_text = re.split(section_pattern, text)[sections.index(section_name) + 1]
                subsections = re.findall(subsection_pattern, subsections_text, re.DOTALL)

                # Iterate over subsections
                for subsection_name in subsections:
                    subsection = SubCategory()
                    section.subcategories.append(subsection)
                    subsection.name = subsection_name

                    # Find all contents within this subsection
                    subsection_text = re.split(subsection_pattern, subsections_text)[subsections.index(subsection_name) + 1].strip()
                    subsection.keywords = TextProcessor.normalize(subsection_text)

                # Add the section to the list of classes
                categories.append(section)

        return categories
