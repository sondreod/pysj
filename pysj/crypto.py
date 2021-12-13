import hashlib
from typing import Literal
import uuid as _uuid

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ" "abcdefghijkmnpqrstuvwxyz" "23456789"


def _hash(plaintext: str, algorithm="sha256") -> str:
    """Calculate hashdigest of plaintext using any algorithm in `hashlib.algorithms_guaranteed`"""

    if algorithm not in hashlib.algorithms_guaranteed:
        raise NotImplementedError(f"Hash algorithm {algorithm} is not implemented.")

    hash_fn = getattr(hashlib, algorithm)
    return hash_fn(plaintext.encode()).hexdigest()


def sha256(plaintext: str) -> str:
    """Returns the hexdigest representation of the sha256 hash from the plaintext input"""
    return _hash(plaintext, "sha256")


def sha1(plaintext: str) -> str:
    """Returns the hexdigest representation of the sha1 hash from the plaintext input"""
    return _hash(plaintext, "sha1")


def md5(plaintext: str) -> str:
    """Returns the hexdigest representation of the md5 hash from the plaintext input"""
    return _hash(plaintext, "md5")


def uuid(type: Literal["alpha", "int"] = None, length: int = None) -> str:
    if length:
        raise NotImplementedError("Not implemented yet")
    if type == "alpha":
        alphabet: str = ALPHABET
        number: int = _uuid.uuid4().int
        output: str = ""
        length: int = len(alphabet)
        while number:
            number, digit = divmod(number, length)
            output += alphabet[digit]
        return output[::-1]
    elif type == "int":
        return _uuid.uuid4().int
    else:
        return str(_uuid.uuid4())
