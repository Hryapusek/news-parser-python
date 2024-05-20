import re

from textprocess.text_processing import normalize

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
    def parse_file(file_path) -> list[Category]:
        categories: list[Category] = []

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

            lines = text.strip().split('\n')

            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                if line.startswith('#['):
                    categories.append(Category())
                    categories[-1].name = line[2:-1]
                elif line.startswith('##['):
                    categories[-1].subcategories.append(SubCategory())
                    categories[-1].subcategories[-1].name = line[3:-1]
                else:
                    try:
                        categories[-1].subcategories[-1].keywords.extend(normalize(line))
                    except IndexError:
                        print(f"Text after cathegory is not allowed! Check category {categories[-1].name}")
                        raise
        
        return categories
