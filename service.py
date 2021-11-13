import json

def get_menu():
    with open("menu.json") as menu_file:
        data = json.load(menu_file)
    return data 