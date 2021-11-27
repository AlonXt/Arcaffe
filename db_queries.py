from sqlalchemy import *

from run import CONNECTION
DISHES_TABLE = "dishes"
# create engine. should be global
engine = create_engine(CONNECTION)
print(type(engine))

# create connection
connection = engine.connect()

# check if dish table exists
inspector = inspect(engine)
print(inspector.has_table("dishes"))

# check if there are any records in the dishes table
result = connection.execute(text("select * from dishes"))
#print(result.fetchone())
print(type(result.fetchall()))

# # print all rows of the dishes table (result objects can be iterated)
# result = connection.execute(text("select * from dishes"))
# for row in result:
#     print(row)


# ----------- CALC PRICE -----------
# with engine.connect() as conn:
#     stmt = text(f"select price, dish_id from {DISHES_TABLE} where dish_id IN :order_ids")
#     res = conn.execute(stmt, {"order_ids": (2055844,2055837,2055844)})
#     rows = res.fetchall()
#     print(rows)#[0]._mapping["price"])
#
# order_price = 0
# for item_id in (2055844, 2055837,2055844):
#     for item_data in rows:
#         if item_data._mapping["dish_id"] == item_id:
#             order_price += item_data._mapping["price"]
# print(order_price)



