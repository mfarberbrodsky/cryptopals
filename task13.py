from task7 import encrypt_aes_ecb, decrypt_aes_ecb
from task9 import pkcs7_unpad, pkcs7_pad
import random
from typing import Callable

KEY = random.randbytes(16)


def kv_parse(cookie: str) -> dict[str, str]:
    return dict(s.split("=") for s in cookie.split("&"))


def profile_for(email: str) -> str:
    d = {
        "email": "".join(ch for ch in email if ch not in ["&", "="]),
        "uid": "10",
        "role": "user",
    }
    return "&".join(f"{k}={v}" for k, v in d.items())


def enc_profile(email: str) -> bytes:
    return encrypt_aes_ecb(bytes(profile_for(email), encoding="utf-8"), KEY)


def dec_profile(ct: bytes) -> dict[str, str]:
    return kv_parse(pkcs7_unpad(decrypt_aes_ecb(ct, KEY)).decode("utf-8"))


def forge_admin_ct() -> bytes:
    admin_block = enc_profile("a" * 10 + pkcs7_pad(b"admin").decode("utf-8"))[16:32]
    up_to_admin_block = enc_profile("maya@snarg.io")[
        :32
    ]  # important that email=maya@snarg.io&uid=10&role= is aligned with block
    return up_to_admin_block + admin_block


if __name__ == "__main__":
    assert kv_parse("foo=bar&baz=qux&zap=zazzle") == {
        "foo": "bar",
        "baz": "qux",
        "zap": "zazzle",
    }
    assert profile_for("foo@bar.com") == "email=foo@bar.com&uid=10&role=user"
    assert dec_profile(enc_profile("foo@bar.com")) == {
        "email": "foo@bar.com",
        "uid": "10",
        "role": "user",
    }

    print(dec_profile(forge_admin_ct()))
