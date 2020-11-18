from src.correction.Corrector import Corrector
from .UI import UI


class Part4UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert Query:")
                    cor_form = Corrector(self.persian_indexer, 10).check_persian_query(input())
                    print("Regular Form: ")
                    print(cor_form[1])
                    print("Normalized Form:")
                    print(cor_form[0])
                elif lang_input == 2:
                    print("Insert Query:")
                    cor_form = Corrector(self.english_indexer, 10).check_english_query(input())
                    print("Regular Form: ")
                    print(cor_form[1])
                    print("Normalized Form:")
                    print(cor_form[0])
                elif lang_input == 3:
                    continue
            elif input_str == 2:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert Two Words:")
                    dis = Corrector(self.persian_indexer, 10).calc_jcard(input(), input())
                    print("Jacard Distance:")
                    print(dis)
                elif lang_input == 2:
                    print("Insert Two Words:")
                    dis = Corrector(self.english_indexer, 10).calc_jcard(input(), input())
                    print("Jacard Distance:")
                    print(dis)
                elif lang_input == 3:
                    continue
            elif input_str == 3:
                self.request_lang()
                lang_input = int(input())
                if lang_input == 1:
                    print("Insert Two Words:")
                    dis = Corrector(self.persian_indexer, 10).calc_edit_dis(input(), input())
                    print("Edit Distance:")
                    print(dis)
                elif lang_input == 2:
                    print("Insert Two Words:")
                    dis = Corrector(self.english_indexer, 10).calc_edit_dis(input(), input())
                    print("Edit Distance:")
                    print(dis)
                elif lang_input == 3:
                    continue
            elif input_str == 4:
                return

    def print_help(self):
        print("Part 4:")
        print("1- Show Correct Form of an Input Query")
        print("2- Calculate Jacard Distance of Two Input Words")
        print("3- Calculate Edit Distance of Two Input Words")
        print("4- Exit")
