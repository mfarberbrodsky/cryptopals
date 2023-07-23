def pkcs7_pad(block: bytes, size: int = 16) -> bytes:
    return block + bytes([size - len(block)] * (size - len(block)))


def pkcs7_unpad(block: bytes) -> bytes:
    pad_length = block[-1]
    return block[:-pad_length]


if __name__ == "__main__":
    assert pkcs7_pad(b"YELLOW SUBMARINE", 20) == b"YELLOW SUBMARINE\x04\x04\x04\x04"
