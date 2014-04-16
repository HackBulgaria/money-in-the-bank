from sql_manager import SqlManager, BlockedUserException
from getpass import getpass
from password import Password, PasswordValidator, PasswordNotStrongException
from client import Client
from sqlite3 import IntegrityError


class BankProgram():
    def __init__(self):
        self.sql_manager = SqlManager("bank.db")
        self.main_menu()

    def input_pass(self):
        password = getpass("Enter your password: ")
        return Password(password)

    def main_menu(self):
        print("""Welcome to our bank service.
                 You are not logged in.
                 Please register or login""")

        while True:
            command = input("$$$>")

            if command == 'register':
                username = input("Enter your username: ")
                email = input("Enter your email: ")

                while True:
                    password = self.input_pass()
                    validator = PasswordValidator(password,
                                                  Client(1,
                                                         username,
                                                         email,
                                                         0))

                    try:
                        validator.validate_with_exception()
                        break
                    except PasswordNotStrongException as e:
                        print(e)

                try:
                    self.sql_manager.register(username, email, password)
                    print("Registration Successfull")
                except IntegrityError as e:
                    print("Username already registered. Try another!")

            elif command == 'login':
                username = input("Enter your username: ")
                password = self.input_pass()

                try:
                    logged_user = self.sql_manager.login(username, password)
                    if logged_user:
                        self.logged_menu(logged_user)
                    else:
                        print("Login failed")
                except BlockedUserException as e:
                    print(str(e))

            elif command == 'help':
                print("login - for logging in!")
                print("register - for creating new account!")
                print("exit - for closing program!")

            elif command == 'exit':
                break
            else:
                print("Not a valid command")

    def logged_menu(self, logged_user):
        print("Welcome you are logged in as: " + logged_user.get_username())
        while True:
            command = input("Logged>>")

            if command == 'info':
                print("You are: " + logged_user.get_username())
                print("Your id is: " + str(logged_user.get_id()))
                print("Your balance is:" + str(logged_user.get_balance())
                                         + '$')

            elif command == 'changepass':
                new_pass = input("Enter your new password: ")
                self.sql_manager.change_pass(new_pass, logged_user)

            elif command == 'change-message':
                new_message = input("Enter your new message: ")
                self.sql_manager.change_message(new_message, logged_user)

            elif command == 'show-message':
                print(logged_user.get_message())

            elif command == 'help':
                print("info - for showing account info")
                print("changepass - for changing passowrd")
                print("change-message - for changing users message")
                print("show-message - for showing users message")


def main():
    BankProgram()

if __name__ == '__main__':
    main()
