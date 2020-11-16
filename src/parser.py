import csv

from index.NormalizedWord import NormalizedWord
from normalizer.normalizer import EnglishNormalizer, PersianNormalizer


class EnglishCollectionParser:

    doc_url = "../data/ted_talks.csv"

    def __init__(self):
        self.english_normalizer = EnglishNormalizer(0.1)

    def get_all_words(self):
        with open(EnglishCollectionParser.doc_url) as file:
            csv_reader = csv.reader(file)

            line = 0
            columns = []
            words = []
            for row in csv_reader:
                if line == 0:
                    for c in range(len(row)):
                        if row[c] == "description":
                            columns.append(("description", c))
                        elif row[c] == "title":
                            columns.append(("title", c))
                else:
                    for column in columns:
                        index = column[1]
                        txt = row[index]
                        normalized_words, _ = self.english_normalizer.parse_document(txt)
                        words += [NormalizedWord(word[0], row[0], column[0], word[1]) for word in normalized_words]
                line += 1
            return words


class PersianCollectionParser:
    doc_url = "../data/Persian.xml"

    def __init__(self):
        self.normalizer = PersianNormalizer(0.1)

