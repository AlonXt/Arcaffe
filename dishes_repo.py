from typing import List, Dict
from sqlalchemy import *
from order_class import Order


DISHES_TABLE = "dishes"


def create_db_engine(conn_string: str):
    try:
        return create_engine(conn_string)
    except Exception as e:
        raise ValueError(f'Could not connect because: {e}')


class DishesRepository:
    def __init__(self, engine):
        self.engine = engine

    def create_dishes_table(self) -> Table:
        metadata = MetaData()
        dish_table = Table(
            DISHES_TABLE,
            metadata,
            Column("dish_id", Integer, primary_key=True),
            Column("dish_name", String(50), nullable=False),
            Column("description", String(255)),
            Column("category", String(255), nullable=False),
            Column("price", Float, nullable=False),
        )

        with self.engine.begin() as conn:
            dish_table.create(conn)
        return dish_table

    def insert_dishes_to_table(self, db_table: Table, menu: List) -> None:
        with self.engine.begin() as conn:
            conn.execute(db_table.insert(), menu)

    def dish_table_exists(self) -> bool:
        inspector = inspect(self.engine)
        return inspector.has_table(DISHES_TABLE)

    def dish_table_empty(self) -> bool:
        with self.engine.connect() as conn:
            res = conn.execute(text(f"select * from {DISHES_TABLE}"))
            if res.fetchone() is None:
                return True
            return False

    def initial_data_insert_to_db(self, dishes_data: List[Dict]) -> None:
        if self.dish_table_exists():
            if not self.dish_table_empty():
                return

        dish_table = self.create_dishes_table()
        self.insert_dishes_to_table(dish_table, dishes_data)

    def get_menu(self):
        with self.engine.connect() as conn:
            res = conn.execute(text(f"select * from {DISHES_TABLE}"))
            return res.fetchall()

    def get_category(self, category: str) -> List:
        with self.engine.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where category=:category")
            res = conn.execute(stmt, {"category": category})
            return res.fetchall()

    def get_category_item(self, category: str, item_id):
        with self.engine.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where dish_id=:dish_id and category=:category")
            res = conn.execute(stmt, {"dish_id": item_id, "category": category})
            return res.fetchall()

    def calc_order_price(self, order: Order):
        with self.engine.connect() as conn:
            stmt = text(f"select dish_id,price from {DISHES_TABLE} where dish_id IN :order_ids")
            res = conn.execute(stmt, {"order_ids": tuple(order.dishes)})
            rows = res.fetchall()

        order_price = 0
        for item_id in order.dishes:
            for item_data in rows:
                if item_data._mapping["dish_id"] == int(item_id):
                    order_price += item_data._mapping["price"]
        return order_price



# if __name__ == "__main__":
# ----- Tests A -----
# DICT_LIST = [
#     {"dish_id": 2, "dish_name": "Alon meat2", "description": "Very good and soft meat2",
#      "category": "Special dishes",
#      "price": 102},
#     {"dish_id": 3, "dish_name": 'Alon meat3', "description": "Very good and soft meat3",
#      "category": "Special dishes",
#      "price": 103}]
# engine = create_db_connection(CONNECTION)
# dish_table = create_dishes_table(engine)
# insert_dishes_to_table(dish_table, DICT_LIST)

# ----- Test B -----
# insert_data_to_db(CONNECTION, DICT_LIST)

# ----- REFLECTION CODE -----
# engine = create_db_connection(CONNECTION)
# metadata2 = MetaData()
# with engine.connect() as conn:
#     dishes_reflected = Table("dishes", metadata2, autoload_with=conn)
#     result = conn.execute(text("select * from dishes"))

# print(dishes_reflected.c)
# print(dishes_reflected.primary_key)
# print(select([dishes_reflected]))

# for row in result:
#     print(row)


# ----- INSERT STATEMENT -----
# insert_stmt = dish_table.insert().values(
#     dish_id=1, dish_name='Alon meat', description="Very good and soft meat", category="Special dishes", price=100
# )
# with engine.begin() as conn:
#     conn.execute(insert_stmt)
