from classifiers.classification_generator import ClassificationGenerator
from classifiers.random_forest import RF
from src.classifiers.naive_bayes import NB
from src.correction.Corrector import Corrector
from src.index.DocumentIndex import DocumentIndex
from src.index.Indexer import Indexer
from src.index.NormalizedWord import NormalizedWord
from src.parser import EnglishCollectionParser, PersianCollectionParser
from src.transformer.transformer import Transformer
from src.classifiers.KNN import KNN
from src.classifiers.SVM import SVM
from src.user_interface.MainUI import MainUI


english_indexer = Indexer()
persian_indexer = Indexer()
english_indexer.load_bigram("eng_bigram.txt")
english_indexer.load_index("eng_comp_index.txt")
persian_indexer.load_bigram("per_bigram.txt")
persian_indexer.load_index("per_comp_index.txt")
MainUI(english_indexer, persian_indexer).start_UI()
