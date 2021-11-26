# Arcaffe

###There are two options for running this project:
* With or without Postgress database

### To run it with the DB please follow the next steps:
1. install docker on your computer
2. create a Postgres-db using terminal:
   * docker run --name postgres-db -e POSTGRES_PASSWORD=docker -p 5432:5432 -d postgres
3. create and activate venv
4. pip install -r requirements.txt
5. go to run.py and uncomment the relevant line
5. python3 run.py
6. enter http://127.0.0.1:8000/docs and enjoy :)

### To run it without the DB follow the above steps disregarding the first two steps!