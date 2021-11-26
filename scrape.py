import json
import traceback
from typing import List, Dict

import requests

from menu_provider import MENU_JSON, PRICE_KEY

DISH_CATEGORIES = ["pizza", "drink", "dessert"]
MENU_URL = "https://tenbis-static.azureedge.net/restaurant-menu/19156_en"


def _create_product(dish_dict: dict):
    return {"name": dish_dict['dishName'], PRICE_KEY: int(dish_dict['dishPrice']), "desc": dish_dict['dishDescription']}


def _find_wanted_dish_index(menu_content: json, dish_name: str) -> int:
    """ The func gets the dish name in lower case an gets the index of the dish from the original menu json"""
    categories = menu_content['categoriesList']
    for index, cat_dict in enumerate(categories):
        if dish_name in cat_dict['categoryName'].lower():
            return index


def _create_menu(index: int, menu_content: json) -> dict:
    product_menu_list = menu_content['categoriesList'][index]['dishList']
    product_menu = {item['dishId']: _create_product(item) for item in product_menu_list}
    return product_menu


def _create_json(content: dict, json_name: str = MENU_JSON):
    with open(json_name, mode='w') as menu_file:
        json.dump(content, menu_file, ensure_ascii=False)


def _get_html_content(url: str) -> str:
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Request failed: {res.status_code}')
    return json.loads(res.content)


def _create_final_menu(content):
    menu = {}
    for dish in DISH_CATEGORIES:
        dish_index = _find_wanted_dish_index(content, dish)
        menu[f"{dish}s_menu"] = _create_menu(dish_index, content)
    return menu


def _create_db_menu(content):
    menu_categories: List[Dict] = content['categoriesList']
    dishes = []
    for cat in menu_categories:
        if cat['categoryID'] == 0:
            continue
        for dish in cat['dishList']:
            dishes.append(
                {"dish_id": dish['dishId'], "dish_name": dish['dishName'], "description": dish['dishDescription'],
                 "category": cat['categoryName'], "price": dish['dishPrice']})
    return dishes
    # return [{"dish_id": dish.dishId, "dish_name": dish.dishName, "description": dish.dishDescription,
    #          "category": cat.categoryName, "price": dish.dishPrice} for dish in cat['dishList'] for cat in
    #         menu_categories]


def _scrape_unsafe(url):
    print(f'Scraping {url}')
    content = _get_html_content(url)
    _create_json(content, json_name="original_menu.json")
    db_menu = _create_db_menu(content)
    menu = _create_final_menu(content)
    _create_json(menu)
    return db_menu


def scrape(url=MENU_URL):
    try:
        db_menu = _scrape_unsafe(url)
        return db_menu
    except:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Scrape 10bis menu')
    parser.add_argument('--url', type=str,
                        default=MENU_URL,
                        help='Menu URL to scrape')

    args = parser.parse_args()
    sys.exit(scrape(args.url))
