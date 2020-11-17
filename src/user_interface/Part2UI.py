from .UI import UI


class Part2UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                #TODO Show Posting List of an Input Word
                pass
            elif input_str == 2:
                #TODO Show Positional Index of an Input Word
                pass
            elif input_str == 3:
                #TODO Show Words that Share an Input Bigram
                pass
            elif input_str == 4:
                return

    def print_help(self):
        print("Part 2:")
        print("1- Show Posting List of an Input Word")
        print("2- Show Positional Index of an Input Word")
        print("3- Show Words that Share an Input Bigram")
        print("4- Exit")
