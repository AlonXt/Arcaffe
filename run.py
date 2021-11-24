import uvicorn
from scrape import scrape


#  uvicorn api:app --reload
def run():
    scrape()
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
