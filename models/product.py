from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey

from utils.database import Base


class Product(Base):
    __tablename__ = 'products'

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=True)
    image_path = Column(String(255), nullable=True)
    in_stock = Column(Boolean, nullable=False, default=False, server_default='0')

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
