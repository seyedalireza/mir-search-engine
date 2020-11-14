from Index.DocumentIndex import DocumentIndex


class WordIndex:
    def __init__(self, word):
        self.word = word
        self.doc_list = []
        self.df = 0

    def add_new_word(self, normalized_word):
        if normalized_word.word != self.word:
            return
        for i in range(len(self.doc_list)):
            if self.doc_list[i].doc_id == normalized_word.doc_id:
                self.doc_list[i].add_p_index(normalized_word.p_type, normalized_word.p_index)
                return
            elif self.doc_list[i].doc_id > normalized_word.doc_id:
                self.doc_list.insert(i, DocumentIndex(normalized_word.doc_id))
                self.doc_list[i].add_p_index(normalized_word.p_type, normalized_word.p_index)
                self.update_tf()
                return
        self.doc_list.insert(len(self.doc_list), DocumentIndex(normalized_word.doc_id))
        self.doc_list[len(self.doc_list) - 1].add_p_index(normalized_word.p_type, normalized_word.p_index)
        self.update_tf()

    def delete_document(self, doc_id):
        del_list = []
        for doc in self.doc_list:
            if doc.doc_id == doc_id:
                del_list.append(doc)
        for doc in del_list:
            self.doc_list.remove(doc)
        self.update_tf()

    def update_tf(self):
        self.df = len(self.doc_list)

