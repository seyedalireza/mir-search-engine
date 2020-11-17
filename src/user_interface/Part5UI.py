from src.engine.engine import TfIdfSearchEngine
from src.engine.proximity import ProximitySearchEngine
from src.index.Indexer import Indexer
from .UI import UI


def get_query_params(input_str):
    print("Write 1 for english or 2 for persian:")
    english = int(input()) == 1
    print("Write 1 for title or 2 for description or 3 for both:")
    location = int(input())
    in_title = True
    in_description = True
    if location == 1:
        in_description = False
    if location == 2:
        in_title = False
    print("write your query: ")
    query = input()
    if input_str == 2:
        print("Enter your distance: ")
        dist = int(input())
    else:
        dist = None
    return english, in_description, in_title, query, dist


class Part5UI(UI):

    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                english, in_description, in_title, query, _ = get_query_params(input_str)
                engine = TfIdfSearchEngine(self.persian_indexer)
                if english:
                    engine = TfIdfSearchEngine(self.english_indexer)
                result = engine.search(query, english=english, in_title=in_title, in_description=in_description)
                print("your top 10 result is:")
                print(",".join(list(map(str, result[:10]))))
            elif input_str == 2:
                english, in_description, in_title, query, dist = get_query_params(input_str)
                if english:
                    engine = ProximitySearchEngine(self.english_indexer)
                else:
                    engine = ProximitySearchEngine(self.persian_indexer)
                engine.search(query, dist, english)
            elif input_str == 3:
                return

    def print_help(self):
        print("Part 5:")
        print("1- Show Result of an Input Query Using tf-idf")
        print("2- Show Result of an Input Query Using Proximity Search")
        print("3- Exit")