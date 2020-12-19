import math

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.classifiers.classifier import Classifier
from src.transformer.transformer import Transformer


class NB(Classifier):
    def __init__(self, transformer: Transformer):
        super(NB, self).__init__(transformer)
        self.des_c1 = [0 for _ in range(len(self.transformer.index_table))]
        self.des_c2 = [0 for _ in range(len(self.transformer.index_table))]
        self.title_c1 = [0 for _ in range(len(self.transformer.index_table))]
        self.title_c2 = [0 for _ in range(len(self.transformer.index_table))]

    def predict(self, text):
        normalized_words, _ = self.normalizer.parse_document(text)
        normalized_words = [word for word in normalized_words if word[0].isalpha()]
        words = [word[0] for word in normalized_words]
        v = []
        for i in range(self.transformer.index_table):
            v.append(words.count(self.transformer.index_table[i]))
        return self.predict_vector(v)

    def predict_vector(self, vector):
        res = [0, 0, 0, 0]
        for i in range(len(vector)):
            res[0] += vector[i] * math.log(self.des_c1[i])
            res[1] += vector[i] * math.log(self.des_c2[i])
            res[2] += vector[i] * math.log(self.title_c1[i])
            res[3] += vector[i] * math.log(self.title_c2[i])
        output = [0, 0]
        if res[0] > res[1]:
            output[0] = 1
        else:
            output[0] = -1
        if res[2] > res[3]:
            output[1] = 1
        else:
            output[1] = -1
        return output[1], output[0]

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

    def train(self):
        t_data = self.transformer.get_train_data()
        des = [0 for _ in range(len(self.transformer.index_table))]
        title = [0 for _ in range(len(self.transformer.index_table))]
        for i in range(len(t_data)):
            if t_data[i].class_type == 1:
                for j in range(len(self.des_c1)):
                    self.des_c1[j] += t_data[i].des_vector[j]
                    self.title_c1[j] += t_data[i].title_vector[j]
            else:
                for j in range(len(self.des_c1)):
                    self.des_c2[j] += t_data[i].des_vector[j]
                    self.title_c2[j] += t_data[i].title_vector[j]
            for j in range(len(self.des_c1)):
                des[j] += t_data[i].des_vector[j]
                title[j] += t_data[i].title_vector[j]
        for j in range(len(self.des_c1)):
            des[j] += len(self.transformer.index_table)
            title[j] += len(self.transformer.index_table)
            self.des_c1[j] += 1
            self.des_c1[j] /= des[j]
            self.des_c2[j] += 1
            self.des_c2[j] /= des[j]
            self.title_c1[j] += 1
            self.title_c1[j] /= title[j]
            self.title_c2[j] += 1
            self.title_c2[j] /= title[j]




