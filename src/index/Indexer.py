from src.index.WordIndex import WordIndex
from src.compressor.gamma import GammaCompressor
from src.compressor.vb import VBCompressor

class Indexer:
    def __init__(self):
        self.word_dict = {}
        self.bigram = {}
        self.doc_set = {}
        self.doc_count = 0
        self.sep = "~~"

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
                            break
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

    def save_index(self, name="indices.txt"):
        address = "../data/" + name
        f = open(address, "w+", encoding="utf-8")
        f.write(self.get_index_str())
        f.close()

    def load_index(self, name="indices.txt"):
        address = "../data/" + name
        f = open(address, "r", encoding="utf-8")
        self.load_index_str(f.read())
        f.close()

    def save_bigram(self, name="bigram.txt"):
        address = "../data/" + name
        f = open(address, "w+", encoding="utf-8")
        f.write(self.get_bigram_str())
        f.close()

    def load_bigram(self, name="bigram.txt"):
        address = "../data/" + name
        f = open(address, "r", encoding="utf-8")
        self.load_bigram_str(f.read())
        f.close()

    def get_index_str(self):
        out_str = ""
        out_str += str(self.doc_count) + self.sep
        for doc in self.doc_set:
            out_str += str(doc) + " "
        out_str += self.sep
        for word in self.word_dict:
            out_str += self.word_dict[word].get_str() + self.sep
        return out_str

    def load_index_str(self, in_str):
        split_str = in_str.split(self.sep)
        self.doc_count = int(split_str[0])
        self.doc_set = {}
        for doc in split_str[1].split(" ")[:-1]:
            self.doc_set[int(doc)] = 1
        self.word_dict = {}
        for word_str in split_str[2:-1]:
            new_word = WordIndex("")
            new_word.load_str(word_str)
            self.word_dict[new_word.word] = new_word

    def get_bigram_str(self):
        out_str = ""
        for bigram in self.bigram:
            out_str += bigram + "@@"
            for word in self.bigram[bigram]:
                out_str += word + " "
            out_str += self.sep
        return out_str

    def load_bigram_str(self, in_str: str):
        split_str = in_str.split(self.sep)
        self.bigram = {}
        for bigram_pair in split_str[:-1]:
            split_pair = bigram_pair.split("@@")
            for word in split_pair[1].split(" ")[:-1]:
                if split_pair[0] in self.bigram:
                    self.bigram[split_pair[0]].append(word)
                else:
                    self.bigram[split_pair[0]] = [word]

    def get_numbers(self):
        count = 0
        lst = []
        for w in self.word_dict:
            for i in self.word_dict[w].doc_list:
                lst.append(i.p_index['title'])
                lst.append(i.p_index['desc'])
                for n in i.p_index['title'] + i.p_index['desc']:
                    count += len((str(n))) + 1

        return count, lst

    def vb_efficiency(self):
        size, lst = self.get_numbers()
        new_size = 0
        for i in lst:
            new_size += len(VBCompressor(indexes=i).encode())
        return new_size * 100 / size / 8

    def gamma_efficiency(self):
        size, lst = self.get_numbers()
        new_size = 0
        for i in lst:
            new_size += len(VBCompressor(indexes=i).encode())
        return new_size * 100 / size / 8
