from src.index.Indexer import Indexer
import numpy as np
from src.normalizer.normalizer import EnglishNormalizer, PersianNormalizer


class ProximitySearchEngine(object):
    def __init__(self, gt, lt, indexer: Indexer):  # greater than ... and less than ...
        self.dist = (gt, lt)
        self.indexer = indexer
        self.en_normalizer = EnglishNormalizer(0.10)
        self.fa_normalizer = PersianNormalizer(0.1)

    def



