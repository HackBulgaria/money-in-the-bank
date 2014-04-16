class Client():
    def __init__(self, id, username, email, balance):
        self.__id = id
        self.__username = username
        self.__email = email
        self.__balance = balance

    def get_username(self):
        return self.__username

    def get_balance(self):
        return self.__balance

    def get_id(self):
        return self.__id

    def get_email(self):
        return self.__email
