from fastapi import FastAPI, Path, HTTPException
from order_class import Order
import menu_provider

app = FastAPI()


@app.get("/")
def home():
    return {"Data": "Hello, This is Alon's Arcaffe Fast API !"}


@app.get("/menu")
def data():
    return menu_provider.get_menu()


@app.get("/drinks")
def get_drinks():
    menu = menu_provider.get_menu()
    if menu['drinks_menu']:
        return menu['drinks_menu']
    raise HTTPException(status_code=404, detail="No drinks")


@app.get("/drink/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the drink you would like to view")):
    menu = menu_provider.get_menu()
    if menu['drinks_menu'].get(item_id):
        return menu['drinks_menu'][item_id]
    raise HTTPException(status_code=404, detail="Drink ID not found")


@app.get("/pizzas")
def get_pizzas():
    menu = menu_provider.get_menu()
    if menu['pizzas_menu']:
        return menu['pizzas_menu']
    raise HTTPException(status_code=404, detail="No pizzas")


@app.get("/pizza/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the pizza you would like to view")):
    menu = menu_provider.get_menu()
    if menu['pizzas_menu'].get(item_id):
        return menu['pizzas_menu'][item_id]
    raise HTTPException(status_code=404, detail="pizza ID not found")


@app.get("/desserts")
def get_desserts():
    menu = menu_provider.get_menu()
    if menu['desserts_menu']:
        return menu['desserts_menu']
    raise HTTPException(status_code=404, detail="No desserts")


@app.get("/dessert/{item_id}")
def get_item(item_id: str = Path(None, description="The ID of the dessert you would like to view")):
    menu = menu_provider.get_menu()
    if menu['desserts_menu'].get(item_id):
        return menu['desserts_menu'][item_id]
    raise HTTPException(status_code=404, detail="dessert ID not found")


@app.post("/order")
def create_order(order: Order):
    if order.check_if_empty():
        raise HTTPException(status_code=400, detail="Bad Request: Order is empty")
    order_total_price = order.calc_price()
    return {"Order_price": order_total_price}
