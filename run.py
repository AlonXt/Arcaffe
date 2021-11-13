from get_data_from_10bis import main
import datetime, uvicorn
#  uvicorn api:app --reload

def run():
    main()
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")


# def refresh_menu_data(START_DATE:datetime.date):
#     today = datetime.date.today()
#     if today > START_DATE:
#         main()

if __name__ == '__main__':
    # START_DATE = datetime.date(2021, 11, 13)
    # today = datetime.date.today()

    try:
        run()
    except Exception as e:
        print(e)