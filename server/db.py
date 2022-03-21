from config import all_items, credits_start, credits_end
import sqlite3
import os
import random


class DataBase:

    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            self.init_db()

    def init_db(self):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("""CREATE TABLE items(
            item_id INT PRIMARY KEY,
            item_name TEXT,
            price INT);
            """)
        sqlite_connection.commit()

        cursor.executemany("INSERT OR IGNORE INTO items VALUES(?, ?, ?);", all_items)
        sqlite_connection.commit()

        cursor.execute("""CREATE TABLE users(
                        username TEXT PRIMARY KEY,
                        credits INT);
                        """)
        sqlite_connection.commit()

        cursor.execute("""CREATE TABLE inventory(
                            username TEXT,
                            item_name TEXT,
                            count INT,
                            PRIMARY KEY (username, item_name));
                            """)
        sqlite_connection.commit()

        cursor.close()
        sqlite_connection.close()

    def insert_user_by_login(self, login):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("INSERT OR IGNORE INTO users VALUES(?, ?);", (login, 0))
        sqlite_connection.commit()

        cursor.close()
        sqlite_connection.close()

    def get_user_info(self, login):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT credits FROM users WHERE username=?", (login,))
        users_credits = cursor.fetchone()[0]

        users_inventory = self.get_users_inventory(login)
        users_inventory.append(users_credits)

        cursor.close()
        sqlite_connection.close()
        return users_inventory

    def earn_credits(self, login):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT credits FROM users WHERE username=?", (login,))
        credits = cursor.fetchone()[0]
        credits += random.randrange(credits_start, credits_end, step=1)

        cursor.execute("UPDATE users SET credits=? WHERE username=?", (credits, login))
        sqlite_connection.commit()

        cursor.close()
        sqlite_connection.close()

    def user_exists(self, login):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (login,))
        user_info = cursor.fetchone()

        cursor.close()
        sqlite_connection.close()
        if user_info is not None:
            return True
        return False

    def get_users_balance(self, login):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT credits FROM users WHERE username=?", (login,))
        balance = cursor.fetchone()[0]

        cursor.close()
        sqlite_connection.close()
        return balance

    def get_item_price(self, item_name: str):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT price FROM items WHERE item_name=?", (item_name,))
        price = cursor.fetchone()[0]

        cursor.close()
        sqlite_connection.close()
        return price

    def buy_item(self, login: str, item_name: str):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        price = self.get_item_price(item_name)

        cursor.execute("SELECT credits FROM users WHERE username=?", (login,))
        money = cursor.fetchone()[0]
        money -= price
        cursor.execute("UPDATE users SET credits=? WHERE username=?", (money, login))
        sqlite_connection.commit()

        new_purchase = (login, item_name, 0)
        cursor.execute("INSERT OR IGNORE INTO inventory VALUES(?, ?, ?);", new_purchase)
        sqlite_connection.commit()

        cursor.execute("SELECT count FROM inventory WHERE username=? AND item_name=?", (login, item_name))
        count = cursor.fetchone()[0]
        count += 1
        cursor.execute("UPDATE inventory SET count=? WHERE username=? AND item_name=?", (count, login, item_name))
        sqlite_connection.commit()

        cursor.close()
        sqlite_connection.close()

    def sell_item(self, login: str, item_name: str):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        price = self.get_item_price(item_name)

        cursor.execute("SELECT credits FROM users WHERE username=?", (login,))
        money = cursor.fetchone()[0]
        money += price
        cursor.execute("UPDATE users SET credits=? WHERE username=?", (money, login))
        sqlite_connection.commit()

        cursor.execute("SELECT count FROM inventory WHERE username=? AND item_name=?", (login, item_name))
        count = cursor.fetchone()[0]
        count -= 1
        if count > 0:
            cursor.execute("UPDATE inventory SET count=? WHERE username=? AND item_name=?",
                           (count, login, item_name))
        else:
            cursor.execute("DELETE FROM inventory WHERE username=? AND item_name=?", (login, item_name))
        sqlite_connection.commit()

        cursor.close()
        sqlite_connection.close()

    def get_users_inventory(self, login: str):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT item_name, count FROM inventory WHERE username=?", (login,))
        users_inventory = cursor.fetchall()

        cursor.close()
        sqlite_connection.close()
        return users_inventory

    def get_all_game_items(self):
        sqlite_connection = sqlite3.connect(self.filename)
        cursor = sqlite_connection.cursor()

        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()

        cursor.close()
        sqlite_connection.close()
        return items
