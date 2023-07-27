# setup a basic database model for webshop using python alchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """Table to store user information."""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)

class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    brand = Column(String)
    category = Column(String)

class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    order_date = Column(String)
    total_amount = Column(Float)
    shipping_address = Column(String)
    payment_method = Column(String)
    user = relationship(User)

class OrderItem(Base):
    __tablename__ = 'order_item'
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    quantity = Column(Integer)
    price_per_unit = Column(Float)
    order = relationship(Order)
    product = relationship(Product)



# setup a basic database model for website using python alchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """Table to store user information."""
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)

class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)
    brand = Column(String)
    category = Column(String)

class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    order_date = Column(String)
    total_amount = Column(Float)
    shipping_address = Column(String)
    payment_method = Column(String)
    user = relationship(User)

class OrderItem(Base):
    __tablename__ = 'order_item'
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    quantity = Column(Integer)
    price_per_unit = Column(Float)
    order = relationship(Order)
    product = relationship(Product)

