import csv
import xml.etree.cElementTree as ET
from src.index.NormalizedWord import NormalizedWord
from src.normalizer.normalizer import EnglishNormalizer, PersianNormalizer


class EnglishCollectionParser:
    doc_url = "data/ted_talks.csv"

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
                        words += [NormalizedWord(word[0], int(row[0]), column[0], word[1]) for word in normalized_words]
                line += 1
            return words


class PersianCollectionParser:
    doc_url = "../data/Persian.xml"

    def __init__(self):
        self.normalizer = PersianNormalizer(0.1)

    def get_all_words(self):
        tree = ET.parse(PersianCollectionParser.doc_url)
        words = []
        for page in tree.getroot():
            doc_id = -1
            title = ""
            comment = ""
            text = ""
            for tag in page:
                if "title" in tag.tag:
                    title = tag.text
                elif "id" in tag.tag:
                    doc_id = int(tag.text)
                elif "revision" in tag.tag:
                    for rev in tag:
                        if "comment" in rev.tag:
                            comment = rev.text
                        elif "text" in rev.tag:
                            text = rev.text
            document = {
                "title": title,
                "comment": comment,
                "text": text
            }
            for column in document:
                normalized_words, _ = self.normalizer.parse_document(document[column])
                words += [NormalizedWord(word[0], doc_id, column, word[1])
                          for word in normalized_words]
        return words
