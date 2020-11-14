from Index.WordIndex import WordIndex


class Indexer:
    def __init__(self):
        self.word_dict = {}
        self.bigram = {}

    def create_index(self, word_list):
        for n_word in word_list:
            if n_word.word in self.word_dict:
                self.word_dict[n_word.word].add_new_word(n_word)
            else:
                self.word_dict[n_word.word] = WordIndex(n_word.word)
                self.word_dict[n_word.word].add_new_word(n_word)
                self.add_bigram(n_word.word)

    def add_bigram(self, word):
        con_word = "$" + word + "$"
        for i in range(len(con_word) - 1):
            bigram = con_word[i:i+2]
            if bigram in self.bigram:
                if word not in self.bigram[bigram]:
                    for j in range(len(self.bigram[bigram])):
                        if self.bigram[bigram][j] > word:
                            self.bigram[bigram].insert(j, word)
                            return
                    self.bigram[bigram].append(word)
            else:
                self.bigram[bigram] = []
                self.bigram[bigram].append(word)
