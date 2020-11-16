class NormalizedWord:
    def __init__(self, word, doc_id, p_type, p_index):
        self.word = word
        self.doc_id = doc_id
        self.p_index = p_index
        # should be either "title" or "desc"
        self.p_type = p_type

    def __str__(self):
        return str.format("normalized word = word: {} , doc_id: {}, p_index: {}, p_type: {};",
                          self.word, self.doc_id, self.p_index, self.p_type)

    def __repr__(self):
        return self.__str__()