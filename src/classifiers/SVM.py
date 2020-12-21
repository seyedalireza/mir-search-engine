from sklearn.svm import SVC
from ..transformer.transformer import Transformer
from .classifier import Classifier
import numpy as np


class SVM(Classifier):
    def __init__(self, transformer: Transformer, c: float = 1.0):
        super(SVM, self).__init__(transformer)
        self.c = c
        self.classifier1 = None
        self.classifier2 = None

    def predict_vector(self, vector):
        # vector = np.array(vector)
        return (
            self.classifier1.predict([vector])[0],
            self.classifier2.predict([vector])[0],
        )

    def _title_train(self, titles, y):
        svclassifier = SVC(kernel='rbf', C=self.c)
        svclassifier.fit(titles, y)
        self.classifier1 = svclassifier

    def _desc_train(self, descs, y):
        svclassifier = SVC(kernel='rbf', C=self.c)
        svclassifier.fit(descs, y)
        self.classifier2 = svclassifier

    def train(self):
        n = len(self.transformer.index_table)
        train_data = self.transformer.get_train_data()
        title_list, desc_list, y = [], [], []
        for doc in train_data:
            title_list.append(list(doc.title_vector))
            desc_list.append(list(doc.des_vector))
            y.append(doc.class_type)
        title_list, desc_list, y = np.array(title_list), np.array(desc_list), y
        self._title_train(title_list, y)
        self._desc_train(desc_list, y)
