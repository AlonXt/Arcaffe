import requests, json

from menu_provider import MENU_JSON, PRICE_KEY

DISH_CATEGORIES = ["pizza", "drink", "dessert"]


def get_html_content(url: str) -> str:
    html_response = requests.get(url)
    if html_response.status_code != 200:
        return "Bad html_response"

    content = json.loads(html_response.content)
    return content


def create_product(dish_dict: dict):
    return {"name": dish_dict['dishName'], PRICE_KEY: int(dish_dict['dishPrice']), "desc": dish_dict['dishDescription']}


def find_wanted_dish_list_index(menu_content: json, dish_name: str) -> int:
    """ The func gets the dish name in lower case an gets the index of the dish from the original menu json"""
    categories_list = menu_content['categoriesList']
    for index, cat_dict in enumerate(categories_list):
        if dish_name in cat_dict['categoryName'].lower():
            return index


def create_menu_dict(index: int, menu_content: json) -> dict:
    product_menu_list = menu_content['categoriesList'][index]['dishList']
    product_menu = {item['dishId']: create_product(item) for item in product_menu_list}
    return product_menu


def create_json(content: dict):
    with open(MENU_JSON, mode='w') as menu_file:
        json.dump(content, menu_file, ensure_ascii=False)


def create_menu_json_from_web():
    # get all the html content - the Arcaffe's menu JSON
    menu_api = "https://tenbis-static.azureedge.net/restaurant-menu/19156_en"
    try:
        menu_content = get_html_content(menu_api)
    except Exception as e:
        print(f"{e} Error happened while getting the Arcaffe menu from the web")

    # Create the wanted menus for the task
    final_menu = {}
    for dish in DISH_CATEGORIES:
        dish_index = find_wanted_dish_list_index(menu_content, dish)
        final_menu = {**final_menu, **create_menu_dict(dish_index, menu_content)}

    create_json(final_menu)


if __name__ == "__main__":
    create_menu_json_from_web()
