from typing import Optional, List

from pydantic import BaseModel

import menu_provider


class Order(BaseModel):
    dishes: Optional[List[str]] = []

    def check_if_empty(self) -> bool:
        return not any(self.dishes)

    def calc_price(self) -> int:
        menu = menu_provider.get_menu()
        return sum(map(menu.get_dish_price, self.dishes))

    def __repr__(self) -> str:
        if self.check_if_empty():
            return "Empty Order"

        return f'Dish ids: {self.dishes}'


# Tests
# if __name__ == "__main__":
    # a = Order(dishes=["2055830","2055830"])
    # print(a.__repr__())
    # print(a.calc_price())

    # b = Order()
    # print(b.__repr__())
    # print(b.calc_price())

    # c = Order(dishes=["11"])
    # print(c.__repr__())
    # print(c.calc_price())
