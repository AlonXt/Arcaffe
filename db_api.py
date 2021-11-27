from fastapi import FastAPI, Path, HTTPException
from sqlalchemy import *
from order_class import Order
from dishes_repo import DishesRepository, create_db_engine
from run import CONNECTION

ENGINE = create_db_engine(CONNECTION)
DISH_REPO = DishesRepository(ENGINE)
db_app = FastAPI()


@db_app.get("/")
def home():
    return {"Data": "Hello, This is Alon's Arcaffe webapp built using FastAPI & Postgress Database!"}


@db_app.get("/menu")
def data():
    try:
        return DISH_REPO.get_menu()
    except:
        raise HTTPException(status_code=404, detail="Menu not found")


@db_app.get("/drinks")
def get_drinks():
    try:
        return DISH_REPO.get_category("Drinks")
    except:
        raise HTTPException(status_code=404, detail="No drinks")


@db_app.get("/drink/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the drink you would like to view")):
    try:
        return DISH_REPO.get_category_item("Desserts", item_id)
    except:
        raise HTTPException(status_code=404, detail="Drink ID not found")


@db_app.get("/pizzas")
def get_pizzas():
    try:
        return DISH_REPO.get_category("Pizzas")
    except:
        raise HTTPException(status_code=404, detail="No Pizzas")


@db_app.get("/pizza/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the pizza you would like to view")):
    try:
        return DISH_REPO.get_category_item("Pizzas", item_id)
    except:
        raise HTTPException(status_code=404, detail="Pizza ID not found")


@db_app.get("/desserts")
def get_desserts():
    try:
        return DISH_REPO.get_category("Desserts")
    except:
        raise HTTPException(status_code=404, detail="No Desserts")


@db_app.get("/dessert/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the dessert you would like to view")):
    try:
        return DISH_REPO.get_category_item("Desserts", item_id)
    except:
        raise HTTPException(status_code=404, detail="Dessert ID not found")


@db_app.post("/order")
def create_order(order: Order):
    if order.check_if_empty():
        raise HTTPException(status_code=400, detail="Bad Request: Order is empty")
    try:
        return DISH_REPO.calc_order_price(order)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))
