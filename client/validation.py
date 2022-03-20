def validate_login(login: str):
    if len(login.split()) != 1:
        return False
    if "_" not in login and not login.isalnum():
        return False
    if login[0].isdigit():
        return False
    if login[0] == "_":
        return False
    if "/" in login:
        return False
    return True


def validate_number(number: str, limit: int):
    if not number.isdigit():
        return False
    if int(number) not in range(1, limit + 1):
        return False
    return True
