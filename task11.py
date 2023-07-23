from task7 import encrypt_aes_ecb
from task10 import encrypt_aes_cbc
from task8 import is_ecb

import random
from typing import Callable


def encryption_oracle(pt: bytes) -> bytes:
    key, iv = random.randbytes(16), random.randbytes(16)

    if random.randint(0, 1):
        print("Encrypting ecb")
        return encrypt_aes_ecb(pt, key)
    else:
        print("Encrypting cbc")
        return encrypt_aes_cbc(pt, key, iv)


def is_ecb_oracle(oracle: Callable[[bytes], bytes]) -> bool:
    return is_ecb(oracle(b"\x00" * 32))


if __name__ == "__main__":
    print(is_ecb_oracle(encryption_oracle))
