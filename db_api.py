from fastapi import FastAPI, Path, HTTPException
from sqlalchemy import *
from order_class import Order
from database import CONNECTION, DISHES_TABLE

ENGINE = create_engine(CONNECTION)
db_app = FastAPI()


@db_app.get("/")
def home():
    return {"Data": "Hello, This is Alon's Arcaffe webapp built using FastAPI & Postgress Database!"}


@db_app.get("/menu")
def data():
    with ENGINE.connect() as conn:
        res = conn.execute(text(f"select * from {DISHES_TABLE}"))
        return res.fetchall()


@db_app.get("/drinks")
def get_drinks():
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where category=:category")
            res = conn.execute(stmt, {"category": "Drinks"})
            return res.fetchall()
    except:
        raise HTTPException(status_code=404, detail="No drinks")


@db_app.get("/drink/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the drink you would like to view")):
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where dish_id=:dish_id and category=:category")
            res = conn.execute(stmt, {"dish_id": item_id, "category": "Drinks"})
            return res.fetchall()
    except:
        raise HTTPException(status_code=404, detail="Drink ID not found")


@db_app.get("/pizzas")
def get_pizzas():
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where category=:category")
            res = conn.execute(stmt, {"category": "Pizzas"})
            return res.fetchall()
    except:
        raise HTTPException(status_code=404, detail="No Pizzas")


@db_app.get("/pizza/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the pizza you would like to view")):
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where dish_id=:dish_id and category=:category")
            res = conn.execute(stmt, {"dish_id": item_id, "category": "Pizzas"})
            return res.fetchall()
    except:
        raise HTTPException(status_code=404, detail="Pizza ID not found")


@db_app.get("/desserts")
def get_desserts():
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where category=:category")
            res = conn.execute(stmt, {"category": "Desserts"})
            return res.fetchall()
    except:
        raise HTTPException(status_code=404, detail="No Desserts")


@db_app.get("/dessert/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the dessert you would like to view")):
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select * from {DISHES_TABLE} where dish_id=:dish_id and category=:category")
            res = conn.execute(stmt, {"dish_id": item_id, "category": "Desserts"})
            return res.fetchall()
    except:
        raise HTTPException(status_code=404, detail="Dessert ID not found")


@db_app.post("/order")
def create_order(order: Order):
    if order.check_if_empty():
        raise HTTPException(status_code=400, detail="Bad Request: Order is empty")
    try:
        with ENGINE.connect() as conn:
            stmt = text(f"select sum(price) from {DISHES_TABLE} where dish_id IN :order_ids")
            res = conn.execute(stmt, {"order_ids": tuple(order.dishes)})
            return res.fetchall()
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))
