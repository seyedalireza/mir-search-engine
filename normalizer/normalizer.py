from collections import Counter

import nltk
from nltk.stem import SnowballStemmer
from nltk import WordNetLemmatizer, word_tokenize
from hazm import Normalizer, word_tokenize, Stemmer, Lemmatizer

# first download
nltk.download("wordnet")

class EnglishNormalizer:

    def __init__(self, most_used_threshold):
        self.most_used_threshold = most_used_threshold

    def parse_document(self, doc):
        """
        :param doc: a String document
        :return: normalized document, most used words
        """
        tokens = word_tokenize(doc)

        # normalization
        tokens = [word for word in tokens if word.isalpha() or word.isnumeric()]
        tokens = [word.lower() for word in tokens]

        # lemmatization
        lemma = WordNetLemmatizer()
        tokens = [lemma.lemmatize(word) for word in tokens]

        # stemming
        snowball = SnowballStemmer("english")
        tokens = [snowball.stem(word) for word in tokens]

        # remove stop words
        word_count = Counter(tokens)

        # TODO: we can use stop words of other libraries
        stop_words = [word for word in tokens if word_count.get(word) / len(tokens) < self.most_used_threshold]
        return list(filter(lambda x: x not in stop_words, tokens)), set(stop_words)


class PersianNormalizer:

    def __init__(self, most_used_threshold):
        self.most_used_threshold = most_used_threshold

    def parse_document(self, doc):
        # normalize
        normalizer = Normalizer()
        normalized_doc = normalizer.normalize(doc)

        # tokenize
        tokens = word_tokenize(normalized_doc)
        tokens = [word for word in tokens if word.isalpha() or word.isnumeric()]

        # stemming
        stemmer = Stemmer()
        tokens = [stemmer.stem(word) for word in tokens]

        # lemmatizer
        lemmatizer = Lemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

        # remove stop words
        word_count = Counter(tokens)

        # TODO: we can use stop words of other libraries
        stop_words = [word for word in tokens if word_count.get(word) / len(tokens) < self.most_used_threshold]
        return list(filter(lambda x: x not in stop_words, tokens)), set(stop_words)
