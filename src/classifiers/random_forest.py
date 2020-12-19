from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from normalizer.normalizer import EnglishNormalizer
from transformer.transformer import Transformer

from src.classifiers.classifier import Classifier


class RF(Classifier):

    def predict_vector(self, vector):
        return self.title_model.predict([vector]), self.des_model.predict([vector])

    def train(self):
        parameters = {'bootstrap': True,
                      'min_samples_leaf': 5,
                      'n_estimators': 100,
                      'min_samples_split': 25,
                      'max_features': 'sqrt',
                      'max_depth': 10000,
                      'max_leaf_nodes': None}
        df = pd.DataFrame(columns=self.transformer.index_table, data=[])
        t_data = self.transformer.get_train_data()
        ddf = pd.DataFrame(columns=self.transformer.index_table, data=[])
        cdf = []
        for i in range(len(t_data)):
            df.loc[i] = t_data[i].title_vector
            ddf.loc[i] = t_data[i].des_vector
            cdf.append(t_data[i].class_type)

        rf = RandomForestClassifier(**parameters)
        rf.fit(df, cdf)
        drf = RandomForestClassifier(**parameters)
        drf.fit(ddf, cdf)
        self.title_model = rf
        self.des_model = drf