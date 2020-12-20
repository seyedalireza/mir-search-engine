from .classifier import Classifier
from ..transformer.transformer import Transformer


class KNN(Classifier):
    def __init__(self, transformer: Transformer, k: int = 1):
        super(KNN, self).__init__(transformer)
        self.k = k

    def _calc(self, a, b):
        if len(a) != len(b):
            raise Exception('not equal dimensions')
        sum = 0
        for i in range(len(a)):
            sum += (a[i]-b[i])**2
        return sum

    def _get_class_type(self, calc_dict):
        lst = list(sorted(calc_dict.values(), key=lambda item: item[0]))[:self.k]
        vote1, vote2 = 0, 0
        for distance, class_type in lst:
            vote1 += 1 if class_type == 1 else 0
            vote2 += 1 if class_type == -1 else 0
        return 1 if vote1 > vote2 else -1

    def _predict_title(self, vector):
        train_data = self.transformer.get_train_data()
        calc_dict = {}
        for doc in train_data:
            calc_dict[doc.id] = (self._calc(vector, doc.title_vector), doc.class_type)
        return self._get_class_type(calc_dict)

    def _predict_desc(self, vector):
        train_data = self.transformer.get_train_data()
        calc_dict = {}
        for doc in train_data:
            calc_dict[doc.id] = (self._calc(vector, doc.des_vector), doc.class_type)
        return self._get_class_type(calc_dict)

    def predict_vector(self, vector):
        return self._predict_title(vector), self._predict_desc(vector)
