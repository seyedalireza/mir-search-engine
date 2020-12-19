import math
from typing import List
import csv
from normalizer.normalizer import EnglishNormalizer
import numpy as np


class Transformer:
    train_set_path = "../data/train.csv"
    test_set_path = "../data/test.csv"

    """
    index_table = list of words in sorted order.
    words_index_dict = dictionary of words to it's index.
    """
    def __init__(self):
        # TODO save data, hash-table
        self.words_index_dict = dict()
        self.english_normalizer = EnglishNormalizer(0.1)
        train_docs, all_words = self._get_documents_and_words(Transformer.train_set_path)
        self.all_words = all_words
        self.index_table = list(set(all_words))
        self.index_table.sort()
        for i in range(len(self.index_table)):
            self.words_index_dict[self.index_table[i]] = i
        test, _ = self._get_documents_and_words(Transformer.test_set_path)
        self.train_data, self.idf = self._create_docs(train_docs)
        self.test_data, _ = self._create_docs(test)

    def _create_docs(self, data):
        docs = []
        idfs = []
        for j in range(len(self.index_table)):
            idfs.append(math.log(len(self.all_words) / self.all_words.count(self.index_table[j])))
        for i in range(len(data)):
            title_vector = [0 for _ in range(len(self.index_table))]
            des_vector = [0 for _ in range(len(self.index_table))]
            for j in range(len(self.index_table)):
                idf = idfs[j]
                title_vector[j] = data[i][0].count(self.index_table[j]) * idf
                des_vector[j] = data[i][1].count(self.index_table[j]) * idf
            docs.append(Doc(i, title_vector, des_vector, data[i][2]))
        return docs, idfs

    def _get_documents_and_words(self, path):
        documents = []  # map of doc_id to [list of title words, list of description words, class]
        all_words = []
        with open(path, encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            line = 0
            columns = {}
            for row in csv_reader:
                if line == 0:
                    for c in range(len(row)):
                        if row[c] == "description":
                            columns["desc"] = c
                        elif row[c] == "title":
                            columns["title"] = c
                        elif row[c] == "views":
                            columns["views"] = c
                else:
                    index = columns["title"]
                    txt = row[index]
                    normalized_words, _ = self.english_normalizer.parse_document(txt)
                    normalized_words = [word for word in normalized_words if word[0].isalpha()]
                    title_words = [word[0] for word in normalized_words]
                    index = columns["desc"]
                    txt = row[index]
                    normalized_words, _ = self.english_normalizer.parse_document(txt)
                    normalized_words = [word for word in normalized_words if word[0].isalpha()]
                    des_words = [word[0] for word in normalized_words]
                    index = columns["views"]
                    class_type = int(row[index])
                    all_words += des_words
                    all_words += title_words
                    documents.append(([title_words, des_words, class_type]))
                line += 1
        return documents, all_words

    def get_train_data(self):
        return self.train_data

    def get_test_data(self):
        return self.test_data

    def get_index_dict(self):
        return self.index_table

    def transform(self, text):
        normalized_words, _ = self.english_normalizer.parse_document(text)
        normalized_words = [word for word in normalized_words if word[0].isalpha()]
        words = [word[0] for word in normalized_words]
        v = []
        for i in range(len(self.index_table)):
            v.append(words.count(self.index_table[i]) * self.idf[i])
        return v


class Doc:

    def __init__(self, doc_id: int, title_vector: List, des_vector: List, class_type: int):
        self.title_vector = np.array(title_vector)
        self.des_vector = np.array(des_vector)
        self.class_type = class_type
        self.doc_id = doc_id

    def __str__(self):
        return str.format("document {}, title_vector : {} , des_vector: {}, class_type: {}",
                          self.doc_id, self.title_vector, self.des_vector, self.class_type)

    def __repr__(self):
        return self.__str__()