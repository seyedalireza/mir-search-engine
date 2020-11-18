import math

from src.index.DocumentIndex import DocumentIndex


class WordIndex:
    def __init__(self, word):
        self.word = word
        self.doc_list = []
        self.df = 0
        self.idf = 0
        self.sep = "^^"

    def add_new_word(self, normalized_word, doc_count):
        if normalized_word.word != self.word:
            return
        for i in range(len(self.doc_list)):
            if self.doc_list[i].doc_id == normalized_word.doc_id:
                self.doc_list[i].add_p_index(normalized_word.p_type, normalized_word.p_index)
                return
            elif self.doc_list[i].doc_id > normalized_word.doc_id:
                self.doc_list.insert(i, DocumentIndex(normalized_word.doc_id))
                self.doc_list[i].add_p_index(normalized_word.p_type, normalized_word.p_index)
                self.update_df()
                self.update_idf(doc_count)
                return
        self.doc_list.insert(len(self.doc_list), DocumentIndex(normalized_word.doc_id))
        self.doc_list[len(self.doc_list) - 1].add_p_index(normalized_word.p_type, normalized_word.p_index)
        self.update_df()
        self.update_idf(doc_count)

    def delete_document(self, doc_id):
        del_list = []
        for doc in self.doc_list:
            if doc.doc_id == doc_id:
                del_list.append(doc)
        for doc in del_list:
            self.doc_list.remove(doc)
        self.update_df()

    def update_df(self):
        self.df = len(self.doc_list)

    def update_idf(self, doc_count):
        self.idf = math.log(doc_count/self.df, 10)

    def get_idf_tf(self):
        return [self.idf, self.doc_list]

    def get_compressed_str(self):
        out_str = ""
        out_str += self.word
        out_str += self.sep
        out_str += str(self.df) + " " + str(self.idf)
        out_str += self.sep
        for doc in self.doc_list:
            out_str += doc.get_compressed_str()
            out_str += self.sep
        return out_str

    def get_str(self):
        out_str = ""
        out_str += self.word
        out_str += self.sep
        out_str += str(self.df) + " " + str(self.idf)
        out_str += self.sep
        for doc in self.doc_list:
            out_str += doc.get_str()
            out_str += self.sep
        return out_str

    def load_compressed_str(self, in_str: str):
        split_str = in_str.split(self.sep)
        self.word = split_str[0]
        split_df = split_str[1].split(" ")
        self.df = int(split_df[0])
        self.idf = float(split_df[1])
        self.doc_list = []
        for doc in split_str[2:-1]:
            new_doc = DocumentIndex(-1)
            new_doc.load_compressed_str(doc)
            self.doc_list.append(new_doc)

    def load_str(self, in_str: str):
        split_str = in_str.split(self.sep)
        self.word = split_str[0]
        split_df = split_str[1].split(" ")
        self.df = int(split_df[0])
        self.idf = float(split_df[1])
        self.doc_list = []
        for doc in split_str[2:-1]:
            new_doc = DocumentIndex(-1)
            new_doc.load_str(doc)
            self.doc_list.append(new_doc)
