from sqlalchemy import (create_engine, Column, Integer,
                        String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = 'Products'

    product_id = Column('ID', Integer, primary_key=True)
    product_name = Column('Name', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Date Updated', Date)

    def __repr__(self):
        price = self.product_price/100
        return f"""ID: {self.product_id}
                   \rProduct name: {self.product_name}
                   \rQuantity: {self.product_quantity}
                   \rPrice: ${price}
                   \rDate updated: {self.date_updated}"""