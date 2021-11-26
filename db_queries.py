from sqlalchemy import *
from database import CONNECTION

# create engine. should be global
engine = create_engine(CONNECTION)
print(type(engine))

# create connection
connection = engine.connect()

# check if dish table exists
inspector = inspect(engine)
print(inspector.has_table("dishes"))

# check if there are any records in the dishes table
result = connection.execute(text("select * from dishes"))
print(result.fetchone())
print(result.fetchall())

# print all rows of the dishes table (result objects can be iterated)
result = connection.execute(text("select * from dishes"))
for row in result:
    print(row)
    break



