from src.user_interface.UI import UI


class Part1UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                #TODO Show the Normalized Form of a Query
                pass
            elif input_str == 2:
                #TODO Show Stop Words
                pass
            elif input_str == 3:
                return

    def print_help(self):
        print("Part 1:")
        print("1- Show the Normalized Form of a Query")
        print("2- Show Stop Words")
        print("3- Exit")
