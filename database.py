from typing import List, Dict

from sqlalchemy import *

import secrets

CONNECTION = f"postgresql://{secrets.DB_USER}:{secrets.DB_PASS}@{secrets.DB_HOST}/{secrets.DB_NAME}"
DISHES_TABLE = "dishes"


def create_db_connection(conn_string: str):
    try:
        return create_engine(conn_string)
    except Exception as e:
        raise ValueError(f'Could not connect {e}')


def create_dishes_table(en) -> Table:
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

    with en.begin() as conn:
        dish_table.create(conn)
    return dish_table


def insert_dishes_to_table(en, db_table: Table, menu: List) -> None:
    with en.begin() as conn:
        conn.execute(db_table.insert(), menu)


def dish_table_exists(en) -> bool:
    inspector = inspect(en)
    return inspector.has_table(DISHES_TABLE)


def dish_table_empty(en) -> bool:
    with en.connect() as conn:
        res = conn.execute(text(f"select * from {DISHES_TABLE}"))
        if res.fetchone() is None:
            return True
        return False


def insert_data_to_db(connection: str, dishes_data: List[Dict]) -> None:
    en = create_db_connection(connection)

    if dish_table_exists(en):
        if not dish_table_empty(en):
            return

    dish_table = create_dishes_table(en)
    insert_dishes_to_table(en, dish_table, dishes_data)


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