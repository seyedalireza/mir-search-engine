from src.index.WordIndex import WordIndex


class Indexer:
    def __init__(self):
        self.word_dict = {}
        self.bigram = {}
        self.doc_set = {}
        self.doc_count = 0

    def create_index(self, word_list):
        for n_word in word_list:
            if n_word.doc_id not in self.doc_set:
                self.doc_set[n_word.doc_id] = 1
                self.update_doc_count()
            if n_word.word in self.word_dict:
                self.word_dict[n_word.word].add_new_word(n_word, self.doc_count)
            else:
                self.word_dict[n_word.word] = WordIndex(n_word.word)
                self.word_dict[n_word.word].add_new_word(n_word, self.doc_count)
                self.add_bigram(n_word.word)

    def add_bigram(self, word):
        con_word = "$" + word + "$"
        for i in range(len(con_word) - 1):
            bigram = con_word[i:i+2]
            if bigram in self.bigram:
                if word not in self.bigram[bigram]:
                    index = -1
                    for j in range(len(self.bigram[bigram])):
                        if self.bigram[bigram][j] > word:
                            index = j
                    if index == -1:
                        index = len(self.bigram[bigram]) - 1
                    self.bigram[bigram].insert(index, word)
            else:
                self.bigram[bigram] = []
                self.bigram[bigram].append(word)

    def delete_document(self, doc_id):
        for word in self.word_dict:
            self.word_dict[word].delete_document(doc_id)
        del_list = []
        for word in self.word_dict:
            if self.word_dict[word].df == 0:
                del_list.append(word)
        for word in del_list:
            self.word_dict.pop(word)
            self.delete_bigram(word)
        self.check_bigram()
        if doc_id in self.doc_set:
            self.doc_set.pop(doc_id)
            self.update_doc_count()

    def delete_bigram(self, word):
        con_word = "$" + word + "$"
        for i in range(len(con_word) - 1):
            bigram = con_word[i:i + 2]
            if word in self.bigram[bigram]:
                self.bigram[bigram].remove(word)

    def check_bigram(self):
        del_list = []
        for bigram in self.bigram:
            if len(self.bigram[bigram]) == 0:
                del_list.append(bigram)
        for bigram in del_list:
            self.bigram.pop(bigram)

    def update_doc_count(self):
        self.doc_count = len(self.doc_set)
        for word in self.word_dict:
            self.word_dict[word].update_idf(self.doc_count)

    def get_idf_tf(self, word):
        return self.word_dict[word].get_idf_tf()

    def get_similar_words(self, word):
        word = "$" + word + "$"
        sim_set = set()
        for i in range(len(word) - 1):
            if word[i:i+2] in self.bigram:
                sim_set.update(self.bigram[word[i:i+2]])
        return sim_set
