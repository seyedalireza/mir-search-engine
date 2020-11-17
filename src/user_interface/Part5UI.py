from src.user_interface.UI import UI


class Part5UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                print("write your query: ")
                query = input()
                print("")
                #TODO Show Result of an Input Query Using tf-idf
                pass
            elif input_str == 2:
                #TODO Show Result of an Input Query Using Proximity Search
                pass
            elif input_str == 3:
                return

    def print_help(self):
        print("Part 5:")
        print("1- Show Result of an Input Query Using tf-idf")
        print("2- Show Result of an Input Query Using Proximity Search")
        print("3- Exit")
