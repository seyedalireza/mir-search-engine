import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.classifiers.classifier import Classifier


class RF(Classifier):

    def predict_vector(self, vector):
        return self.title_model.predict([vector])[0], self.des_model.predict([vector])[0]

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