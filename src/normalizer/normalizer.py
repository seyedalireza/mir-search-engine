from collections import Counter

import hazm
import nltk
from nltk.stem import SnowballStemmer
from nltk import WordNetLemmatizer, word_tokenize
from hazm import Normalizer, word_tokenize, Stemmer, Lemmatizer
import nltk
import ssl

def just_in_case(pack):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download(pack)

# first download wordnet
try:
    nltk.download("wordnet")
    nltk.download("punkt")
except:
    just_in_case('wordnet')
    just_in_case('punkt')


class EnglishNormalizer:

    def __init__(self, most_used_threshold):
        self.most_used_threshold = most_used_threshold

    def parse_document(self, doc):
        """
        :param doc: an English String document
        :return: normalized document words with their position, most used words
        """
        tokens = word_tokenize(doc)
        tokens = [(tokens[i], i) for i in range(len(tokens))]

        # normalization
        tokens = [("".join(c for c in word[0] if c.isalnum()), word[1]) for word in tokens]
        tokens = [word for word in tokens if word[0].isalpha() or word[0].isnumeric()]
        tokens = [(word[0].lower(), word[1]) for word in tokens]

        # lemmatization
        lemma = WordNetLemmatizer()
        tokens = [(lemma.lemmatize(word[0]), word[1]) for word in tokens]

        # stemming
        snowball = SnowballStemmer("english")
        tokens = [(snowball.stem(word[0]), word[1]) for word in tokens]

        # remove stop words
        word_count = Counter([word[0] for word in tokens])

        # TODO: we can use stop words of other libraries
        if len(tokens) >= 20:
            stop_words = [word[0] for word in tokens if word_count.get(word[0]) / len(tokens) > self.most_used_threshold]
        else:
            stop_words = []
        return list(filter(lambda x: x[0] not in stop_words, tokens)), set(stop_words)


class PersianNormalizer:

    def __init__(self, most_used_threshold):
        self.most_used_threshold = most_used_threshold
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()

    def parse_document(self, doc):
        """
        :param doc: a Persian string document
        :return: normalized document words with their position, most used words
        """
        # normalize
        normalized_doc = self.normalizer.normalize(doc)

        # tokenize
        tokens = hazm.word_tokenize(normalized_doc)
        tokens = [(tokens[i], i) for i in range(len(tokens))]
        tokens = [("".join(c for c in word[0] if c.isalnum()), word[1]) for word in tokens]
        tokens = [word for word in tokens if word[0].isalnum()]

        # stemming
        tokens = [(self.stemmer.stem(word[0]), word[1]) for word in tokens]

        # lemmatizer
        tokens = [(self.lemmatizer.lemmatize(word[0]), word[1]) for word in tokens]

        # remove stop words
        word_count = Counter([word[0] for word in tokens])

        # TODO: we can use stop words of other libraries
        if len(tokens) >= 20:
            stop_words = [word[0] for word in tokens if
                          word_count.get(word[0]) / len(tokens) > self.most_used_threshold]
        else:
            stop_words = []
        return list(filter(lambda x: x[0] not in stop_words, tokens)), set(stop_words)
