from src.classifiers.classifier import Classifier
from src.transformer.transformer import Transformer
from numpy.linalg import norm


class KNN(Classifier):
    def __init__(self, transformer: Transformer, k: int = 9):
        super(KNN, self).__init__(transformer)
        self.k = k
        self.data = self.transformer.get_train_data()

    def _get_class_type(self, calcs):
        vote1, vote2 = 0, 0
        for distance, class_type in calcs:
            vote1 += 1 if class_type == 1 else 0
            vote2 += 1 if class_type == -1 else 0
        return 1 if vote1 > vote2 else -1

    def _predict_title(self, vector):
        calcs = []
        for doc in self.data:
            c = norm(vector - doc.title_vector)
            calc = (c, doc.class_type)
            calcs.append(calc)
        calcs.sort()
        return self._get_class_type(calcs[:self.k])

    def _predict_desc(self, vector):
        calcs = []
        for doc in self.data:
            c = norm(vector-doc.des_vector)
            calc = (c, doc.class_type)
            calcs.append(calc)
        calcs.sort()
        return self._get_class_type(calcs[:self.k])

    def predict_vector(self, vector):
        return self._predict_title(vector), self._predict_desc(vector)
