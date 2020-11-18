from .UI import UI


class Part3UI(UI):
    def start_UI(self):
        english_size, persian_size = 2493398, 22845663
        while True:
            self.print_help()
            input_str = int(input())
            if input_str == 1:
                print('english, before: ', english_size, 'after:', english_size+self.english_indexer.vb_efficiency()/8, 'bytes')
                print('persian, before: ', persian_size, 'after:', persian_size+self.persian_indexer.vb_efficiency()/8, 'bytes')
            elif input_str == 2:
                print('english, before: ', english_size, 'after:', english_size + self.english_indexer.gamma_efficiency()/8,
                      'bytes')
                print('persian, before: ', persian_size, 'after:',
                      persian_size + self.persian_indexer.gamma_efficiency()/8, 'bytes')
            elif input_str == 3:
                return

    def print_help(self):
        print("Part 3:")
        print("1- Show The Saved Memory By Using Variable Byte Encoding")
        print("2- Show The Saved Memory By Using Gamma Code Encoding")
        print("3- Exit")
