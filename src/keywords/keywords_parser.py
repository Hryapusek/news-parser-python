from textprocess.text_processing import normalize
from concurrent.futures import ProcessPoolExecutor, as_completed

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

            current_category = None
            current_subcategory = None
            tasks = []
            keywords_mapping = {}

            with ProcessPoolExecutor() as executor:
                for line in lines:
                    line = line.strip()
                    if len(line) == 0:
                        continue
                    if line.startswith('#['):
                        current_category = Category()
                        current_category.name = line[2:-1]
                        categories.append(current_category)
                    elif line.startswith('##['):
                        current_subcategory = SubCategory()
                        current_subcategory.name = line[3:-1]
                        if current_category:
                            current_category.subcategories.append(current_subcategory)
                    else:
                        if current_subcategory:
                            # Schedule the normalization task
                            future = executor.submit(normalize, line)
                            tasks.append(future)
                            keywords_mapping[future] = current_subcategory
                        else:
                            print(f"Text after category is not allowed! Check category {current_category.name}")
                            raise IndexError(f"Text after category is not allowed! Check category {current_category.name}")

                # Collect the results of normalization
                for task in as_completed(tasks):
                    keywords = task.result()
                    subcategory = keywords_mapping[task]
                    subcategory.keywords.extend(keywords)

        return categories
