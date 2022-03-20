from terminal_interface import Actions, TerminalLogger
from user_interface import UserInterface

user = UserInterface()
user.login()

action = TerminalLogger.request_action()
while action != Actions.CLOSE_SESSION.value:
    if action == Actions.BALANCE.value:
        user.balance()
    elif action == Actions.ALL_GAME_ITEMS.value:
        user.all_game_items()
    elif action == Actions.MY_ITEMS.value:
        user.my_items()
    elif action == Actions.BUY_ITEMS.value:
        user.buy_item()
    elif action == Actions.SELL_ITEMS.value:
        user.sell_item()
    elif action == Actions.LOG_OUT.value:
        user.log_out()
    action = TerminalLogger.request_action()

if action == Actions.CLOSE_SESSION.value:
    user.close_session()
