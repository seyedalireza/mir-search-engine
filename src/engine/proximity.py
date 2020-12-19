from classifiers.classification_generator import ClassificationGenerator
from src.index.Indexer import Indexer
import numpy as np
import math
from src.normalizer.normalizer import EnglishNormalizer, PersianNormalizer
from src.engine.engine import normalize_vector


class ProximitySearchEngine(object):
    def __init__(self, indexer: Indexer, classifier: ClassificationGenerator = None):
        self.dist = None
        self.indexer = indexer
        self.en_normalizer = EnglishNormalizer(0.10)
        self.fa_normalizer = PersianNormalizer(0.1)
        self.query = []
        self.common_docs = []
        self.all_docs = {}
        self.classifier = classifier

    def _get_common_docs(self):
        query = self.query
        query_num = len(query)
        lst = []
        all_docs = {}
        for word in query:
            _, docs = self.indexer.get_idf_tf(word)
            ids = [doc.doc_id for doc in docs]
            lst.extend(ids)
        unique_list = list(set(lst))
        common_docs = []
        for i in unique_list:
            if lst.count(i) == query_num:
                common_docs.append(i)
        self.common_docs = common_docs
        for word in query:
            _, docs = self.indexer.get_idf_tf(word)
            docs = filter(lambda doc: doc.doc_id in common_docs, docs)
            all_docs[word] = {doc.doc_id: doc for doc in docs}
        self.all_docs = all_docs

    def _find_in_dist(self, pi1, pi2):
        i, j = 0, 0
        dist = self.dist
        while i < len(pi1) and j < len(pi2):
            n1, n2 = int(pi1[i]), int(pi2[j])
            if abs(n1 - n2) <= dist:
                return True
            if n1 < n2:
                i += 1
            else:
                j += 1
        return False

    def _check_two_word(self, d1, d2):
        result = []
        for i in self.common_docs:
            if self._find_in_dist(d1[i].p_index['desc'], d2[i].p_index['desc']) or \
                    self._find_in_dist(d1[i].p_index['title'], d2[i].p_index['title']):
                result.append(i)
        return result

    def _get_proper_docs(self):
        docs = self.all_docs
        ans = self.common_docs
        for i in range(1, len(self.query)):
            w1, w2 = self.query[i - 1], self.query[i]
            new_doc = self._check_two_word(docs[w1], docs[w2])
            ans = list(filter(lambda doc_id: doc_id in new_doc, ans))
        return ans

    def _get_result_docs(self):
        self._get_common_docs()
        return self._get_proper_docs()

    def _get_query_score(self, query):
        score_lst = []
        for word in self.query:
            score_lst.append((math.log(query.count(word)) + 1) * math.log(len(query) / query.count(word)))
        return normalize_vector(score_lst)

    def _get_doc_score(self, doc):
        score_lst = []
        all_docs = self.all_docs
        for word in self.query:
            d = all_docs[word][doc]
            x = d.tf[0]
            score_lst.append(math.log(x) + 1)
        return normalize_vector(score_lst)

    def _rank_results(self, docs, query):
        query_score = self._get_query_score(query)
        score_board = {}
        for doc in docs:
            doc_score = self._get_doc_score(doc)
            score_board[doc] = np.dot(query_score, doc_score)
        result = [k for k, v in sorted(score_board.items(), key=lambda item: item[1])]
        return result

    def search(self, query, dist, is_english=True, in_most_views: bool = False):
        self.dist = dist
        if is_english:
            query, _ = self.en_normalizer.parse_document(query)
        else:
            query, _ = self.fa_normalizer.parse_document(query)
        query = list(map(lambda z: z[0], query))
        terms = list(set(query))
        self.query = [word for word in terms]
        docs = self._get_result_docs()
        doc_ids = self._rank_results(docs, query)
        if in_most_views:
            doc_ids = [key for key in doc_ids
                       if self.classifier.get_description_class(key) == 1 or self.classifier.get_title_class(key) == 1]
        return doc_ids[:10]
