import base64


def hex_to_base64(s: str) -> str:
    return base64.b64encode(bytes.fromhex(s)).decode("utf-8")


if __name__ == "__main__":
    assert (
        hex_to_base64(
            "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        )
        == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    )
