from db import DataBase
from config import items

import os
from fastapi import FastAPI

app = FastAPI()

db_filename = "wargaming.db"
db = DataBase(db_filename)


@app.get("/user/{login}")
def login_user(login: str):
    if not db.user_exists(login):
        db.insert_user_by_login(login)
    db.earn_credits(login)

    user_info = db.get_user_info(login)
    return user_info


@app.get("/user/{login}/balance")
def get_user_balance(login: str):
    balance = db.get_users_balance(login)
    return balance


@app.get("/user/{login}/inventory")
def get_users_inventory(login: str):
    inventory = db.get_users_inventory(login)
    return inventory


@app.get("/all_game_items")
def get_all_game_items():
    items = db.get_all_game_items()
    return items


@app.get("/user/{login}/buy/{item_number}")
def buy_item(login: str, item_number: int):
    user_balance = db.get_users_balance(login)
    item_price = db.get_item_price(items[item_number]["name"])
    if user_balance < item_price:
        return False
    db.buy_item(login, items[item_number]["name"])
    return True


@app.get("/user/{login}/sell/{item_name}")
def sell_item(login: str, item_name: str):
    db.sell_item(login, item_name)
    return True


if __name__ == "__main__":
    os.system('cmd /k "uvicorn main:app --reload"')
