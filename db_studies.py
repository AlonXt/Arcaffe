from sqlalchemy import *
from run import CONNECTION

# ---- STUDIES ----

# create engine. should be global
engine = create_engine(CONNECTION)

# create connection
connection = engine.connect()
print(connection)
print(connection.connection.connection)

# sql query
stmt = text("select emp_name from employees where emp_id=:emp_id")
result = connection.execute(stmt, {"emp_id": 2})

# result object is similar to a cursor, has feature methods like fetchone() and fetchall()
row = result.fetchone()
print(row.keys())
print(row._mapping["emp_name"])  # in the future it will be like this
print(row[1])
print(row.emp_name)

# result objects can be iterated
result = connection.execute(text("select * from employees"))
for row in result:
    print(row)

# fancy method for getting a whole column as a list
result.scalars("emp_name").all()

# connection should be closed. This releases the DBAPI connection to the connection pool for a faster re-use.
# This may or may not actually close the DBAPI connection.
connection.close()

# however it is preferred to use context managers to manage the connect/ release process
with engine.connect() as connection:
    connection.execute(text("select * from employees"))

# transactions, commiting and auto commit
connection = engine.connect()
connection.execute(text("insert into employee_of_the_month (emp_name) values (:emp_name)"), {"emp_name": "spongebob"})

with engine.begin() as connection:
    connection.execute(text())
    # commits transaction, releases connection back to pool
    # rolls back if there is an exception before re-throwing

with engine.connect() as connection:
    with connection.begin() as trans:
        connection.execute(
            text("update employee_of_the_month set emp_name = :emp_name"),
            {"emp_name": "squidward"}
        )
        # commits transaction, or rollback if exception
    # closes connection
    # it is possible to do several connection.begin() in one connection


