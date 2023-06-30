def fixed_xor(x: bytes, y: bytes) -> bytes:
    assert len(x) == len(y)
    return bytes(xx ^ yy for xx, yy in zip(x, y))


if __name__ == "__main__":
    assert fixed_xor(bytes.fromhex("1c0111001f010100061a024b53535009181c"), bytes.fromhex(
        "686974207468652062756c6c277320657965")) == bytes.fromhex("746865206b696420646f6e277420706c6179")
