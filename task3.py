from collections import Counter
from task2 import fixed_xor
import string

ENGLISH_FREQ = {
    "E": 0.12003601080324099,
    "T": 0.09102730819245775,
    "A": 0.08122436731019306,
    "O": 0.07682304691407423,
    "I": 0.0731219365809743,
    "N": 0.06952085625687708,
    "S": 0.06281884565369612,
    "R": 0.06021806541962589,
    "H": 0.05921776532959889,
    "D": 0.04321296388916676,
    "L": 0.03981194358307493,
    "U": 0.028808642592777836,
    "C": 0.027108132439731925,
    "M": 0.026107832349704915,
    "F": 0.02300690207062119,
    "Y": 0.021106331899569872,
    "W": 0.02090627188156447,
    "G": 0.020306091827548264,
    "P": 0.01820546163849155,
    "B": 0.014904471341402423,
    "V": 0.011103330999299792,
    "K": 0.006902070621186356,
    "X": 0.0017005101530459142,
    "Q": 0.0011003300990297092,
    "J": 0.0010003000900270084,
    "Z": 0.0007002100630189059,
}


def freq_score(text: bytes) -> float:
    text_freq = {ch: 0 for ch in ENGLISH_FREQ}
    text_freq[None] = 0

    try:
        if not all(ch in string.printable for ch in text.decode("utf-8")):
            return float("inf")
    except:
        return float("inf")

    for ch in text:
        english_ch = chr(ch).upper()
        if english_ch in ENGLISH_FREQ:
            text_freq[english_ch] += 1
        else:
            text_freq[None] += 1

    text_freq = {ch: freq / sum(text_freq.values()) for ch, freq in text_freq.items()}
    return sum((text_freq.get(ch) - ENGLISH_FREQ.get(ch, 0)) ** 2 for ch in text_freq)


def single_byte_xor(ct: bytes) -> tuple[int, bytes]:
    best_freq_score = float("inf")
    best_res = (None, None)

    for key in range(256):
        pt = fixed_xor(ct, bytes([key] * len(ct)))

        pt_score = freq_score(pt)
        if pt_score < best_freq_score:
            best_freq_score = pt_score
            best_res = (key, pt)

    return best_res


if __name__ == "__main__":
    print(
        single_byte_xor(
            bytes.fromhex(
                "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
            )
        )
    )
