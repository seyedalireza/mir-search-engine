import math
from src.index.Indexer import Indexer
import numpy as np
from src.normalizer.normalizer import EnglishNormalizer, PersianNormalizer
from .utils import normalize_vector
from classifiers.classification_generator import ClassificationGenerator


class TfIdfSearchEngine:

    def __init__(self, indexer: Indexer, classifier: ClassificationGenerator = None):
        self.indexer = indexer
        self.en_normalizer = EnglishNormalizer(0.10)
        self.fa_normalizer = PersianNormalizer(0.1)
        self.classifier = classifier

    def search(self, query, in_title: bool = True, in_description: bool = True, english: bool = True,
               in_most_views: bool = False):
        if english:
            terms, _ = self.en_normalizer.parse_document(query)
        else:
            terms, _ = self.fa_normalizer.parse_document(query)
        terms = [word[0] for word in terms]
        des_doc_vectors, title_doc_vectors, query_vectors = self.get_vectors(terms)
        query_vectors = normalize_vector(query_vectors)
        des_result = {}
        title_result = {}
        total_result = {}
        for v in des_doc_vectors:
            des_doc_vectors[v] = normalize_vector(des_doc_vectors[v])
            des_result[v] = np.dot(des_doc_vectors[v], query_vectors)
        for v in title_doc_vectors:
            title_doc_vectors[v] = normalize_vector(title_doc_vectors[v])
            title_result[v] = np.dot(title_doc_vectors[v], query_vectors)
        for v in title_doc_vectors:
            if in_description and in_title:
                total_result[v] = des_result[v] + title_result[v]
            elif in_description:
                total_result[v] = des_result[v]
            else:
                total_result[v] = title_result[v]
        total_keys = list(total_result.keys())
        total_keys.sort(key=lambda x: total_result[x], reverse=True)
        if in_most_views:
            total_keys = [key for key in total_keys
                          if self.classifier.get_description_class(key) == 1 or self.classifier.get_title_class(key) == 1]
        return total_keys

    def get_vectors(self, terms):
        query_vector = {}
        # construct table for documents
        uniqe_terms = list(set(terms))
        uniqe_terms.sort()
        title_words_table = {}
        description_words_table = {}
        idf_table = {}
        all_doc_ids = set()
        for word in uniqe_terms:
            idf, docs = self.indexer.get_idf_tf(word)
            title_words_table[word] = [(doc.doc_id, math.log(doc.tf[1] + 1) + 0.01) for doc in docs]
            description_words_table[word] = [(doc.doc_id, math.log(doc.tf[2] + 0.01) + 1) for doc in docs]
            all_doc_ids = all_doc_ids.union(set([doc.doc_id for doc in docs]))
            idf_table[word] = idf
            query_vector[word] = (math.log(terms.count(word) + 0.01) + 1) * math.log(len(terms) / (terms.count(word) + 0.01))
        title_doc_vectors = {}  # map of doc and term vector
        des_doc_vectors = {}  # map of doc and term vector
        for doc in all_doc_ids:
            title_vector = []
            des_vector = []
            for term in uniqe_terms:
                find = False
                des_find = False
                for tp in title_words_table[term]:
                    if tp[0] == doc:
                        title_vector.append(tp[1])
                        find = True
                        break
                for tp in description_words_table[term]:
                    if tp[0] == doc:
                        des_vector.append(tp[1])
                        des_find = True
                        break

                if not find:
                    title_vector.append(0)
                if not des_find:
                    des_vector.append(0)
            title_doc_vectors[doc] = title_vector
            des_doc_vectors[doc] = des_vector
        q_v = []
        for i in uniqe_terms:
            q_v.append(query_vector[i])
        return des_doc_vectors, title_doc_vectors, q_v
