import requests, json

def get_html_content(url:str) -> str:
    html_response = requests.get(url)
    if html_response.status_code != 200:
        return "Bad html_response"

    content = json.loads(html_response.content)
    return content

def create_product(dish_dict:dict):
    return {"name":dish_dict['dishName'],"price":int(dish_dict['dishPrice']), "desc":dish_dict['dishDescription']}

def create_menu_dict(index:int, menu_content:json) -> dict:
    product_menu_list = menu_content['categoriesList'][index]['dishList']
    product_menu = {item['dishId']:create_product(item) for item in product_menu_list}
    return product_menu

def create_json(content:dict):
    with open("menu.json", mode='w') as menu_file:
        json.dump(content, menu_file, ensure_ascii=False)
    
def main():
    # get all the html content - the Arcaffe's menu JSON
    menu_api = "https://tenbis-static.azureedge.net/restaurant-menu/19156_en"
    menu_content = get_html_content(menu_api)
    #Create the wanted menues for the task
    final_menu = {'pizzas_menu':create_menu_dict(3,menu_content),'desserts_menu':create_menu_dict(4,menu_content),'drinks_menu':create_menu_dict(5,menu_content)}
    create_json(final_menu)

    
    




