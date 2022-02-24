import string
import random


def generate_strong_password(length = 10):
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!@#$%^&*()")

    alphabets_length = random.randint(1, length - 2)
    digits_length = random.randint(1, length - alphabets_length - 1)
    special_characters_length = length - alphabets_length - digits_length

    alphabets_string = [random.choice(alphabets) for _ in range(alphabets_length)]
    digits_string = [random.choice(digits) for _ in range(digits_length)]
    special_characters_string = [random.choice(special_characters) for _ in range(special_characters_length)]
    characters_string = alphabets_string + digits_string + special_characters_string
    random.shuffle(characters_string)

    return "".join(characters_string)
