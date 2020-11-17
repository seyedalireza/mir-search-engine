import csv
import xml.etree.cElementTree as ET
from src.index.NormalizedWord import NormalizedWord
from src.normalizer.normalizer import EnglishNormalizer, PersianNormalizer


class EnglishCollectionParser:

    def __init__(self, doc_url="../data/ted_talks.csv"):
        self.doc_url = doc_url
        self.english_normalizer = EnglishNormalizer(0.1)

    def get_all_words(self):
        with open(self.doc_url, encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            line = 0
            columns = []
            words = []
            for row in csv_reader:
                if line == 0:
                    for c in range(len(row)):
                        if row[c] == "description":
                            columns.append(("desc", c))
                        elif row[c] == "title":
                            columns.append(("title", c))
                else:
                    for column in columns:
                        index = column[1]
                        txt = row[index]
                        normalized_words, _ = self.english_normalizer.parse_document(txt)
                        words += [NormalizedWord(word[0], line, column[0], word[1]) for word in normalized_words]
                line += 1
            return words


class PersianCollectionParser:

    def __init__(self, doc_url="../data/Persian.xml"):
        self.doc_url = doc_url
        self.normalizer = PersianNormalizer(0.1)

    def get_all_words(self):
        tree = ET.parse(self.doc_url)
        words = []
        for page in tree.getroot():
            doc_id = -1
            title = ""
            text = ""
            for tag in page:
                if "title" in tag.tag:
                    title = tag.text
                elif "id" in tag.tag:
                    doc_id = int(tag.text)
                elif "revision" in tag.tag:
                    for rev in tag:
                        if "text" in rev.tag:
                            text = rev.text
            document = {
                "title": title,
                "desc": text
            }
            for column in document:
                normalized_words, _ = self.normalizer.parse_document(document[column])
                words += [NormalizedWord(word[0], doc_id, column, word[1])
                          for word in normalized_words]
        return words
