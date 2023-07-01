import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_aes_ecb(ct: bytes, key: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()


if __name__ == "__main__":
    ct = ''.join(open(os.path.join(os.path.dirname(__file__),
                 "data/task7.txt")).read().splitlines())
    ct = base64.b64decode(ct)

    key = b"YELLOW SUBMARINE"

    print(decrypt_aes_ecb(ct, key).decode('utf-8'))
