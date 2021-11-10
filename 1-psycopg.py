import psycopg2

connection = psycopg2.connect(dbname='test', user='postgres', password='1111')

cur = connection.cursor()

cur.execute(
    "insert into users values (101, 'Jesse');"
    "select * from users")

print(cur.fetchall())
connection.commit()