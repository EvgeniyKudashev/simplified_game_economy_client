from validation import validate_login, validate_number
from terminal_interface import TerminalLogger

import urllib3
import json

http = urllib3.PoolManager()


class UserInterface:

    def __init__(self):
        self.username = ""

    def login(self):
        TerminalLogger.enter_login()
        self.username = input()
        while not validate_login(self.username):
            TerminalLogger.invalid_login()
            self.username = input()

        url = f"http://127.0.0.1:8000/user/{self.username}"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        inventory = json.loads(r.data.decode('utf-8'))
        TerminalLogger.user_inventory(self.username, inventory)

    def buy_item(self):
        TerminalLogger.buy()

        url = f"http://127.0.0.1:8000/all_game_items"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        items = json.loads(r.data.decode('utf-8'))
        TerminalLogger.print_all_items(items)

        number = input()
        while not validate_number(number, len(items)):
            TerminalLogger.wrong_number(number)
            number = input()

        url = f"http://127.0.0.1:8000/user/{self.username}/buy/{number}"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        result = json.loads(r.data.decode('utf-8'))

        if result:
            TerminalLogger.successful_purchase(items[int(number) - 1][1])
        else:
            TerminalLogger.unsuccessful_purchase(items[int(number) - 1][1])

    def sell_item(self):
        url = f"http://127.0.0.1:8000/user/{self.username}/inventory"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        inventory = json.loads(r.data.decode('utf-8'))
        if len(inventory) == 0:
            TerminalLogger.empty_inventory()
            return
        TerminalLogger.sell()
        TerminalLogger.inventory(inventory)

        number = input()
        while not validate_number(number, len(inventory)):
            TerminalLogger.wrong_number(number)
            number = input()

        item_name = inventory[int(number) - 1][0]

        url = f"http://127.0.0.1:8000/user/{self.username}/sell/{item_name}"
        http.request("GET", url, headers={"Content-Type": "application/json"})

        TerminalLogger.item_sold(item_name)

    def balance(self):
        url = f"http://127.0.0.1:8000/user/{self.username}/balance"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        balance = json.loads(r.data.decode('utf-8'))
        TerminalLogger.balance(balance)

    @staticmethod
    def all_game_items():
        url = f"http://127.0.0.1:8000/all_game_items"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        items = json.loads(r.data.decode('utf-8'))
        TerminalLogger.print_all_items(items)

    def my_items(self):
        url = f"http://127.0.0.1:8000/user/{self.username}/inventory"
        r = http.request("GET", url, headers={"Content-Type": "application/json"})
        inventory = json.loads(r.data.decode('utf-8'))

        if len(inventory) == 0:
            TerminalLogger.empty_inventory()
        else:
            TerminalLogger.inventory(inventory)

    @staticmethod
    def close_session():
        TerminalLogger.good_bye()

    def log_out(self):
        TerminalLogger.logged_out()
        self.login()
