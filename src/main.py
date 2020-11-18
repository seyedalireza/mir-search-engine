from src.correction.Corrector import Corrector
from src.index.Indexer import Indexer
from src.index.NormalizedWord import NormalizedWord
from src.parser import EnglishCollectionParser, PersianCollectionParser
from src.user_interface.MainUI import MainUI
#
# to create a new save uncomment these
# english_indexer = Indexer()
# persian_indexer = Indexer()
# english_parser = EnglishCollectionParser()
# persian_parser = PersianCollectionParser()
# english_indexer.create_index(english_parser.get_all_words())
# persian_indexer.create_index(persian_parser.get_all_words())
# print("start saving")
# english_indexer.save_bigram("eng_bigram.txt")
# english_indexer.save_index("eng_index.txt")
# print("saved english")
# persian_indexer.save_bigram("per_bigram.txt")
# persian_indexer.save_index("per_index.txt")
# print("saved persian")

english_indexer = Indexer()
persian_indexer = Indexer()
english_indexer.load_bigram("eng_bigram.txt")
english_indexer.load_index("eng_index.txt")
persian_indexer.load_bigram("per_bigram.txt")
persian_indexer.load_index("per_index.txt")

MainUI(english_indexer, persian_indexer).start_UI()

