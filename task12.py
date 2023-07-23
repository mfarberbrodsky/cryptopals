from task7 import encrypt_aes_ecb
from task8 import is_ecb

import random
import base64
from typing import Callable

KEY = random.randbytes(16)
SECRET = base64.b64decode(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
)


def ecb_oracle(pt: bytes) -> bytes:
    return encrypt_aes_ecb(pt + SECRET, KEY)


def decrypt_simple(oracle: Callable[[bytes], bytes]) -> bytes:
    padding_len = 1
    prev_len = len(ecb_oracle(b""))
    while True:
        curr_len = len(ecb_oracle(b"A" * padding_len))
        if curr_len > prev_len:
            block_size = curr_len - prev_len
            break
        padding_len += 1

    assert is_ecb(b"A" * (2 * block_size))

    secret_len = len(ecb_oracle(b"")) - padding_len
    secret = bytearray(secret_len)

    for i in range(secret_len):
        ith_byte_block = ecb_oracle(b"A" * (block_size - (i % block_size) - 1))[
            block_size * (i // block_size) : block_size * (i // block_size + 1)
        ]

        # for i < block_size, we're looking at AAAA || secret || byte, for the others we don't need AAA prefix, just the prev block_size-1 secret bytes
        possible_blocks = {
            ecb_oracle(
                (b"A" * block_size + secret)[i + 1 : i + block_size] + bytes([byte])
            )[:block_size]: byte
            for byte in range(256)
        }
        secret[i] = possible_blocks[ith_byte_block]

    return bytes(secret)


if __name__ == "__main__":
    assert decrypt_simple(ecb_oracle) == SECRET
    print(decrypt_simple(ecb_oracle).decode("utf-8"))
