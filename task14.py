from task7 import encrypt_aes_ecb
from task12 import decrypt_simple

import random
import base64
from typing import Callable

KEY = random.randbytes(16)
SECRET = base64.b64decode(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
)
RANDOM_PREFIX = random.randbytes(random.randint(1, 100))


def ecb_rand_oracle(pt: bytes) -> bytes:
    return encrypt_aes_ecb(RANDOM_PREFIX + pt + SECRET, KEY)


def decrypt_hard(oracle: Callable[[bytes], bytes]) -> bytes:
    block_size = 16

    ct1, ct2 = oracle(b"A"), oracle(b"B")
    for prefix_len_div in range(len(ct1) // block_size):
        if (
            ct1[prefix_len_div * block_size : (prefix_len_div + 1) * block_size]
            != ct2[prefix_len_div * block_size : (prefix_len_div + 1) * block_size]
        ):
            break

    for prefix_len_mod in range(block_size):
        ct = oracle(b"A" * (block_size - prefix_len_mod) + b"B" * (2 * block_size))
        if (
            ct[(prefix_len_div + 1) * block_size : (prefix_len_div + 2) * block_size]
            == ct[(prefix_len_div + 2) * block_size : (prefix_len_div + 3) * block_size]
        ):
            break

    prefix_len = prefix_len_div * block_size + prefix_len_mod

    def det_oracle(pt: bytes) -> bytes:
        return oracle(b"A" * (block_size - prefix_len_mod) + pt)[
            (prefix_len_div + 1) * block_size :
        ]

    return decrypt_simple(det_oracle)


if __name__ == "__main__":
    assert decrypt_hard(ecb_rand_oracle) == SECRET
    print(decrypt_hard(ecb_rand_oracle).decode("utf-8"))
