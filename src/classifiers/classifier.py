import pandas as pd
import numpy as np


from normalizer.normalizer import EnglishNormalizer
from transformer.transformer import Transformer


class Classifier:

    def __init__(self, transformer: Transformer):
        self.transformer = transformer
        self.normalizer = EnglishNormalizer(0.1)
        self.des_model = None
        self.title_model = None

    def predict(self, text):
        return self.predict_vector(self.transformer.transform(text))

    def predict_vector(self, vector):
        pass

    def train(self):
        pass

    def test(self):
        t_data = self.transformer.get_test_data()
        con_matrix_des = [[0, 0], [0, 0]]
        con_matrix_title = [[0, 0], [0, 0]]
        for i in range(len(t_data)):
            predict = self.predict_vector(t_data[i].des_vector)
            if predict[1] == 1:
                if t_data[i].class_type == 1:
                    con_matrix_des[0][0] += 1
                else:
                    con_matrix_des[1][0] += 1
            if predict[1] == -1:
                if t_data[i].class_type == 1:
                    con_matrix_des[0][1] += 1
                else:
                    con_matrix_des[1][1] += 1
            predict = self.predict_vector(t_data[i].title_vector)
            if predict[0] == 1:
                if t_data[i].class_type == 1:
                    con_matrix_title[0][0] += 1
                else:
                    con_matrix_title[1][0] += 1
            if predict[0] == -1:
                if t_data[i].class_type == 1:
                    con_matrix_title[0][1] += 1
                else:
                    con_matrix_title[1][1] += 1
        return con_matrix_title, con_matrix_des

