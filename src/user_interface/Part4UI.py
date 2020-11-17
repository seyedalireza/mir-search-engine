from src.user_interface.UI import UI


class Part4UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                #TODO Show Correct Form of an Input Query
                pass
            elif input_str == 2:
                #TODO Calculate Jacard Distance of Two Input Words
                pass
            elif input_str == 3:
                #TODO Calculate Edit Distance of Two Input Words
                pass
            elif input_str == 4:
                return

    def print_help(self):
        print("Part 4:")
        print("1- Show Correct Form of an Input Query")
        print("2- Calculate Jacard Distance of Two Input Words")
        print("3- Calculate Edit Distance of Two Input Words")
        print("4- Exit")
