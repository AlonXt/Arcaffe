from get_data_from_10bis import create_menu_json_from_web
import uvicorn


#  uvicorn api:app --reload

def run():
    create_menu_json_from_web()
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
