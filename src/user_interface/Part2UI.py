from src.normalizer.normalizer import PersianNormalizer, EnglishNormalizer
from src.parser import PersianCollectionParser, EnglishCollectionParser
from .UI import UI


class Part2UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert a Word:")
                    word = input()
                    word = PersianNormalizer(100).parse_document(word)[0][0][0]
                    for doc in self.persian_indexer.word_dict[word].doc_list:
                        print(doc.doc_id, end=" ")
                    print()
                elif lang_input == 2:
                    print("Insert a Word:")
                    word = input()
                    word = EnglishNormalizer(100).parse_document(word)[0][0][0]
                    for doc in self.english_indexer.word_dict[word].doc_list:
                        print(doc.doc_id, end=" ")
                    print()
                elif lang_input == 3:
                    continue
            elif input_str == 2:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert a Word:")
                    word = input()
                    word = PersianNormalizer(100).parse_document(word)[0][0][0]
                    for doc in self.persian_indexer.word_dict[word].doc_list:
                        print(doc.doc_id, end=" ")
                        print(doc.p_index)
                elif lang_input == 2:
                    print("Insert a Word:")
                    word = input()
                    word = EnglishNormalizer(100).parse_document(word)[0][0][0]
                    for doc in self.english_indexer.word_dict[word].doc_list:
                        print(doc.doc_id, end=" ")
                        print(doc.p_index)
                elif lang_input == 3:
                    continue
            elif input_str == 3:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert a Bigram:")
                    bigram = input()
                    if bigram in self.persian_indexer.bigram:
                        print(self.persian_indexer.bigram[bigram])
                    else:
                        print("No Such Bigram Exists")
                elif lang_input == 2:
                    print("Insert a Bigram:")
                    bigram = input()
                    if bigram in self.english_indexer.bigram:
                        print(self.english_indexer.bigram[bigram])
                    else:
                        print("No Such Bigram Exists")
                elif lang_input == 3:
                    continue
            elif input_str == 4:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert Your New Document Location")
                    doc_loc = input()
                    self.persian_indexer.create_index(PersianCollectionParser(doc_loc).get_all_words())
                elif lang_input == 2:
                    print("Insert Your New Document Location")
                    doc_loc = input()
                    self.english_indexer.create_index(EnglishCollectionParser(doc_loc).get_all_words())
                elif lang_input == 3:
                    continue
            elif input_str == 5:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert Your New Document ID")
                    doc_id = int(input())
                    self.persian_indexer.delete_document(doc_id)
                elif lang_input == 2:
                    print("Insert Your New Document ID")
                    doc_id = int(input())
                    self.english_indexer.delete_document(doc_id)
                elif lang_input == 3:
                    continue
            elif input_str == 6:
                return

    def print_help(self):
        print("Part 2:")
        print("1- Show Posting List of an Input Word")
        print("2- Show Positional Index of an Input Word")
        print("3- Show Words that Share an Input Bigram")
        print("4- َ Add New Document")
        print("5- Remove a Document")
        print("6- Exit")
