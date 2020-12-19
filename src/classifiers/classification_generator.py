import csv
import pandas as pd


class ClassificationGenerator:

    OUTPUT_FILE_PATH = "../data/classification_results.csv"
    DOC_FILE_PATH = "../data/ted_talks.csv"

    def __init__(self, transformer, classifier):
        self.transformer = transformer
        self.classifier = classifier
        self.df = pd.DataFrame()

    def load(self):
        self.df = pd.read_csv(self.OUTPUT_FILE_PATH)

    def get_title_class(self, doc_id):
        return self.df.loc[doc_id - 1, "t_class"]

    def get_description_class(self, doc_id):
        return self.df.loc[doc_id - 1, "d_class"]

    def train_and_write(self):
        title_doc_class_map = dict()
        description_class_map = dict()
        with open(self.DOC_FILE_PATH, encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            line = 0
            columns = dict()
            for row in csv_reader:
                if line == 0:
                    for c in range(len(row)):
                        if row[c] == "description":
                            columns["desc"] = c
                        elif row[c] == "title":
                            columns["title"] = c
                else:
                    txt = row[columns["title"]]
                    t_class, _ = self.classifier.predict(txt)
                    txt = row[columns["desc"]]
                    _, d_class = self.classifier.predict(txt)
                    title_doc_class_map[line] = t_class
                    description_class_map[line] = d_class
                line += 1
            self.df = pd.DataFrame(columns=["t_class", "d_class"])
            for i in range(1, line, 1):
                self.df.loc[i] = [title_doc_class_map[i], title_doc_class_map[i]]
            self.df.to_csv(self.OUTPUT_FILE_PATH)
