from src.normalizer.normalizer import PersianNormalizer, EnglishNormalizer
import hazm
from nltk import word_tokenize

class Corrector:
    def __init__(self, indexer, threshold):
        self.indexer = indexer
        self.threshold = threshold

    def check_persian_query(self, query):
        tokens = hazm.word_tokenize(query)
        word_list = []
        for tuple in PersianNormalizer(1).parse_document(query)[0]:
            word_list.append(tuple[0])
        cor_list = self.spell_check(word_list)
        non_norm_list = []
        for i in range(len(word_list)):
            if word_list[i] == cor_list[i]:
                non_norm_list.append(tokens[i])
            else:
                non_norm_list.append(cor_list[i])
        return [" ".join(cor_list), " ".join(non_norm_list)]

    def check_english_query(self, query):
        tokens = word_tokenize(query)
        word_list = []
        for tuple in EnglishNormalizer(1).parse_document(query)[0]:
            word_list.append(tuple[0])
        cor_list = self.spell_check(word_list)
        non_norm_list = []
        for i in range(len(word_list)):
            if word_list[i] == cor_list[i]:
                non_norm_list.append(tokens[i])
            else:
                non_norm_list.append(cor_list[i])
        return [" ".join(cor_list), " ".join(non_norm_list)]

    #TODo add support for query instead of list of words
    def spell_check(self, word_list):
        correct_list = []
        for word in word_list:
            sim_list = [("", 0)] * self.threshold
            for sim_word in self.indexer.get_similar_words(word):
                self.add_ordered(sim_word, self.calc_jcard(word, sim_word), sim_list)
            #most similar word, and its jacard and edit distance rating
            most_similar = ["", float('inf'), float('inf')]
            for word_val in sim_list:
                edit_dis = self.calc_edit_dis(word_val[0], word)
                if edit_dis < most_similar[2]:
                    most_similar = [word_val[0], word_val[1], edit_dis]
                if edit_dis == most_similar[2] and word_val[1] > most_similar[1]:
                    most_similar = [word_val[0], word_val[1], edit_dis]
            correct_list.append(most_similar[0])
        return correct_list

    def calc_edit_dis(self, word1, word2):
        edit_table = [[0] * (len(word1) + 1) for _ in range(len(word2) + 1)]
        for i in range(len(word1) + 1):
            edit_table[0][i] = i
        for i in range(len(word2) + 1):
            edit_table[i][0] = i
        for i in range(1, len(word2) + 1):
            for j in range(1, len(word1) + 1):
                equal = 1
                if word2[i - 1] == word1[j - 1]:
                    equal = 0
                edit_table[i][j] = min(edit_table[i - 1][j] + 1, edit_table[i][j - 1] + 1, edit_table[i - 1][j - 1] + equal)
        return edit_table[len(word2)][len(word1)]

    def add_ordered(self, word, val, sim_list):
        for i in range(len(sim_list)):
            if sim_list[i][1] < val:
                sim_list.insert(i, (word, val))
                sim_list.pop()

    def calc_jcard(self, word1, word2):
        word1 = "$" + word1 + "$"
        word2 = "$" + word2 + "$"
        dict_word1 = {}
        dict_word2 = {}
        for i in range(len(word1) - 1):
            dict_word1[word1[i:i+2]] = 1
        for i in range(len(word2) - 1):
            dict_word2[word2[i:i+2]] = 1
        inter = 0
        for bigram in dict_word1:
            if bigram in dict_word2:
                inter += 1
        return inter / (len(dict_word1) + len(dict_word2) - inter)
