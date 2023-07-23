from task10 import encrypt_aes_cbc, decrypt_aes_cbc
from task2 import fixed_xor

import random

KEY = random.randbytes(16)
IV = random.randbytes(16)


def cbc_weird_oracle(pt: bytes) -> bytes:
    pt = pt.replace(b";", b"%3B").replace(b"=", b"%3D")
    return encrypt_aes_cbc(
        b"comment1=cooking%20MCs;userdata="
        + pt
        + b";comment2=%20like%20a%20pound%20of%20bacon",
        KEY,
        IV,
    )


def is_admin(ct: bytes) -> bytes:
    return b";admin=true;" in decrypt_aes_cbc(ct, KEY, IV)


def make_admin() -> bytes:
    blank_ct = cbc_weird_oracle(b"\x00" * 16)
    return (
        blank_ct[:16] + fixed_xor(blank_ct[16:32], b"aaaaa;admin=true") + blank_ct[32:]
    )


if __name__ == "__main__":
    assert not is_admin(cbc_weird_oracle(b";admin=true;"))
    assert is_admin(make_admin())
