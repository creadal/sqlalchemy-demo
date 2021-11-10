from sqlalchemy import *

engine = create_engine('postgresql+psycopg2://postgres:1111@localhost:5432/test')

result = engine.execute(
    "insert into users values (3, 'Jesse');"
    "select * from users"
)

print(result.fetchall())
