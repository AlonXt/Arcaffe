import secrets
import uvicorn
from dishes_repo import DishesRepository, create_db_engine
from scrape import scrape

CONNECTION = f"postgresql://{secrets.DB_USER}:{secrets.DB_PASS}@{secrets.DB_HOST}/{secrets.DB_NAME}"


# Manually run the app: "uvicorn api:app --reload"
def run():
    db_menu = scrape()

    # Uncomment the next lines for db app (You should setup the db first via docker)
    engine = create_db_engine(CONNECTION)
    dishes_repo = DishesRepository(engine=engine)
    dishes_repo.initial_data_insert_to_db(db_menu)
    uvicorn.run("db_api:db_app", host="127.0.0.1", port=8000, log_level="info")

    # Uncomment the next line for JSON app
    # uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
