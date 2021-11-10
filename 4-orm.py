from sqlalchemy import *
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.schema import Column
from random import randrange


engine = create_engine('postgresql+psycopg2://postgres:1111@localhost:5432/test')

Base = declarative_base()

class User(Base):
    __table__ = Table('users', Base.metadata, autoload=True, autoload_with=engine)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(16))
    price = Column(Integer)


class ItemUserConnection(Base):
    __tablename__ = 'item_user_connection'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    item_id = Column(Integer)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

delete_all_users = session.query(User).delete()
delete_all_items = session.query(Item).delete()
delete_all_connections = session.query(ItemUserConnection).delete()

new_users = []
for i in range (100):
    new_users.append(User(id=i, name=f'user{i}'))

new_items = []
for i in range(50):
    new_items.append(Item(id=i, name=f'item{i}', price=randrange(100)))

new_connections = []
for i in range(15):
    new_connections.append(ItemUserConnection(id=i, user_id=randrange(100), item_id=randrange(50)))

session.add_all(new_users+new_items+new_connections)

q = session.query(User.id, User.name.label('users_name'), Item.name).filter(User.id > 20)\
                        .order_by(User.id)\
                        .join(ItemUserConnection, User.id == ItemUserConnection.user_id)\
                        .join(Item, ItemUserConnection.item_id == Item.id)\
                        .filter(Item.price < 50)

#for row in q.all():
#    print(row)

print(q.statement)

session.commit()