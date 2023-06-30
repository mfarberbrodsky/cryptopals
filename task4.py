import os
from task3 import single_byte_xor, freq_score


def single_byte_xor_score(ct: bytes) -> float:
    _, pt = single_byte_xor(ct)
    return freq_score(pt)


if __name__ == "__main__":
    strings = [bytes.fromhex(s) for s in open(os.path.join(
        os.path.dirname(__file__), "data/task4.txt")).read().splitlines()]

    best_string = min(strings, key=single_byte_xor_score)
    print(best_string, single_byte_xor(best_string))
