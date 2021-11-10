from sqlalchemy import *

engine = create_engine('postgresql+psycopg2://postgres:1111@localhost:5432/test')

metadata = MetaData()
users = Table('users', metadata, autoload=True, autoload_with=engine)

result = engine.execute(users.select())
print(result.fetchall())

items = Table('items', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(16)),
              Column('price', Integer)
             )

metadata.create_all(engine)

insertion = insert(items)
rows = [
    {'id': 2000, 'name': 'sword', 'price': 100},
    {'id': 2001, 'name': 'bow', 'price': 200}
]

engine.execute(insertion, rows)
print(insertion)
