import os


class VBCompressor(object):
    def __init__(self, indexes):
        self.indexes = indexes

    def create_gap_list(self):
        numbers = self.indexes
        if not numbers:
            return []
        return [numbers[0]] + [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]

    def get_byte(self, number):
        ans = ''
        while True:
            ans += str(number % 2)
            if number < 2:
                break
            number = number // 2
        for i in range(8-len(ans)):
            ans += '0'
        return ans[::-1]

    def get_num(self, number):
        bytes_list = []
        while True:
            bytes_list.insert(0, number % 128)
            if number < 128:
                break
            number = number // 128
        bytes_list[-1] += 128
        return ''.join([self.get_byte(i) for i in bytes_list])

    def encode(self):
        lst = self.create_gap_list()
        result = "".join([self.get_num(number) for number in lst])
        return result
