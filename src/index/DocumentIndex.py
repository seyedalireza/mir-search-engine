class DocumentIndex:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.p_index = {"title": [], "desc": []}
        self.tf = [0, 0, 0]
        self.sep = "@@"

    def add_p_index(self, p_type, p_index):
        index_list = self.p_index[p_type]
        for i in range(len(index_list)):
            if index_list[i] > p_index:
                self.p_index[p_type].insert(i, p_index)
                self.update_tf()
                return
        self.p_index[p_type].insert(len(self.p_index[p_type]), p_index)
        self.update_tf()

    def update_tf(self):
        self.tf = [
            len(self.p_index["title"]) + len(self.p_index["desc"]),
            len(self.p_index["title"]),
            len(self.p_index["desc"])
        ]

    def get_str(self):
        out_str = ""
        out_str += str(self.doc_id) + self.sep
        out_str += str(self.tf[1]) + " " + str(self.tf[2]) + self.sep
        for p_index in self.p_index["title"]:
            out_str += str(p_index) + " "
        out_str += self.sep
        for p_index in self.p_index["desc"]:
            out_str += str(p_index) + " "
        return out_str

    def load_str(self, in_str: str):
        split_str = in_str.split(self.sep)
        self.doc_id = int(split_str[0])
        split_tf = split_str[1].split(" ")
        self.tf = [int(split_tf[0]) + int(split_tf[1]), int(split_tf[0]), int(split_tf[1])]
        self.p_index = {"title": [], "desc": []}
        for title_id in split_str[2].split(" ")[:-1]:
            self.p_index["title"].append(title_id)
        for desc_id in split_str[3].split(" ")[:-1]:
            self.p_index["desc"].append(desc_id)
