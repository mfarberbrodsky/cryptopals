import os
import base64
from task2 import fixed_xor
from task9 import pkcs7_pad, pkcs7_unpad

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_aes_cbc(pt: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()

    padded_pt = pkcs7_pad(pt, (len(pt)//16 + 1)*16)
    ct = bytearray([])

    prev_block = iv
    for i in range(0, len(padded_pt), 16):
        ct += encryptor.update(fixed_xor(prev_block, padded_pt[i:i+16]))
        prev_block = ct[-16:]
    ct += encryptor.finalize()

    return bytes(ct)


def decrypt_aes_cbc(ct: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()

    pt = bytearray([])
    for i in range(0, len(ct), 16):
        pt += decryptor.update(ct[i:i+16])
    pt += decryptor.finalize()

    return fixed_xor(pt, iv + ct[:-16])


if __name__ == "__main__":
    ct = ''.join(open(os.path.join(os.path.dirname(__file__),
                 "data/task10.txt")).read().splitlines())
    ct = base64.b64decode(ct)

    key = b"YELLOW SUBMARINE"
    IV = b"\x00" * 16

    print(pkcs7_unpad(decrypt_aes_cbc(ct, key, IV)).decode('utf-8'))
