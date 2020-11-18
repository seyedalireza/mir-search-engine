class GammaCompressor(object):
    def __init__(self, indexes=None):
        self.indexes = indexes

    def get_offset(self, gap):
        return bin(gap)[3:]

    def get_length(self, gap):
        return "".join(["1" for _ in range(len(gap))])+"0"

    def create_gap_list(self):
        numbers = self.indexes
        return [numbers[0]] + [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]

    def encode(self):
        encoded_nums = [self.get_length(self.get_offset(gap)) + self.get_offset(gap) for gap in self.create_gap_list()]
        result = "".join(encoded_nums)
        return result


def decoding(code):
    num, length, offset, aux, res = 0, "", "", 0, []
    while code != "":
        aux = code.find("0")
        length = code[:aux]
        if length == "":
            if len(res) == 0:
                x = 0
            else:
                x = res[-1]
            res.append(1+x)
            code = code[1:]
        else:
            if len(res) == 0:
                x = 0
            else:
                x = res[-1]
            offset = "1" + code[aux + 1:aux + 1 + len(length)]
            res.append(int(offset, 2)+x)
            code = code[aux + 1 + len(length):]
    return res
