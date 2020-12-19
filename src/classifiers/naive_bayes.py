import math

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.classifiers.classifier import Classifier
from src.transformer.transformer import Transformer


class NB(Classifier):
    def __init__(self, transformer: Transformer):
        super(NB, self).__init__(transformer)
        self.des_c1 = pd.DataFrame(columns=self.transformer.index_table, data=[])
        self.des_c2 = pd.DataFrame(columns=self.transformer.index_table, data=[])
        self.title_c1 = pd.DataFrame(columns=self.transformer.index_table, data=[])
        self.title_c2 = pd.DataFrame(columns=self.transformer.index_table, data=[])

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
        return output[0], output[1]

    def test(self):
        t_data = self.transformer.get_test_data()
        con_matrix_des = [[0, 0], [0, 0]]
        con_matrix_title = [[0, 0], [0, 0]]
        for i in range(len(t_data)):
            predict = self.predict_vector(t_data[i].des_vector)
            if predict == 1:
                if t_data[i].class_type == 1:
                    con_matrix_des[0][0] += 1
                else:
                    con_matrix_des[1][0] += 1
            if predict == -1:
                if t_data[i].class_type == 1:
                    con_matrix_des[0][1] += 1
                else:
                    con_matrix_des[1][1] += 1
            predict = self.predict_vector(t_data[i].title_vector)
            if predict == 1:
                if t_data[i].class_type == 1:
                    con_matrix_title[0][0] += 1
                else:
                    con_matrix_title[1][0] += 1
            if predict == -1:
                if t_data[i].class_type == 1:
                    con_matrix_title[0][1] += 1
                else:
                    con_matrix_title[1][1] += 1
        return con_matrix_title, con_matrix_des

    def train(self):
        df = pd.DataFrame(columns=self.transformer.index_table, data=[])
        t_data = self.transformer.get_train_data()
        ddf = pd.DataFrame(columns=self.transformer.index_table, data=[])
        cdf = []
        for i in range(len(t_data)):
            df.loc[i] = t_data[i].title_vector
            ddf.loc[i] = t_data[i].des_vector
            cdf.append(t_data[i].class_type)
        des = pd.DataFrame(columns=self.transformer.index_table, data=[])
        title = pd.DataFrame(columns=self.transformer.index_table, data=[])
        for i in range(len(t_data)):
            if cdf[i] == 1:
                self.des_c1 += df.loc[i]
                self.title_c1 += ddf.loc[i]
            else:
                self.des_c2 += df.loc[i]
                self.title_c2 += ddf.loc[i]
            des += df.loc[i]
            title += df.loc[i]
        self.des_c1 += 1
        self.des_c2 += 1
        self.title_c1 += 1
        self.title_c2 += 1
        des += len(self.transformer.index_table)
        title += len(self.transformer.index_table)
        self.des_c1 = self.des_c1 / des
        self.des_c2 = self.des_c2 / des
        self.title_c1 = self.title_c1 / title
        self.title_c2 = self.title_c2 / title



