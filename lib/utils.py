from base64 import b64decode as b64d, b64encode as b64e
from itertools import product

TRASH_CHARS = '!"#$%&\'()/?@[\\]^{}\t\n\r\x0b\x0c'
# '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'


class HDUtils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def clear_fname(fname: str) -> str:
        for char in TRASH_CHARS:
            fname.replace(char, "")
        return fname
    
    @staticmethod
    def decode_url(url: str, get_new: callable, separator: str = "//_//") -> list[str]:
        while True:
            try:
                trash_codes_set: list[str] = []
                for i in range(2, 4):
                    for chars in product(["@", "#", "!", "^", "$"], repeat=i):
                        trash_codes_set.append(b64e(''.join(chars).encode("utf-8")))

                trash_string = ''.join(url.replace("#h", "").split(separator))
                for i in trash_codes_set:
                    trash_string = trash_string.replace(i.decode("utf-8"), '')

                return b64d(trash_string + "==").decode("utf-8")
            except Exception as e:
                url = get_new()["url"] # getting new url, bcz that one cant be decoded
                print(f"bruh {e}")
            else:
                break
