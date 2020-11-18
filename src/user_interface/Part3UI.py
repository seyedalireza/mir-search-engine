from .UI import UI
from src.compressor.gamma import GammaCompressor
from src.compressor.vb import VBCompressor


def get_query_params():
    print("Enter your numbers: ( separate using space )")
    numbers = list(map(int, input().split()))
    return numbers


class Part3UI(UI):
    def start_UI(self):
        while True:
            self.print_help()
            input_str = int(input())
            encoded = ''
            numbers = get_query_params()
            if input_str == 1:
                encoded = GammaCompressor(indexes=numbers).encode()
            elif input_str == 2:
                encoded = VBCompressor(indexes=numbers).encode()
            elif input_str == 3:
                return
            count = 0
            for i in numbers:
                count += len(str(i))
            print('encoded :', encoded)
            print(len(encoded) * 100 / count / 8, '% saved')

    def print_help(self):
        print("Part 3:")
        print("1- Show The Saved Memory By Using Variable Byte Encoding")
        print("2- Show The Saved Memory By Using Gamma Code Encoding")
        print("3- Exit")
