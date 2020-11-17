from src.index.Indexer import Indexer


class UI:
    def __init__(self, english_indexer: Indexer, persian_indexer: Indexer):
        self.english_indexer = english_indexer
        self.persian_indexer = persian_indexer

    def start_UI(self):
        print("Start")

    def print_help(self):
        print("help")

    def request_lang(self):
        print("Select Your language: ")
        print("1- Persian")
        print("2- English")
        print("3- Exit")