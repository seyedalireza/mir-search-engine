import os


class GammaCompressor(object):
    def __init__(self, index_file_address='../test/compressor_index_test.txt'):
        self.index_file = index_file_address
        file_stat = os.stat(self.index_file)
        print(file_stat.st_size / (1024 * 1024))

    def get_offset(self, gap):
        return bin(gap)[3:]

    def get_length(self, gap):
        return "".join(["1" for _ in range(len(gap))])+"0"

    def create_gap_list(self):
        numbers = []
        with open(self.index_file, 'r') as file:
            lst = file.readlines()
            for line in lst:
                numbers.extend(list(map(int, line.split())))
        return [numbers[0]] + [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]

    def encode(self):
        encoded_nums = [self.get_length(self.get_offset(gap)) + self.get_offset(gap) for gap in self.create_gap_list()]
        result = "".join(encoded_nums)
        with open('../../test/compressing_res.txt', 'w') as file:
            file.write(result)
        return '../test/compressing_res.txt'


x = GammaCompressor()
z = x.encode()
z_stat = os.stat(z)
print(z_stat.st_size / (1024 * 1024))
