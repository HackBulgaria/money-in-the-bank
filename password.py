import hashlib


class PasswordNotStrongException(Exception):
    pass


MESSAGE = """Password should be:
             * >= 8 chars
             * At least 1 capital letter
             * At least 1 number
             * At least 1 special symbol
             * username is not in the password
          """


class PasswordValidator():
    def __init__(self, password_obj, user):
        self.password = password_obj
        self.user = user

    def validate(self):
        validators = [self._more_than_n_symbols,
                      self._one_capital,
                      self._one_number,
                      self._one_special,
                      self._name_in_password]

        result = map(lambda f: f(), validators)
        return all(result)

    def validate_with_exception(self):
        if not self.validate():
            raise PasswordNotStrongException(MESSAGE)

    def _more_than_n_symbols(self, n=8):
        plain_text = self.password.get_plain()
        return len(plain_text) >= n

    def _one_capital(self):
        result = filter(lambda c: c.isupper(), self.password.get_plain())

        return len(list(result)) > 0

    def _one_number(self):
        result = filter(lambda c: c.isdigit(), self.password.get_plain())
        return len(list(result)) > 0

    def _one_special(self):
        special_characters = "` ~ ! @ # $ % ^ & * ( ) _ - \
                                 + = { } [ ] \ | : ; \" \' < > \
                                 , . ? "
        special_characters = special_characters.split()
        # should be with filter

        for c in self.password.get_plain():
            if c in special_characters:
                return True

        return False

    def _name_in_password(self):
        username = self.user.get_username()
        plain = self.password.get_plain()

        return username not in plain


class Password():
    """docstring for Password"""
    def __init__(self, plain_text):
        self.__plain_text = plain_text

        sha1 = hashlib.new("sha1")
        sha1.update(self.__plain_text.encode("utf-8"))
        self.__encrypted = sha1.hexdigest()

    def get_plain(self):
        return self.__plain_text

    def to_sha1(self):
        return self.__encrypted

    def __str__(self):
        return self.__encrypted
