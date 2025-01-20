from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey

from utils.database import Base


class Product(Base):
    __tablename__ = 'products'

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=True)
    image_path = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False, default='0', server_default='0')
    article = Column(String(255), nullable=True)
    code = Column(String(255), nullable=True)
    unit = Column(String(55), nullable=True)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
