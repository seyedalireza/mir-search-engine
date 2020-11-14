from Index.WordIndex import WordIndex


class Indexer:
    def __init__(self):
        self.word_list = []

    def create_index(self, word_list):
        for n_word in word_list:
            found_word = None
            for word in self.word_list:
                if word.word == n_word.word:
                    found_word = word
            if found_word is None:
                self.word_list.insert(len(self.word_list), WordIndex(n_word.word))
                self.word_list[len(self.word_list) - 1].add_new_word(n_word)
            else:
                found_word.add_new_word(n_word)