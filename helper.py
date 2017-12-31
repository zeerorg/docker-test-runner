import random
import string


def get_rand_str(length=5):
    return ''.join(random.choices(string.ascii_letters, k=length))
