from typing import Iterable


def zz(b: Iterable[str]) -> bool:
    "a" in b
    print(" ".join(b))


zz(["b" for i in range(10)])
zz(("b" for i in range(10)))
