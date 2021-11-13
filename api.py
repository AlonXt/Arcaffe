from os import stat
from fastapi import FastAPI, Path, Query, HTTPException
from Order import Order
import service

app = FastAPI()

@app.get("/")
def home():
    return {"Data": "Hello, This is Alon's Arcaffe Fast API !"}

@app.get("/menu")
def data():
    return service.get_menu()

@app.get("/drinks")
def get_drinks():
    menu = service.get_menu()
    if menu['drinks_menu'] != None:
        return menu['drinks_menu']
    raise HTTPException(status_code=404, detail="No drinks")

@app.get("/drink/{item_id}")
def get_item(item_id:str = Path(None,description= "The ID of the drink you would like to view")):
    menu = service.get_menu()
    if menu['drinks_menu'].get(item_id) != None:
        return menu['drinks_menu'][item_id]
    raise HTTPException(status_code=404, detail="Drink ID not found")

@app.get("/pizzas")
def get_pizzas():
    menu = service.get_menu()
    if menu['pizzas_menu'] != None:
        return menu['pizzas_menu']
    raise HTTPException(status_code=404, detail="No pizzas")

@app.get("/pizza/{item_id}")
def get_item(item_id:str = Path(None,description= "The ID of the pizza you would like to view")):
    menu = service.get_menu()
    if menu['pizzas_menu'].get(item_id) != None:
        return menu['pizzas_menu'][item_id]
    raise HTTPException(status_code=404, detail="pizza ID not found")

@app.get("/desserts")
def get_desserts():
    menu = service.get_menu()
    if menu['desserts_menu'] != None:
        return menu['desserts_menu']
    raise HTTPException(status_code=404, detail="No desserts") 

@app.get("/dessert/{item_id}")
def get_item(item_id:str = Path(None,description= "The ID of the dessert you would like to view")):
    menu = service.get_menu()
    if menu['desserts_menu'].get(item_id) != None:
        return menu['desserts_menu'][item_id]
    raise HTTPException(status_code=404, detail="dessert ID not found")

@app.post("/order")
def create_order(order: Order):
    if order.check_if_empty():
        raise HTTPException(status_code=400, detail="Bad Request: Order is empty")
    order_total_price = order.calc_price()
    return {"Order_price":order_total_price}
