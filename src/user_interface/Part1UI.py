from src.normalizer.normalizer import EnglishNormalizer, PersianNormalizer
from .UI import UI


class Part1UI(UI):

    def __init__(self):
        self.en_normalizer = EnglishNormalizer(0.05)
        self.fa_normalizer = PersianNormalizer(0.05)

    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                english, query = get_query_params()
                normalizer = self.fa_normalizer
                if english:
                    normalizer = self.en_normalizer
                words, stop_words = normalizer.parse_document(query)
                print("Normalized text:")
                print(",".join([word[0] for word in words]))
                print("Stop words:")
                print(",".join(stop_words))
            elif input_str == 2:
                return

    def print_help(self):
        print("Part 1:")
        print("1- Show the Normalized Form of a Query and stop words:")
        print("2- Exit")

def get_query_params():
    print("Write 1 for english or 2 for persian:")
    english = int(input()) == 1
    print("Write your query: ")
    query = input()
    return english, query
