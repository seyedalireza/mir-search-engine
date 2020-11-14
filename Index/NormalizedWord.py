class NormalizedWord:
    def __init__(self, word, doc_id, p_type, p_index):
        self.word = word
        self.doc_id = doc_id
        self.p_index = p_index
        # should be either "title" or "desc"
        self.p_type = p_type
