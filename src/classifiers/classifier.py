import pandas as pd
import numpy as np


from src.normalizer.normalizer import EnglishNormalizer
from src.transformer.transformer import Transformer


class Classifier:

    def __init__(self, transformer: Transformer):
        self.transformer = transformer
        self.normalizer = EnglishNormalizer(0.1)
        self.des_model = None
        self.title_model = None

    def predict(self, text):
        pass

    def predict_vector(self, vector):
        pass

    def train(self):
        pass
