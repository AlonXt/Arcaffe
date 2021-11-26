import uvicorn
from database import insert_data_to_db, CONNECTION
from scrape import scrape


# Manually run the app: "uvicorn api:app --reload"
def run():
    db_menu = scrape()
    insert_data_to_db(CONNECTION, db_menu)

    # Uncomment the next line for db app
    # uvicorn.run("db_api:db_app", host="127.0.0.1", port=8000, log_level="info")

    # Uncomment the next line for JSON app
    # uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
