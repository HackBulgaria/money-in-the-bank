class Client():
    def __init__(self, id, username, balance):
        self.__username = username
        self.__balance = balance
        self.__id = id

    def get_username(self):
        return self.__username

    def get_balance(self):
        return self.__balance

    def get_id(self):
        return self.__id
