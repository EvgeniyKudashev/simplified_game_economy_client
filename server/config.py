items = {
    1: {"name": "Destroyer", "price": 1000},
    2: {"name": "Cruiser", "price": 2000},
    3: {"name": "Battleship", "price": 3000},
    4: {"name": "Aircraft_carrier", "price": 4000},
    5: {"name": "Shell", "price": 100},
    6: {"name": "Armor", "price": 250},
    7: {"name": "Cannon", "price": 800},
    8: {"name": "Skin", "price": 10000},
}

all_items = []
for i in items.keys():
    item = [i]
    for j in items[i].values():
        item.append(j)
    all_items.append(tuple(item))

credits_start = 500
credits_end = 1500
