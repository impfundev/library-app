import random
import string


def generate_unique_number(digit: int):
    while True:
        number = "".join(random.choices(string.digits, k=digit))
        if not is_number_used(number):
            return number


def is_number_used(number):
    return False
