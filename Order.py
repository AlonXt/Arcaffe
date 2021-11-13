from typing import List, Optional
from pydantic import BaseModel
import service

class Order(BaseModel):
    drinks: Optional[List[str]] = []
    desserts: Optional[List[str]] = []
    pizzas: Optional[List[str]] = []

    def check_if_empty(self):
        if len(self.drinks) == 0 and len(self.desserts) == 0 and len(self.pizzas) == 0:
            return True
        return False

    def calc_price(self) -> int:
        total_price = 0
        menu = service.get_menu()
        products_list = [(self.drinks, menu['drinks_menu']), (self.desserts, menu['desserts_menu']), (self.pizzas, menu['pizzas_menu'])]

        for tuple in products_list:
            order_products, menu_products = tuple[0], tuple[1]
            if len(order_products) != 0:
                for product_id in order_products:
                    if menu_products.get(product_id) != None:
                        total_price += menu_products.get(product_id)['price']
                    else: 
                        return f"Product ID: {product_id} doesn't exist!"

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