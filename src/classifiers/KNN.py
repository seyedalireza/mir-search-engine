from src.classifiers.classifier import Classifier
from src.transformer.transformer import Transformer


class KNN(Classifier):
    def __init__(self, transformer: Transformer, k: int = 1):
        super(KNN, self).__init__(transformer)
        self.k = k
        n = len(self.transformer.index_table)
        self.data = self.transformer.get_train_data()[n // 100:2 * n // 100]

    def _calc(self, a, b):
        if len(a) != len(b):
            raise Exception('not equal dimensions')
        sum = 0
        for i in range(len(a)):
            sum += (a[i] - b[i]) ** 2
        return sum

    def _get_class_type(self, calcs):
        vote1, vote2 = 0, 0
        for distance, class_type in calcs:
            vote1 += 1 if class_type == 1 else 0
            vote2 += 1 if class_type == -1 else 0
        return 1 if vote1 > vote2 else -1

    def _predict_title(self, vector):
        calcs = []
        for doc in self.data:
            calc = (self._calc(vector, doc.title_vector), doc.class_type)
            if len(calcs) < self.k:
                calcs.append(calc)
            else:
                if calc[0] > calcs[0][0]:
                    calcs = [calc] + calcs[1:]
            calcs.sort()
        return self._get_class_type(calcs)

    def _predict_desc(self, vector):
        calcs = []
        for doc in self.data:
            calc = (self._calc(vector, doc.des_vector), doc.class_type)
            if len(calcs) < self.k:
                calcs.append(calc)
            else:
                if calc[0] > calcs[0][0]:
                    calcs = [calc] + calcs[1:]
            calcs.sort()
        return self._get_class_type(calcs)

    def predict_vector(self, vector):
        return self._predict_title(vector), self._predict_desc(vector)
