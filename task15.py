def pkcs7_unpad(padded: bytes) -> bytes:
    if len(padded) == 0:
        raise ValueError("Bad padding! Too short.")

    pad_length = padded[-1]
    if len(padded) < pad_length:
        raise ValueError("Bad padding! Too short.")

    for i in range(pad_length):
        if padded[-i - 1] != pad_length:
            raise ValueError("Bad padding! Wrong last bytes.")

    return padded[:-pad_length]


if __name__ == "__main__":
    assert pkcs7_unpad(b"ICE ICE BABY\x04\x04\x04\x04") == b"ICE ICE BABY"
