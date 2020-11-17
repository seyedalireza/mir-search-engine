import math

def normalize_vector(array):
    norm_term = 0
    for i in array:
        norm_term += i**2
    norm_term = math.sqrt(norm_term)
    return [i / norm_term for i in array]