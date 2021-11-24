import json

MENU_JSON = "menu.json"
PRICE_KEY = "price"


def _id_to_dish(dish_menu: dict) -> dict:
    return {
        dish_id: dish
        for _, id_to_dish in dish_menu.items()
        for dish_id, dish in id_to_dish.items()
    }


class Menu:
    menu: dict
    flat_menu: dict

    def __init__(self, menu_dict: dict) -> None:
        self.menu = menu_dict
        self.flat_menu = _id_to_dish(menu_dict)

    def get_dish_price(self, dish_id: str) -> int:
        if dish_id not in self.flat_menu:
            raise KeyError(f"Dish id {dish_id} not found in menu (possible ids: {tuple(self.flat_menu.keys())}")

        return self.flat_menu[dish_id][PRICE_KEY]


def get_menu() -> Menu:
    with open(MENU_JSON) as menu_file:
        data = json.load(menu_file)
    return Menu(data)
