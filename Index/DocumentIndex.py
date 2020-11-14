class DocumentIndex:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.p_index = {"title": [], "desc": []}

    def add_p_index(self, p_type, p_index):
        index_list = self.p_index[p_type]
        for i in range(len(index_list)):
            if index_list[i] > p_index:
                self.p_index[p_type].insert(i, p_index)
                return
        self.p_index[p_type].insert(len(self.p_index[p_type]), p_index)