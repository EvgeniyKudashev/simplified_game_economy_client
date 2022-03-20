from enum import Enum
import colorama


class TextColors:
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    end = '\033[0m'


class Actions(Enum):
    BALANCE = 1
    ALL_GAME_ITEMS = 2
    MY_ITEMS = 3
    BUY_ITEMS = 4
    SELL_ITEMS = 5
    LOG_OUT = 6
    CLOSE_SESSION = 7


colorama.init()


class TerminalLogger:
    @staticmethod
    def request_action():
        TerminalLogger.list_of_actions()

        try:
            action_number = int(input())
        except ValueError:
            TerminalLogger.value_error()
            return None

        if action_number not in range(1, len(Actions) + 1):
            TerminalLogger.wrong_number(action_number)
            return None

        return action_number

    @staticmethod
    def list_of_actions():
        print(TextColors.blue + "\nHere is a list of actions you can do:" + TextColors.end)
        print("""1. My balance
2. All available items in games
3. My items
4. Buy items
5. Sell items
6. Log out
7. End session""")
        print(TextColors.blue + "\nPlease choose an action" + TextColors.end)

    @staticmethod
    def enter_login():
        print(TextColors.blue + "\nPlease enter your login" + TextColors.end)

    @staticmethod
    def invalid_login():
        print(TextColors.red + "\nInvalid login format. Please try again" + TextColors.end)

    @staticmethod
    def user_inventory(username, inventory: list):
        print(TextColors.green + f"\nHi {username}! Now you have:" + TextColors.end)
        print(inventory.pop(), "credits")
        for element in inventory:
            print(element[0] + " x" + str(element[1]))

    @staticmethod
    def logged_out():
        print(TextColors.green + "\nYou logged out" + TextColors.end)

    @staticmethod
    def value_error():
        print(TextColors.red + "\nThis is not a number. Please enter a number from list" + TextColors.end)

    @staticmethod
    def wrong_number(action_number):
        print(
            TextColors.red + f"\nThere is no number {action_number}. Please enter a number from list" + TextColors.end)

    @staticmethod
    def buy():
        print(TextColors.blue + "\nWhat do you want to buy? Please enter a number" + TextColors.end)

    @staticmethod
    def print_all_items(items):
        print("\nAll available items in game:")
        for item in items:
            print(str(item[0]) + ". " + item[1] + " for " + str(item[2]) + " credits")

    @staticmethod
    def successful_purchase(item_name):
        print(TextColors.green + f"\nYou successfully purchased the {item_name}" + TextColors.end)

    @staticmethod
    def unsuccessful_purchase(item_name):
        print(TextColors.red + f"\nYou don't have enough credits for {item_name}" + TextColors.end)

    @staticmethod
    def item_sold(item_name):
        print(TextColors.green + f"\nYou successfully sold the {item_name}" + TextColors.end)

    @staticmethod
    def balance(balance):
        print("\nYour balance is " + TextColors.green + str(balance) + TextColors.end + " credits")

    @staticmethod
    def sell():
        print(TextColors.blue + "\nWhat do you want to sell? Please enter a number" + TextColors.end)

    @staticmethod
    def inventory(inventory):
        for index, element in enumerate(inventory):
            print(str(index + 1) + ". " + element[0] + " x" + str(element[1]), sep="")

    @staticmethod
    def empty_inventory():
        print(TextColors.red + "\nYour inventory is empty" + TextColors.end)

    @staticmethod
    def good_bye():
        print(TextColors.blue + "\nGood bye!" + TextColors.end)
