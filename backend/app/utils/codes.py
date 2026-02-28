import random
import string

ALPHABET = string.ascii_uppercase + string.digits


def generate_public_code(length: int = 12) -> str:
    return ''.join(random.choices(ALPHABET, k=length))
