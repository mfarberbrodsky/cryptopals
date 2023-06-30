import os
import base64


def is_ecb(ct):
    blocks = [ct[i:i+16] for i in range(len(ct))]
    return len(set(blocks)) != len(blocks)


if __name__ == "__main__":
    cts = [bytes.fromhex(ct) for ct in open(os.path.join(os.path.dirname(__file__),
                                                         "data/task8.txt")).read().splitlines()]

    for ct in cts:
        if is_ecb(ct):
            print(ct)
