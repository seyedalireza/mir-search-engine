import math
from index.Indexer import Indexer
import numpy as np
from normalizer.normalizer import EnglishNormalizer, PersianNormalizer


class TfIdfSearchEngine:

    def __init__(self, indexer: Indexer):
        self.indexer = indexer
        self.en_normalizer = EnglishNormalizer(0.10)
        self.fa_normalizer = PersianNormalizer(0.1)

    def search_english(self, query, in_title: bool = True, in_description: bool = True, english: bool = True):
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
        total_keys.sort(key=lambda x: total_keys[x], reverse=True)
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
            title_words_table[word] = [(doc.doc_id, math.log(doc.tf[1]) + 1) for doc in docs]
            description_words_table[word] = [(doc.doc_id, math.log(doc.tf[2]) + 1) for doc in docs]
            all_doc_ids += [doc.doc_id for doc in docs]
            idf_table[word] = idf
            query_vector[word] = (math.log(terms.count(word)) + 1) * math.log(len(terms) / terms.count(word))
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
        return des_doc_vectors, title_doc_vectors, query_vector


def normalize_vector(array):
    norm_term = 0
    for i in array:
        norm_term += i**2
    norm_term = math.sqrt(norm_term)
    return [i / norm_term for i in array]