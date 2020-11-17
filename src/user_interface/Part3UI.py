from user_interface.UI import UI


class Part3UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                #TODO Show The Saved Memory By Using Variable Byte Encoding
                pass
            elif input_str == 2:
                #TODO Show The Saved Memory By Using Gamma Code Encoding
                pass
            elif input_str == 3:
                return

    def print_help(self):
        print("Part 3:")
        print("1- Show The Saved Memory By Using Variable Byte Encoding")
        print("2- Show The Saved Memory By Using Gamma Code Encoding")
        print("3- Exit")
