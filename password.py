import hashlib


class Password():
    """docstring for Password"""
    def __init__(self, plain_text):
        self.__plain_text = plain_text
        sha1 = hashlib.new("sha1")
        sha1.update(self.__plain_text.encode("utf-8"))

        self.__encrypted = sha1.hexdigest()

    def to_sha1(self):
        return self.__encrypted

    def __str__(self):
        return self.__encrypted
