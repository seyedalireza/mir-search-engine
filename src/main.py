# from src.index.Indexer import Indexer
from src.index.DocumentIndex import DocumentIndex
from src.index.Indexer import Indexer
from src.index.NormalizedWord import NormalizedWord
from src.parser import EnglishCollectionParser, PersianCollectionParser
from src.user_interface.MainUI import MainUI

# english_parser = EnglishCollectionParser()
# persian_parser = PersianCollectionParser()
# english_indexer = Indexer()
# persian_indexer = Indexer()
# english_indexer.create_index(english_parser.get_all_words())
# persian_indexer.create_index(persian_parser.get_all_words())
# print("here")
# MainUI(english_indexer, persian_indexer).start_UI()
# english_indexer.save_index()

english_indexer = Indexer()
english_indexer.create_index(
    [
        NormalizedWord("sajjd", 1, "title", 3),
        NormalizedWord("sa", 2, "title", 3),
        NormalizedWord("sajadfjd", 3, "desc", 3),
        NormalizedWord("sa", 1, "desc", 3),
    ]
)
english_indexer.save_index()
english_indexer.save_bigram()
i = Indexer()
i.load_index()
i.load_bigram()
print()