import string
import random


def random_string_generator(
    size: int = 8, chars: str = string.ascii_lowercase + string.digits
) -> str:
    return "".join(random.choice(chars) for _ in range(size))
