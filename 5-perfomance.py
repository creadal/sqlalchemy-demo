import psycopg2
from sqlalchemy import *
from time import process_time

engine = create_engine('postgresql+psycopg2://postgres:1111@localhost:5432/test')
metadata = MetaData()

users = Table('users', metadata, autoload=True, autoload_with=engine)

connection = psycopg2.connect(dbname='test', user='postgres', password='1111')
cur = connection.cursor()

begin = process_time()

for i in range(4000, 5004):
    cur.execute(f"insert into users values ({i}, 'Dummy')")

connection.commit()

api_time = process_time() - begin
print('psycopg: %.2fms' % (api_time * 1000))

begin = process_time()

for i in range(5004, 6004):
    q = users.insert((i, 'Dummy'))
    engine.execute(q)

sa_time = process_time() - begin
print('sqlalchemy: %.2fms' % (sa_time * 1000))

print('ratio: %.2f' % (sa_time / api_time))

cur.execute("delete from users where name='Dummy'")
connection.commit()