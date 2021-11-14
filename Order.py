from typing import List, Optional
from pydantic import BaseModel
import menu_provider


class Order(BaseModel):
    drinks: Optional[List[str]] = []
    desserts: Optional[List[str]] = []
    pizzas: Optional[List[str]] = []

    def check_if_empty(self):
        if not self.drinks and not self.desserts and not self.pizzas:
            return True
        return False

    def calc_price(self) -> int:
        total_price: int = 0
        menu = menu_provider.get_menu()
        products_list = [(self.drinks, menu['drinks_menu']), (self.desserts, menu['desserts_menu']),
                         (self.pizzas, menu['pizzas_menu'])]

        for _tuple in products_list:
            order_products, menu_products = _tuple[0], _tuple[1]
            if order_products:
                for product_id in order_products:
                    if menu_products.get(product_id):
                        try:
                            total_price += menu_products.get(product_id)['price']  # fix price name into global var?
                        except Exception as e:
                            # Raise error instead of returning string while saying you return int.
                            raise f"{e} Product ID: {product_id} doesn't exist!"

        return total_price

    def __repr__(self) -> str:
        if self.check_if_empty():
            return "Empty Order"

        return f'Pizzas ids: {self.pizzas}, Desserts ids: {self.desserts}, Drinks ids: {self.drinks}'

# Tests

# a = Order(drinks=[], desserts=[], pizzas=["2055830"])
# print(a)
# print(a.__repr__())
# print(a.calc_price())

# b = Order()
# print(b.__repr__())
# print(b.calc_price())
