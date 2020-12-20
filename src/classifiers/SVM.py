from .classifier import Classifier
from ..transformer.transformer import Transformer
import numpy as np
import cvxopt


class SVM(Classifier):
    def __init__(self, transformer: Transformer, c: int = 1):
        super(SVM, self).__init__(transformer)
        self.c = c
        self.bias = []
        self.weights = []
        self.support_vectors = []
        self.support_labels = []

    def _linear_kernel(self, x, y):
        return np.inner(x, y)

    def _gram_matrix(self, vectors):
        n_samples = len(vectors)
        res = np.zeros((n_samples, n_samples))
        for i, x_i in enumerate(vectors):
            for j, x_j in enumerate(vectors):
                res[i, j] = self._linear_kernel(x_i, x_j)
        return res

    def _compute_multipliers(self, vectors, y):
        n_samples = len(vectors)

        K = self._gram_matrix(vectors)
        P = cvxopt.matrix(np.outer(y, y) * K)
        q = cvxopt.matrix(-1 * np.ones(n_samples))
        G_std = cvxopt.matrix(np.diag(np.ones(n_samples) * -1))
        h_std = cvxopt.matrix(np.zeros(n_samples))
        G_slack = cvxopt.matrix(np.diag(np.ones(n_samples)))
        h_slack = cvxopt.matrix(np.ones(n_samples) * self.c)
        G = cvxopt.matrix(np.vstack((G_std, G_slack)))
        h = cvxopt.matrix(np.vstack((h_std, h_slack)))
        A = cvxopt.matrix(y, (1, n_samples))
        b = cvxopt.matrix(0.0)
        solution = cvxopt.solvers.qp(P, q, G, h, A, b)
        return np.ravel(solution['x'])

    def _set_parameters(self, vectors, labels, lagrange_multipliers):
        support_vector_indices = lagrange_multipliers > 1e-10

        weights = lagrange_multipliers[support_vector_indices]
        support_vectors = vectors[support_vector_indices]
        support_labels = labels[support_vector_indices]
        bias = np.mean(
            [y - self._svm_predict(x, 0.0, weights, support_vectors, support_labels)
             for (y, x) in zip(support_labels, support_vectors)])
        self.bias.append(bias)
        self.weights.append(weights)
        self.support_vectors.append(support_vectors)
        self.support_labels.append(support_labels)

    def _svm_predict(self, vector, bias, weights, support_vectors, support_labels):
        result = bias
        for z_i, x_i, y_i in zip(weights, support_vectors, support_labels):
            result += z_i * y_i * self._linear_kernel(x_i, vector)
        return np.sign(result).item()

    def predict_vector(self, vector):
        return (
            self._svm_predict(vector, self.bias[0], self.weights[0], self.support_vectors[0], self.support_labels[0]),
            self._svm_predict(vector, self.bias[1], self.weights[1], self.support_vectors[1], self.support_labels[1])
        )

    def _title_train(self, titles, y):
        multipliers = self._compute_multipliers(titles, y)
        self._set_parameters(titles, y, multipliers)

    def _desc_train(self, descs, y):
        multipliers = self._compute_multipliers(descs, y)
        self._set_parameters(descs, y, multipliers)

    def train(self):
        train_data = self.transformer.get_train_data()
        title_list, desc_list, y = [], [], []
        for doc in train_data:
            title_list.append(doc.title_vector)
            desc_list.append(doc.des_vector)
            y.append(doc.class_type)
        self._title_train(title_list, y)
        self._desc_train(desc_list, y)
