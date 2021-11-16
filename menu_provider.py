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
    def __init__(self, menu_dict: dict) -> None:
        self._id_to_dish = _id_to_dish(menu_dict)

    def get_dish_price(self, dish_id: str) -> int:
        if dish_id not in self._id_to_dish:
            raise KeyError(f"Dish id {dish_id} not found in menu (possible ids: {tuple(self._id_to_dish.keys())}")

        return self._id_to_dish[dish_id][PRICE_KEY]


def get_menu() -> Menu:
    with open(MENU_JSON) as menu_file:
        data = json.load(menu_file)
    return Menu(data)
