import os
import base64
from itertools import chain, zip_longest

from task3 import single_byte_xor


def hamming_distance(x: bytes, y: bytes) -> int:
    def num_diff_bits(x, y): return sum((((x ^ y) >> i) & 1) for i in range(8))
    return sum(num_diff_bits(xx, yy) for xx, yy in zip(x, y))


def repeating_key_xor(ct: bytes) -> bytes:
    best_key_sizes = sorted(range(2, min(40, len(
        ct)//2)), key=lambda key_size: (hamming_distance(ct[:key_size], ct[key_size:2*key_size]) + hamming_distance(ct[2*key_size:3*key_size], ct[3*key_size:4*key_size])) / key_size)

    def key_size_score(key_size): return sum(hamming_distance(
        ct[i*key_size:(i+1)*key_size], ct[(i+1)*key_size:(i+2)*key_size]) for i in range(len(ct) // key_size - 1))
    best_key_sizes = sorted(range(2, min(40, len(ct)//2)), key=key_size_score)

    for key_size in best_key_sizes[:3]:
        single_byte_xors = [ct[i::key_size] for i in range(key_size)]
        partial_pts = [single_byte_xor(part)[1] for part in single_byte_xors]
        if not all(partial_pt is not None for partial_pt in partial_pts):
            continue
        pt = bytes(chain.from_iterable(zip_longest(
            *partial_pts, fillvalue=0)))[:len(ct)]
        return pt


if __name__ == "__main__":
    assert hamming_distance(b"this is a test", b"wokka wokka!!!") == 37

    ct = ''.join(open(os.path.join(os.path.dirname(__file__),
                 "data/task6.txt")).read().splitlines())
    ct = base64.b64decode(ct)

    print(repeating_key_xor(ct).decode('utf-8'))
